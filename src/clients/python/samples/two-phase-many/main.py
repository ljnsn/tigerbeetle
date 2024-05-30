"""Two-phase-many example."""

import logging
import os
import sys
from dataclasses import dataclass

from tb_client.bindings import (
    CreateAccountResult,
    CreateTransferResult,
    TransferFlags,
)
from tb_client.client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("two-phase-many")


@dataclass
class Acc:
    id: int
    debits_posted: int
    credits_posted: int
    debits_pending: int
    credits_pending: int


def assert_account_balances(
    client: Client,
    accounts: list[Acc],
    debug_msg: str,
) -> None:
    """Assert account balances."""
    ids = [account.id for account in accounts]
    accounts_found = client.lookup_accounts(ids)
    assert len(accounts) == len(accounts_found), "accounts"

    for account_found in accounts_found:
        requested = False
        for account in accounts:
            requested = True
            if account.id == account_found.id:
                assert (
                    account.debits_posted == account_found.debits_posted
                ), f"{debug_msg} debits posted"
                assert (
                    account.credits_posted == account_found.credits_posted
                ), f"{debug_msg} credits posted"
                assert (
                    account.debits_pending == account_found.debits_pending
                ), f"{debug_msg} debits pending"
                assert (
                    account.credits_pending == account_found.credits_pending
                ), f"{debug_msg} credits pending"

        if not requested:
            msg = f"Unexpected account found: {account_found.id}"
            raise RuntimeError(msg)


def run(client: Client) -> None:
    results = client.create_accounts(
        [
            {"id": 1, "ledger": 1, "code": 1},
            {"id": 2, "ledger": 1, "code": 1},
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

    # start five pending transfers
    transfer_results = client.create_transfers(
        [
            {
                "id": 1,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 100,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            },
            {
                "id": 2,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 200,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            },
            {
                "id": 3,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 300,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            },
            {
                "id": 4,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 400,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            },
            {
                "id": 5,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 500,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.PENDING.value,
            },
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
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=0,
                credits_posted=0,
                debits_pending=1500,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=0,
                debits_pending=0,
                credits_pending=1500,
            ),
        ],
        "after starting five pending transfers",
    )

    # Create a 6th transfer posting the 1st transfer
    transfer_results = client.create_transfers(
        [
            {
                "id": 6,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 100,
                "pending_id": 1,
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

    # Validate account balances after posting 1st pending transfer.
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=100,
                credits_posted=0,
                debits_pending=1400,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=100,
                debits_pending=0,
                credits_pending=1400,
            ),
        ],
        "after completing 1 pending transfer",
    )

    # Create a 7th transfer voiding the 2nd transfer.
    transfer_results = client.create_transfers(
        [
            {
                "id": 7,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 200,
                "pending_id": 2,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.VOID_PENDING_TRANSFER.value,
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

    # Validate account balances after voiding 2nd pending transfer.
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=100,
                credits_posted=0,
                debits_pending=1200,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=100,
                debits_pending=0,
                credits_pending=1200,
            ),
        ],
        "after voiding 2nd pending transfer",
    )

    # Create an 8th transfer posting the 3rd transfer.
    transfer_results = client.create_transfers(
        [
            {
                "id": 8,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 300,
                "pending_id": 3,
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

    # Validate account balances after posting 3rd pending transfer.
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=400,
                credits_posted=0,
                debits_pending=900,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=400,
                debits_pending=0,
                credits_pending=900,
            ),
        ],
        "after posting 3rd pending transfer",
    )

    # Create a 9th transfer voiding the 4th transfer.
    transfer_results = client.create_transfers(
        [
            {
                "id": 9,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 400,
                "pending_id": 4,
                "ledger": 1,
                "code": 1,
                "flags": TransferFlags.VOID_PENDING_TRANSFER.value,
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

    # Validate account balances after voiding 4th pending transfer.
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=400,
                credits_posted=0,
                debits_pending=500,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=400,
                debits_pending=0,
                credits_pending=500,
            ),
        ],
        "after voiding 4th pending transfer",
    )

    # Create a 10th transfer posting the 5th transfer.
    transfer_results = client.create_transfers(
        [
            {
                "id": 10,
                "debit_account_id": 1,
                "credit_account_id": 2,
                "amount": 500,
                "pending_id": 5,
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

    # Validate account balances after voiding 5th pending transfer.
    assert_account_balances(
        client,
        [
            Acc(
                id=1,
                debits_posted=900,
                credits_posted=0,
                debits_pending=0,
                credits_pending=0,
            ),
            Acc(
                id=2,
                debits_posted=0,
                credits_posted=900,
                debits_pending=0,
                credits_pending=0,
            ),
        ],
        "after posting 5th pending transfer",
    )


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
