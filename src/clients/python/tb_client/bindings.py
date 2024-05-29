#########################################################
## This file was auto-generated by python_bindings.zig ##
##              Do not manually modify.                ##
#########################################################

import enum
from dataclasses import dataclass

class AccountFlags(enum.Enum):
    """See [AccountFlags](https://docs.tigerbeetle.com/reference/account#flags)"""

    NONE = 0
    LINKED = (1 << 0)
    """See [linked](https://docs.tigerbeetle.com/reference/account#flagslinked)"""
    DEBITS_MUST_NOT_EXCEED_CREDITS = (1 << 1)
    """See [debits_must_not_exceed_credits](https://docs.tigerbeetle.com/reference/account#flagsdebits_must_not_exceed_credits)"""
    CREDITS_MUST_NOT_EXCEED_DEBITS = (1 << 2)
    """See [credits_must_not_exceed_debits](https://docs.tigerbeetle.com/reference/account#flagscredits_must_not_exceed_debits)"""
    HISTORY = (1 << 3)
    """See [history](https://docs.tigerbeetle.com/reference/account#flagshistory)"""


class TransferFlags(enum.Enum):
    """See [TransferFlags](https://docs.tigerbeetle.com/reference/transfer#flags)"""

    NONE = 0
    LINKED = (1 << 0)
    """See [linked](https://docs.tigerbeetle.com/reference/transfer#flagslinked)"""
    PENDING = (1 << 1)
    """See [pending](https://docs.tigerbeetle.com/reference/transfer#flagspending)"""
    POST_PENDING_TRANSFER = (1 << 2)
    """See [post_pending_transfer](https://docs.tigerbeetle.com/reference/transfer#flagspost_pending_transfer)"""
    VOID_PENDING_TRANSFER = (1 << 3)
    """See [void_pending_transfer](https://docs.tigerbeetle.com/reference/transfer#flagsvoid_pending_transfer)"""
    BALANCING_DEBIT = (1 << 4)
    """See [balancing_debit](https://docs.tigerbeetle.com/reference/transfer#flagsbalancing_debit)"""
    BALANCING_CREDIT = (1 << 5)
    """See [balancing_credit](https://docs.tigerbeetle.com/reference/transfer#flagsbalancing_credit)"""


class AccountFilterFlags(enum.Enum):
    """See [AccountFilterFlags](https://docs.tigerbeetle.com/reference/account-filter#flags)"""

    NONE = 0
    DEBITS = (1 << 0)
    """See [debits](https://docs.tigerbeetle.com/reference/account-filter#flagsdebits)"""
    CREDITS = (1 << 1)
    """See [credits](https://docs.tigerbeetle.com/reference/account-filter#flagscredits)"""
    REVERSED = (1 << 2)
    """See [reversed](https://docs.tigerbeetle.com/reference/account-filter#flagsreversed)"""


@dataclass
class Account:
    """See [Account](https://docs.tigerbeetle.com/reference/account/#)"""

    id: int
    """See [id](https://docs.tigerbeetle.com/reference/account/#id)"""
    debits_pending: int
    """See [debits_pending](https://docs.tigerbeetle.com/reference/account/#debits_pending)"""
    debits_posted: int
    """See [debits_posted](https://docs.tigerbeetle.com/reference/account/#debits_posted)"""
    credits_pending: int
    """See [credits_pending](https://docs.tigerbeetle.com/reference/account/#credits_pending)"""
    credits_posted: int
    """See [credits_posted](https://docs.tigerbeetle.com/reference/account/#credits_posted)"""
    user_data_128: int
    """See [user_data_128](https://docs.tigerbeetle.com/reference/account/#user_data_128)"""
    user_data_64: int
    """See [user_data_64](https://docs.tigerbeetle.com/reference/account/#user_data_64)"""
    user_data_32: int
    """See [user_data_32](https://docs.tigerbeetle.com/reference/account/#user_data_32)"""
    reserved: int
    """See [reserved](https://docs.tigerbeetle.com/reference/account/#reserved)"""
    ledger: int
    """See [ledger](https://docs.tigerbeetle.com/reference/account/#ledger)"""
    code: int
    """See [code](https://docs.tigerbeetle.com/reference/account/#code)"""
    flags: int
    """See [flags](https://docs.tigerbeetle.com/reference/account/#flags)"""
    timestamp: int
    """See [timestamp](https://docs.tigerbeetle.com/reference/account/#timestamp)"""


