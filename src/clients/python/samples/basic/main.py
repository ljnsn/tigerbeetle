"""Basic example."""

import logging
import os
import sys

from tb_client.bindings import CreateAccountResult, CreateTransferResult
from tb_client.client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(client: Client) -> None:
    """Run the example."""
    acc_id_1, acc_id_2 = 3, 4
    tx_id = 1002

    results = client.create_accounts(
        [
            {"id": acc_id_1, "ledger": 700, "code": 10},
            {"id": acc_id_2, "ledger": 700, "code": 10},
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

    transfer_results = client.create_transfers(
        [
            {
                "id": tx_id,
                "debit_account_id": acc_id_1,
                "credit_account_id": acc_id_2,
                "amount": 100,
                "ledger": 700,
                "code": 10,
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

    accounts = client.lookup_accounts([acc_id_1, acc_id_2])

    logger.info("Accounts looked up: %s", accounts)

    assert len(accounts) == 2

    for account in accounts:
        if account.id == acc_id_1:
            assert account.debits_posted == 100
            assert account.credits_posted == 0
        elif account.id == acc_id_2:
            assert account.debits_posted == 0
            assert account.credits_posted == 100
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
