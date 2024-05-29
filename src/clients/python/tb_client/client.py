"""Python client for TigerBeetle."""

import threading
from dataclasses import dataclass

from tb_client import _tb_client, bindings, errors

ffi = _tb_client.ffi
lib = _tb_client.lib


@dataclass(slots=True)
class Request:
    id: int
    packet: ffi.CData
    result: ffi.CData
    ready: threading.Event


@ffi.def_extern()
def on_completion_fn(context, client, packet, result_ptr, result_len):
    """
    Simple statically registered extern "Python" fn. This gets
    called for any callbacks, looks up the respective client from our
    global mapping, and forwards on the callback.

    NB: This runs in the Zig's client thread.
    """
    client = Client.completion_mapping[client]
    client._on_completion_fn(context, client, packet, result_ptr, result_len)


# class ClientInterface(abc.ABC):
#     """Client interface for TigerBeetle."""
#
#     @abc.abstractmethod
#     def create_accounts(self, batch):
#         """Create accounts in the ledger.
#
#         Args:
#             batch (List[Dict]): List of account dictionaries.
#
#         Returns:
#             List[Dict]: List of account creation results.
#         """
#
#     @abc.abstractmethod
#     def create_transfers(self, batch):
#         """Create transfers in the ledger.
#
#         Args:
#             batch (List[Dict]): List of transfer dictionaries.
#
#         Returns:
#             List[Dict]: List of transfer creation results.
#         """
#
#     @abc.abstractmethod
#     def lookup_accounts(self):
#         """Lookup accounts in the ledger.
#
#         Returns:
#             List[Dict]: List of account dictionaries.
#         """
#
#     @abc.abstractmethod
#     def lookup_transfers(self):
#         """Lookup transfers in the ledger.
#
#         Returns:
#             List[Dict]: List of transfer dictionaries.
#         """
#
#     @abc.abstractmethod
#     def get_account_transfers(self, filter):
#         """Get transfers for an account.
#
#         Args:
#             filter (Dict): Filter dictionary.
#
#         Returns:
#             List[Dict]: List of transfer dictionaries.
#         """
#
#     @abc.abstractmethod
#     def get_account_balances(self, filter):
#         """Get balances for an account.
#
#         Args:
#             filter (Dict): Filter dictionary.
#
#         Returns:
#             List[Dict]: List of balance dictionaries.
#         """


def to_bigint(x: int) -> tuple[int, int]:
    b = f"{x:0>128b}"
    assert len(b) == 128
    return int(b[:64], 2), int(b[64:], 2)


def from_bigint(high: int, low: int) -> int:
    mask = 1 << 64
    if high == 0 and low == 0:
        return 0
    if high < 0:
        high = high + mask
    if low < 0:
        low = low + mask
    return low + high * mask


def cint128_to_int(x: ffi.CData) -> int:
    return from_bigint(x.high, x.low)