@dataclass
class Transfer:
    """See [Transfer](https://docs.tigerbeetle.com/reference/transfer/#)"""

    id: int
    """See [id](https://docs.tigerbeetle.com/reference/transfer/#id)"""
    debit_account_id: int
    """See [debit_account_id](https://docs.tigerbeetle.com/reference/transfer/#debit_account_id)"""
    credit_account_id: int
    """See [credit_account_id](https://docs.tigerbeetle.com/reference/transfer/#credit_account_id)"""
    amount: int
    """See [amount](https://docs.tigerbeetle.com/reference/transfer/#amount)"""
    pending_id: int
    """See [pending_id](https://docs.tigerbeetle.com/reference/transfer/#pending_id)"""
    user_data_128: int
    """See [user_data_128](https://docs.tigerbeetle.com/reference/transfer/#user_data_128)"""
    user_data_64: int
    """See [user_data_64](https://docs.tigerbeetle.com/reference/transfer/#user_data_64)"""
    user_data_32: int
    """See [user_data_32](https://docs.tigerbeetle.com/reference/transfer/#user_data_32)"""
    timeout: int
    """See [timeout](https://docs.tigerbeetle.com/reference/transfer/#timeout)"""
    ledger: int
    """See [ledger](https://docs.tigerbeetle.com/reference/transfer/#ledger)"""
    code: int
    """See [code](https://docs.tigerbeetle.com/reference/transfer/#code)"""
    flags: int
    """See [flags](https://docs.tigerbeetle.com/reference/transfer/#flags)"""
    timestamp: int
    """See [timestamp](https://docs.tigerbeetle.com/reference/transfer/#timestamp)"""


