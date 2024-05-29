"""Basic example."""

import logging
import os

from tb_client.bindings import CreateAccountResult, CreateTransferResult
from tb_client.client import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    port = os.getenv("TB_PORT", "3003")

    client = Client(0, [port], 256)

    results = client.create_accounts(
        [
            {"id": 102, "ledger": 700, "code": 10},
            {"id": 103, "ledger": 700, "code": 10},
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

    transfer_results = client.create_transfers(
        [
            {
                "id": 100,
                "debit_account_id": 102,
                "credit_account_id": 103,
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


if __name__ == "__main__":
    main()