# TODO: ensure endianness is correct
class Client:
    """Client for TigerBeetle."""

    completion_mapping = {}

    def __init__(
        self,
        cluster_id: int,
        addresses: list[str],
        concurrency_max: int,
    ) -> None:
        self._tb_client: ffi.CData | None = ffi.new("tb_client_t *")
        addresses_raw = ",".join(addresses).encode()
        status = lib.tb_client_init(
            self._tb_client,
            to_bigint(cluster_id),
            ffi.new("char[]", addresses_raw),
            len(addresses_raw),
            concurrency_max,
            0,
            lib.on_completion_fn,
        )

        if status != lib.TB_STATUS_SUCCESS:
            self._raise_status(status)

        self.completion_mapping[self._tb_client[0]] = self
        self.inflight = {}

    def _raise_status(self, status: int) -> None:
        match status:
            case lib.TB_STATUS_UNEXPECTED:
                raise errors.UnexpectedError()
            case lib.TB_STATUS_OUT_OF_MEMORY:
                raise errors.OutOfMemoryError()
            case lib.TB_STATUS_ADDRESS_INVALID:
                raise errors.InvalidAddressError()
            case lib.TB_STATUS_ADDRESS_LIMIT_EXCEEDED:
                raise errors.AddressLimitExceededError()
            case lib.TB_STATUS_CONCURRENCY_MAX_INVALID:
                raise errors.InvalidConcurrencyMaxError()
            case lib.TB_STATUS_SYSTEM_RESOURCES:
                raise errors.SystemResourcesError()
            case lib.TB_STATUS_NETWORK_SUBSYSTEM:
                raise errors.NetworkSubsystemError()
            case _:
                msg = f"Unexpected status: {status}"
                raise errors.TigerBeetleError(msg)

    def close(self) -> None:
        print("closing client")
        if self._tb_client is not None:
            del self.completion_mapping[self._tb_client[0]]
            lib.tb_client_deinit(self._tb_client[0])
            self._tb_client = None

    def create_accounts(
        self,
        accounts: list[dict],
    ) -> list[bindings.CreateAccountsResult]:
        """Create accounts in the ledger.

        Args:
            accounts: List of account dictionaries.

        Returns:
            List of account creation results.
        """
        count = len(accounts)
        results = ffi.new("tb_create_accounts_result_t[]", count)

        batch = ffi.new("tb_account_t[]", count)
        for idx, account in enumerate(accounts):
            batch[idx].id = to_bigint(account["id"])
            batch[idx].ledger = account["ledger"]
            batch[idx].code = account["code"]
            batch[idx].flags = account.get("flags", 0)
            batch[idx].user_data_128 = to_bigint(account.get("user_data_128", 0))
            batch[idx].user_data_64 = account.get("user_data_64", 0)
            batch[idx].user_data_32 = account.get("user_data_32", 0)
            batch[idx].timestamp = 0

        wrote = self._do_request(
            bindings.Operation.CREATE_ACCOUNTS,
            count,
            batch,
            results,
        )
        print("wrote", wrote)

        # result_count = wrote // int(ffi.sizeof("tb_create_accounts_result_t"))
        return [
            bindings.CreateAccountsResult(
                result.index,
                bindings.CreateAccountResult(result.result),
            )
            for result in results
        ]

    def create_transfers(
        self,
        transfers: list[dict],
    ) -> list[bindings.CreateTransfersResult]:
        """Create transfers in the ledger.

        Args:
            transfers: List of transfer dictionaries.

        Returns:
            List of transfer creation results.
        """
        count = len(transfers)
        results = ffi.new("tb_create_transfers_result_t[]", count)

        batch = ffi.new("tb_transfer_t[]", count)
        for idx, transfer in enumerate(transfers):
            batch[idx].id = to_bigint(transfer["id"])
            batch[idx].debit_account_id = to_bigint(transfer["debit_account_id"])
            batch[idx].credit_account_id = to_bigint(transfer["credit_account_id"])
            batch[idx].amount = to_bigint(transfer["amount"])
            batch[idx].pending_id = to_bigint(transfer.get("pending_id", 0))
            batch[idx].user_data_128 = to_bigint(transfer.get("user_data_128", 0))
            batch[idx].user_data_64 = transfer.get("user_data_64", 0)
            batch[idx].user_data_32 = transfer.get("user_data_32", 0)
            batch[idx].timeout = transfer.get("timeout", 0)
            batch[idx].ledger = transfer["ledger"]
            batch[idx].code = transfer["code"]
            batch[idx].flags = transfer.get("flags", 0)
            batch[idx].timestamp = 0

        wrote = self._do_request(
            bindings.Operation.CREATE_TRANSFERS,
            count,
            batch,
            results,
        )
        print("wrote", wrote)

        # result_count = wrote // int(ffi.sizeof("tb_create_transfers_result_t"))
        return [
            bindings.CreateTransfersResult(
                result.index,
                bindings.CreateTransferResult(result.result),
            )
            for result in results
        ]

    def lookup_accounts(self, account_ids: list[int]) -> list[bindings.Account]:
        """Lookup accounts in the ledger.

        Args:
            account_ids: List of account IDs to look up.

        Returns:
            List of account dictionaries.
        """
        count = len(account_ids)
        results = ffi.new("tb_account_t[]", count)

        batch = ffi.new("tb_uint128_t[]", [to_bigint(i) for i in account_ids])

        wrote = self._do_request(
            bindings.Operation.LOOKUP_ACCOUNTS,
            count,
            batch,
            results,
        )
        print("wrote", wrote)

        result_count = wrote // int(ffi.sizeof("tb_account_t"))
        return [
            bindings.Account(
                id=from_bigint(result.id.high, result.id.low),
                debits_pending=cint128_to_int(result.debits_pending),
                debits_posted=cint128_to_int(result.debits_posted),
                credits_pending=cint128_to_int(result.credits_pending),
                credits_posted=cint128_to_int(result.credits_posted),
                user_data_128=cint128_to_int(result.user_data_128),
                user_data_64=result.user_data_64,
                user_data_32=result.user_data_32,
                ledger=result.ledger,
                code=result.code,
                flags=result.flags,
                timestamp=result.timestamp,
                reserved=result.reserved,
            )
            for result in results[0:result_count]
        ]

    def _do_request(
        self,
        op: bindings.Operation,
        count: int,
        data: ffi.CData,
        result: ffi.CData,
    ) -> int:
        print("sending request")
        if count == 0:
            raise errors.EmptyBatchError()

        if self._tb_client is None:
            raise errors.ClientClosedError()

        req = Request(
            id=0,
            packet=ffi.new("tb_packet_t *"),
            result=result,
            ready=threading.Event(),
        )
        print("request", req)
        status = lib.tb_client_acquire_packet(
            self._tb_client[0],
            ffi.new("tb_packet_t * *", req.packet),
        )
        if status == lib.TB_STATUS_CONCURRENCY_MAX_INVALID:
            raise errors.ConcurrencyExceededError()
        if status == lib.TB_PACKET_ACQUIRE_SHUTDOWN:
            raise errors.ClientClosedError()
        if req.packet is None:
            raise errors.TigerBeetleError("Unexpected None packet")

        print("status", status)
        lib.tb_client_release_packet(self._tb_client[0], req.packet)

        req.packet.user_data = ffi.cast("void *", req.id)
        req.packet.operation = ffi.cast("TB_OPERATION", op.value)
        req.packet.status = lib.TB_PACKET_OK
        req.packet.data_size = count * get_event_size(op)
        req.packet.data = data

        self.inflight[req.id] = req

        # Submit the request.
        lib.tb_client_submit(self._tb_client[0], req.packet)

        # Wait for the response
        req.ready.wait()
        status = int(ffi.cast("TB_PACKET_STATUS", req.packet.status))

        if status != lib.TB_PACKET_OK:
            match status:
                case lib.TB_PACKET_TOO_MUCH_DATA:
                    raise errors.MaximumBatchSizeExceededError()
                case lib.TB_PACKET_INVALID_OPERATION:
                    # we control what C.TB_OPERATION is given
                    # but allow an invalid opcode to be passed to emulate a client nop
                    raise errors.InvalidOperationError()
                case lib.TB_PACKET_INVALID_DATA_SIZE:
                    # we control what type of data is given
                    raise Exception("unreachable")
                case _:
                    raise Exception(
                        "tb_client_submit(): returned packet with invalid status"
                    )

        # Return the amount of bytes written into result
        return int(req.packet.data_size)

    def _on_completion_fn(
        self,
        context,
        client,
        packet,
        result_ptr,
        result_len,
    ) -> None:
        print("request complete")
        req = self.inflight[int(ffi.cast("int", packet[0].user_data))]
        if req.packet != packet:
            raise Exception("Packet mismatch")

        wrote = 0
        if result_len > 0 and result_ptr is not None:
            op = bindings.Operation(int(packet.operation))
            result_size = get_result_size(op)
            if result_len % result_size != 0:
                raise Exception("Invalid result length")

            if (
                op.value != lib.TB_OPERATION_GET_ACCOUNT_TRANSFERS
                and op.value != lib.TB_OPERATION_GET_ACCOUNT_BALANCES
            ):
                # Make sure the amount of results at least matches the amount of requests.
                count = packet.data_size // get_event_size(op)
                if count * result_size < result_len:
                    raise Exception("Invalid result length")

            if req.result is not None:
                wrote = result_len
                ffi.memmove(req.result, result_ptr, wrote)

        req.packet.data_size = wrote
        req.ready.set()