class CreateAccountResult(enum.Enum):
    """See [CreateAccountResult](https://docs.tigerbeetle.com/reference/requests/create_accounts#)"""

    OK = 0
    """See [ok](https://docs.tigerbeetle.com/reference/requests/create_accounts#ok)"""
    LINKED_EVENT_FAILED = 1
    """See [linked_event_failed](https://docs.tigerbeetle.com/reference/requests/create_accounts#linked_event_failed)"""
    LINKED_EVENT_CHAIN_OPEN = 2
    """See [linked_event_chain_open](https://docs.tigerbeetle.com/reference/requests/create_accounts#linked_event_chain_open)"""
    TIMESTAMP_MUST_BE_ZERO = 3
    """See [timestamp_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#timestamp_must_be_zero)"""
    RESERVED_FIELD = 4
    """See [reserved_field](https://docs.tigerbeetle.com/reference/requests/create_accounts#reserved_field)"""
    RESERVED_FLAG = 5
    """See [reserved_flag](https://docs.tigerbeetle.com/reference/requests/create_accounts#reserved_flag)"""
    ID_MUST_NOT_BE_ZERO = 6
    """See [id_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#id_must_not_be_zero)"""
    ID_MUST_NOT_BE_INT_MAX = 7
    """See [id_must_not_be_int_max](https://docs.tigerbeetle.com/reference/requests/create_accounts#id_must_not_be_int_max)"""
    FLAGS_ARE_MUTUALLY_EXCLUSIVE = 8
    """See [flags_are_mutually_exclusive](https://docs.tigerbeetle.com/reference/requests/create_accounts#flags_are_mutually_exclusive)"""
    DEBITS_PENDING_MUST_BE_ZERO = 9
    """See [debits_pending_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#debits_pending_must_be_zero)"""
    DEBITS_POSTED_MUST_BE_ZERO = 10
    """See [debits_posted_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#debits_posted_must_be_zero)"""
    CREDITS_PENDING_MUST_BE_ZERO = 11
    """See [credits_pending_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#credits_pending_must_be_zero)"""
    CREDITS_POSTED_MUST_BE_ZERO = 12
    """See [credits_posted_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#credits_posted_must_be_zero)"""
    LEDGER_MUST_NOT_BE_ZERO = 13
    """See [ledger_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#ledger_must_not_be_zero)"""
    CODE_MUST_NOT_BE_ZERO = 14
    """See [code_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_accounts#code_must_not_be_zero)"""
    EXISTS_WITH_DIFFERENT_FLAGS = 15
    """See [exists_with_different_flags](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_flags)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_128 = 16
    """See [exists_with_different_user_data_128](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_user_data_128)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_64 = 17
    """See [exists_with_different_user_data_64](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_user_data_64)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_32 = 18
    """See [exists_with_different_user_data_32](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_user_data_32)"""
    EXISTS_WITH_DIFFERENT_LEDGER = 19
    """See [exists_with_different_ledger](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_ledger)"""
    EXISTS_WITH_DIFFERENT_CODE = 20
    """See [exists_with_different_code](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists_with_different_code)"""
    EXISTS = 21
    """See [exists](https://docs.tigerbeetle.com/reference/requests/create_accounts#exists)"""


class CreateTransferResult(enum.Enum):
    """See [CreateTransferResult](https://docs.tigerbeetle.com/reference/requests/create_transfers#)"""

    OK = 0
    """See [ok](https://docs.tigerbeetle.com/reference/requests/create_transfers#ok)"""
    LINKED_EVENT_FAILED = 1
    """See [linked_event_failed](https://docs.tigerbeetle.com/reference/requests/create_transfers#linked_event_failed)"""
    LINKED_EVENT_CHAIN_OPEN = 2
    """See [linked_event_chain_open](https://docs.tigerbeetle.com/reference/requests/create_transfers#linked_event_chain_open)"""
    TIMESTAMP_MUST_BE_ZERO = 3
    """See [timestamp_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#timestamp_must_be_zero)"""
    RESERVED_FLAG = 4
    """See [reserved_flag](https://docs.tigerbeetle.com/reference/requests/create_transfers#reserved_flag)"""
    ID_MUST_NOT_BE_ZERO = 5
    """See [id_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#id_must_not_be_zero)"""
    ID_MUST_NOT_BE_INT_MAX = 6
    """See [id_must_not_be_int_max](https://docs.tigerbeetle.com/reference/requests/create_transfers#id_must_not_be_int_max)"""
    FLAGS_ARE_MUTUALLY_EXCLUSIVE = 7
    """See [flags_are_mutually_exclusive](https://docs.tigerbeetle.com/reference/requests/create_transfers#flags_are_mutually_exclusive)"""
    DEBIT_ACCOUNT_ID_MUST_NOT_BE_ZERO = 8
    """See [debit_account_id_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#debit_account_id_must_not_be_zero)"""
    DEBIT_ACCOUNT_ID_MUST_NOT_BE_INT_MAX = 9
    """See [debit_account_id_must_not_be_int_max](https://docs.tigerbeetle.com/reference/requests/create_transfers#debit_account_id_must_not_be_int_max)"""
    CREDIT_ACCOUNT_ID_MUST_NOT_BE_ZERO = 10
    """See [credit_account_id_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#credit_account_id_must_not_be_zero)"""
    CREDIT_ACCOUNT_ID_MUST_NOT_BE_INT_MAX = 11
    """See [credit_account_id_must_not_be_int_max](https://docs.tigerbeetle.com/reference/requests/create_transfers#credit_account_id_must_not_be_int_max)"""
    ACCOUNTS_MUST_BE_DIFFERENT = 12
    """See [accounts_must_be_different](https://docs.tigerbeetle.com/reference/requests/create_transfers#accounts_must_be_different)"""
    PENDING_ID_MUST_BE_ZERO = 13
    """See [pending_id_must_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_id_must_be_zero)"""
    PENDING_ID_MUST_NOT_BE_ZERO = 14
    """See [pending_id_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_id_must_not_be_zero)"""
    PENDING_ID_MUST_NOT_BE_INT_MAX = 15
    """See [pending_id_must_not_be_int_max](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_id_must_not_be_int_max)"""
    PENDING_ID_MUST_BE_DIFFERENT = 16
    """See [pending_id_must_be_different](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_id_must_be_different)"""
    TIMEOUT_RESERVED_FOR_PENDING_TRANSFER = 17
    """See [timeout_reserved_for_pending_transfer](https://docs.tigerbeetle.com/reference/requests/create_transfers#timeout_reserved_for_pending_transfer)"""
    AMOUNT_MUST_NOT_BE_ZERO = 18
    """See [amount_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#amount_must_not_be_zero)"""
    LEDGER_MUST_NOT_BE_ZERO = 19
    """See [ledger_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#ledger_must_not_be_zero)"""
    CODE_MUST_NOT_BE_ZERO = 20
    """See [code_must_not_be_zero](https://docs.tigerbeetle.com/reference/requests/create_transfers#code_must_not_be_zero)"""
    DEBIT_ACCOUNT_NOT_FOUND = 21
    """See [debit_account_not_found](https://docs.tigerbeetle.com/reference/requests/create_transfers#debit_account_not_found)"""
    CREDIT_ACCOUNT_NOT_FOUND = 22
    """See [credit_account_not_found](https://docs.tigerbeetle.com/reference/requests/create_transfers#credit_account_not_found)"""
    ACCOUNTS_MUST_HAVE_THE_SAME_LEDGER = 23
    """See [accounts_must_have_the_same_ledger](https://docs.tigerbeetle.com/reference/requests/create_transfers#accounts_must_have_the_same_ledger)"""
    TRANSFER_MUST_HAVE_THE_SAME_LEDGER_AS_ACCOUNTS = 24
    """See [transfer_must_have_the_same_ledger_as_accounts](https://docs.tigerbeetle.com/reference/requests/create_transfers#transfer_must_have_the_same_ledger_as_accounts)"""
    PENDING_TRANSFER_NOT_FOUND = 25
    """See [pending_transfer_not_found](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_not_found)"""
    PENDING_TRANSFER_NOT_PENDING = 26
    """See [pending_transfer_not_pending](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_not_pending)"""
    PENDING_TRANSFER_HAS_DIFFERENT_DEBIT_ACCOUNT_ID = 27
    """See [pending_transfer_has_different_debit_account_id](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_has_different_debit_account_id)"""
    PENDING_TRANSFER_HAS_DIFFERENT_CREDIT_ACCOUNT_ID = 28
    """See [pending_transfer_has_different_credit_account_id](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_has_different_credit_account_id)"""
    PENDING_TRANSFER_HAS_DIFFERENT_LEDGER = 29
    """See [pending_transfer_has_different_ledger](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_has_different_ledger)"""
    PENDING_TRANSFER_HAS_DIFFERENT_CODE = 30
    """See [pending_transfer_has_different_code](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_has_different_code)"""
    EXCEEDS_PENDING_TRANSFER_AMOUNT = 31
    """See [exceeds_pending_transfer_amount](https://docs.tigerbeetle.com/reference/requests/create_transfers#exceeds_pending_transfer_amount)"""
    PENDING_TRANSFER_HAS_DIFFERENT_AMOUNT = 32
    """See [pending_transfer_has_different_amount](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_has_different_amount)"""
    PENDING_TRANSFER_ALREADY_POSTED = 33
    """See [pending_transfer_already_posted](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_already_posted)"""
    PENDING_TRANSFER_ALREADY_VOIDED = 34
    """See [pending_transfer_already_voided](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_already_voided)"""
    PENDING_TRANSFER_EXPIRED = 35
    """See [pending_transfer_expired](https://docs.tigerbeetle.com/reference/requests/create_transfers#pending_transfer_expired)"""
    EXISTS_WITH_DIFFERENT_FLAGS = 36
    """See [exists_with_different_flags](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_flags)"""
    EXISTS_WITH_DIFFERENT_DEBIT_ACCOUNT_ID = 37
    """See [exists_with_different_debit_account_id](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_debit_account_id)"""
    EXISTS_WITH_DIFFERENT_CREDIT_ACCOUNT_ID = 38
    """See [exists_with_different_credit_account_id](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_credit_account_id)"""
    EXISTS_WITH_DIFFERENT_AMOUNT = 39
    """See [exists_with_different_amount](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_amount)"""
    EXISTS_WITH_DIFFERENT_PENDING_ID = 40
    """See [exists_with_different_pending_id](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_pending_id)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_128 = 41
    """See [exists_with_different_user_data_128](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_user_data_128)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_64 = 42
    """See [exists_with_different_user_data_64](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_user_data_64)"""
    EXISTS_WITH_DIFFERENT_USER_DATA_32 = 43
    """See [exists_with_different_user_data_32](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_user_data_32)"""
    EXISTS_WITH_DIFFERENT_TIMEOUT = 44
    """See [exists_with_different_timeout](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_timeout)"""
    EXISTS_WITH_DIFFERENT_CODE = 45
    """See [exists_with_different_code](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists_with_different_code)"""
    EXISTS = 46
    """See [exists](https://docs.tigerbeetle.com/reference/requests/create_transfers#exists)"""
    OVERFLOWS_DEBITS_PENDING = 47
    """See [overflows_debits_pending](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_debits_pending)"""
    OVERFLOWS_CREDITS_PENDING = 48
    """See [overflows_credits_pending](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_credits_pending)"""
    OVERFLOWS_DEBITS_POSTED = 49
    """See [overflows_debits_posted](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_debits_posted)"""
    OVERFLOWS_CREDITS_POSTED = 50
    """See [overflows_credits_posted](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_credits_posted)"""
    OVERFLOWS_DEBITS = 51
    """See [overflows_debits](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_debits)"""
    OVERFLOWS_CREDITS = 52
    """See [overflows_credits](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_credits)"""
    OVERFLOWS_TIMEOUT = 53
    """See [overflows_timeout](https://docs.tigerbeetle.com/reference/requests/create_transfers#overflows_timeout)"""
    EXCEEDS_CREDITS = 54
    """See [exceeds_credits](https://docs.tigerbeetle.com/reference/requests/create_transfers#exceeds_credits)"""
    EXCEEDS_DEBITS = 55
    """See [exceeds_debits](https://docs.tigerbeetle.com/reference/requests/create_transfers#exceeds_debits)"""


@dataclass
class CreateAccountsResult:

    index: int
    result: CreateAccountResult


@dataclass
class CreateTransfersResult:

    index: int
    result: CreateTransferResult


@dataclass
class AccountFilter:
    """See [AccountFilter](https://docs.tigerbeetle.com/reference/account-filter#)"""

    account_id: int
    """See [account_id](https://docs.tigerbeetle.com/reference/account-filter#account_id)"""
    timestamp_min: int
    """See [timestamp_min](https://docs.tigerbeetle.com/reference/account-filter#timestamp_min)"""
    timestamp_max: int
    """See [timestamp_max](https://docs.tigerbeetle.com/reference/account-filter#timestamp_max)"""
    limit: int
    """See [limit](https://docs.tigerbeetle.com/reference/account-filter#limit)"""
    flags: int
    """See [flags](https://docs.tigerbeetle.com/reference/account-filter#flags)"""


@dataclass
class AccountBalance:
    """See [AccountBalance](https://docs.tigerbeetle.com/reference/account-balances#)"""

    debits_pending: int
    """See [debits_pending](https://docs.tigerbeetle.com/reference/account-balances#debits_pending)"""
    debits_posted: int
    """See [debits_posted](https://docs.tigerbeetle.com/reference/account-balances#debits_posted)"""
    credits_pending: int
    """See [credits_pending](https://docs.tigerbeetle.com/reference/account-balances#credits_pending)"""
    credits_posted: int
    """See [credits_posted](https://docs.tigerbeetle.com/reference/account-balances#credits_posted)"""
    timestamp: int
    """See [timestamp](https://docs.tigerbeetle.com/reference/account-balances#timestamp)"""


class Operation(enum.Enum):

    PULSE = 128
    CREATE_ACCOUNTS = 129
    CREATE_TRANSFERS = 130
    LOOKUP_ACCOUNTS = 131
    LOOKUP_TRANSFERS = 132
    GET_ACCOUNT_TRANSFERS = 133
    GET_ACCOUNT_BALANCES = 134


