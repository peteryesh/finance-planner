from enum import Enum


class AccountType(Enum):
    NONE = 0
    CHECKING = 1
    SAVINGS = 2
    MMA = 3
    CD = 4
    IRA = 5
    RETIREMENT = 6
    BROKERAGE = 7
    CREDIT = 8
    HSA = 9


class TransactionType(Enum):
    NONE = 0
    FOOD = 1
    SPENDING = 2
    TRANSPORTATION = 3
    HOUSING = 4
    UTILITIES = 5
    SUPPLIES = 6
    COSMETICS = 7
    INSURANCE = 8
    EDUCATION = 9
    ENTERTAINMENT = 10
    SUBSCRIPTIONS = 11
    MEDICAL = 12
    MISCELLANEOUS = 13
    PAYMENT = 14
    TRANSFER = 15
