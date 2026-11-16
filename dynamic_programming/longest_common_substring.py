"""
Longest Common Substring Problem Statement:
    Given two sequences, find the
    longest common substring present in both of them. A substring is
    necessarily continuous.

Example:
    ``abcdef`` and ``xabded`` have two longest common substrings, ``ab`` or ``de``.
    Therefore, algorithm should return any one of them.
"""


def longest_common_substring(text1: str, text2: str) -> str:
    """
    Find the longest common substring between two strings.

    Time complexity is O(n * m), since each pair of characters is checked once.
    Space complexity is O(min(n, m)), since only two rows of the DP table are
    kept.

    >>> longest_common_substring("", "")
    ''
    >>> longest_common_substring("a","")
    ''
    >>> longest_common_substring("", "a")
    ''
    >>> longest_common_substring("a", "a")
    'a'
    >>> longest_common_substring("abcdef", "bcd")
    'bcd'
    >>> longest_common_substring("abcdef", "xabded")
    'ab'
    >>> longest_common_substring("GeeksforGeeks", "GeeksQuiz")
    'Geeks'
    >>> longest_common_substring("abcdxyz", "xyzabcd")
    'abcd'
    >>> longest_common_substring("zxabcdezy", "yzabcdezx")
    'abcdez'
    >>> longest_common_substring("OldSite:GeeksforGeeks.org", "NewSite:GeeksQuiz.com")
    'Site:Geeks'
    >>> longest_common_substring(1, 1)
    Traceback (most recent call last):
        ...
    ValueError: longest_common_substring() takes two strings for inputs
    >>> longest_common_substring("xyz", "axyz")
    'xyz'
    >>> longest_common_substring("abc", "xyz")
    ''
    >>> longest_common_substring("abc", "zzabcx")
    'abc'
    """

    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError("longest_common_substring() takes two strings for inputs")

    if not text1 or not text2:
        return ""

    if len(text1) >= len(text2):
        longer_text, shorter_text = text1, text2
    else:
        longer_text, shorter_text = text2, text1

    previous_row = [0] * (len(shorter_text) + 1)
    current_row = [0] * (len(shorter_text) + 1)
    end_pos = 0
    max_length = 0

    for i, longer_char in enumerate(longer_text, start=1):
        for j, shorter_char in enumerate(shorter_text, start=1):
            if longer_char == shorter_char:
                current_row[j] = previous_row[j - 1] + 1
                if current_row[j] > max_length:
                    end_pos = i
                    max_length = current_row[j]
            else:
                current_row[j] = 0
        previous_row, current_row = current_row, previous_row

    return longer_text[end_pos - max_length : end_pos]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
