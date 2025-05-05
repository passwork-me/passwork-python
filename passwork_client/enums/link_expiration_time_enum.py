from enum import StrEnum

class LinkExpirationTime(StrEnum):
    Hour = '1 hour'
    Week = '1 week'
    Month = '1 month'
    Unlimited = 'unlimited'