"""
Return the ordinal suffix of an integer. Input n may be numeric or a string.
"""
def ordinal(n):
    # Use abs() to handle Python's handling of modulo for negative numbers.
    n = abs(int(n))
    if (n % 100) / 10 != 1 and (1 <= n % 10 <= 3):
        return ("st", "nd", "rd")[(n % 10) - 1]
    return "th"
