"""Two-phase example."""

import logging
import os
import sys

from tb_client.bindings import CreateAccountResult, CreateTransferResult, TransferFlags
from tb_client.client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("two-phase")

increment = 6


def run(client: Client) -> None:
    acc_id_1 = 7 + increment * 2
    acc_id_2 = acc_id_1 + 1
    tx_id = 1004 + increment * 2

    results = client.create_accounts(
        [
            {"id": acc_id_1, "ledger": 1, "code": 1},
            {"id": acc_id_2, "ledger": 1, "code": 1},
        ]
    )

    halt = False
    for result in results:
        if result.result == CreateAccountResult.OK:
            continue
        halt = True
        msg = f"Error creating account: {result}"
        logger.error(msg)

    if halt:
        raise RuntimeError("Error creating accounts")

    logger.info("Accounts created")

    # start a pending transfer
    transfer_results = client.create_transfers(
        [
            {
                "id": tx_id,
                "debit_account_id": acc_id_1,
                "credit_account_id": acc_id_2,
                "amount": 500,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            }
        ]
    )

    for result in transfer_results:
        if result.result == CreateTransferResult.OK:
            continue
        halt = True
        msg = f"Error creating transfer: {result}"
        logger.error(msg)

    if halt:
        raise RuntimeError("Error creating transfers")

    logger.info("Transfers created")

    # Validate accounts pending and posted debits/credits before finishing the two-phase transfer
    accounts = client.lookup_accounts([acc_id_1, acc_id_2])

    logger.info("Accounts looked up: %s", accounts)

    assert len(accounts) == 2

    for account in accounts:
        if account.id == acc_id_1:
            assert account.debits_posted == 0, "account 1 debits, before posted"
            assert account.credits_posted == 0, "account 1 credits, before posted"
            assert (
                account.debits_pending == 500
            ), "account 1 debits pending, before posted"
            assert (
                account.credits_pending == 0
            ), "account 1 credits pending, before posted"
        elif account.id == acc_id_2:
            assert account.debits_posted == 0, "account 2 debits, before posted"
            assert account.credits_posted == 0, "account 2 credits, before posted"
            assert (
                account.debits_pending == 0
            ), "account 2 debits pending, before posted"
            assert (
                account.credits_pending == 500
            ), "account 2 credits pending, before posted"
        else:
            raise RuntimeError("Unexpected account")

    # Create a second transfer simply posting the first transfer
    transfer_results = client.create_transfers(
        [
            {
                "id": tx_id + 1,
                "debit_account_id": acc_id_1,
                "credit_account_id": acc_id_2,
                "amount": 500,
                "pending_id": tx_id,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.POST_PENDING_TRANSFER.value,
            }
        ]
    )

    for result in transfer_results:
        if result.result == CreateTransferResult.OK:
            continue
        halt = True
        msg = f"Error creating transfer: {result}"
        logger.error(msg)

    if halt:
        raise RuntimeError("Error creating transfers")

    logger.info("Transfers created")

    # Validate accounts pending and posted debits/credits after finishing the two-phase transfer
    accounts = client.lookup_accounts([acc_id_1, acc_id_2])

    for account in accounts:
        if account.id == acc_id_1:
            assert account.debits_posted == 500, "account 1 debits"
            assert account.credits_posted == 0, "account 1 credits"
            assert account.debits_pending == 0, "account 1 debits pending"
            assert account.credits_pending == 0, "account 1 credits pending"
        elif account.id == acc_id_2:
            assert account.debits_posted == 0, "account 2 debits"
            assert account.credits_posted == 500, "account 2 credits"
            assert account.debits_pending == 0, "account 2 debits pending"
            assert account.credits_pending == 0, "account 2 credits pending"
        else:
            raise RuntimeError("Unexpected account")


def main() -> None:
    port = os.getenv("TB_PORT", "3003")
    client = Client(0, [port], 256)

    run(client)

    # FIXME: .close() hangs trying to call deinit
    # try:
    #     run(client)
    # finally:
    #     client.close()


if __name__ == "__main__":
    sys.exit(main())