def get_event_size(op: bindings.Operation) -> int:
    return {
        lib.TB_OPERATION_CREATE_ACCOUNTS: ffi.sizeof("tb_account_t"),
        lib.TB_OPERATION_CREATE_TRANSFERS: ffi.sizeof("tb_transfer_t"),
        lib.TB_OPERATION_LOOKUP_ACCOUNTS: ffi.sizeof("tb_uint128_t"),
        lib.TB_OPERATION_LOOKUP_TRANSFERS: ffi.sizeof("tb_uint128_t"),
        lib.TB_OPERATION_GET_ACCOUNT_TRANSFERS: ffi.sizeof("tb_account_filter_t"),
        lib.TB_OPERATION_GET_ACCOUNT_BALANCES: ffi.sizeof("tb_account_filter_t"),
    }.get(op.value, 0)


def get_result_size(op: bindings.Operation) -> int:
    return {
        lib.TB_OPERATION_CREATE_ACCOUNTS: ffi.sizeof("tb_create_accounts_result_t"),
        lib.TB_OPERATION_CREATE_TRANSFERS: ffi.sizeof("tb_create_transfers_result_t"),
        lib.TB_OPERATION_LOOKUP_ACCOUNTS: ffi.sizeof("tb_account_t"),
        lib.TB_OPERATION_LOOKUP_TRANSFERS: ffi.sizeof("tb_transfer_t"),
        lib.TB_OPERATION_GET_ACCOUNT_TRANSFERS: ffi.sizeof("tb_account_t"),
        lib.TB_OPERATION_GET_ACCOUNT_BALANCES: ffi.sizeof("tb_account_balance_t"),
    }.get(op.value, 0)
