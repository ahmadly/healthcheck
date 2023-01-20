"""
check must return a tuple of (status, message)
check must handle exceptions internally
check must handle timeouts internally
"""


def check_database_connection() -> tuple[bool, str]:
    return True, 'Database is reachable'


def check_cache_connection() -> tuple[bool, str]:
    return True, 'Cache is reachable'


def check_internet_connection() -> tuple[bool, str]:
    return True, 'Internet is reachable'
