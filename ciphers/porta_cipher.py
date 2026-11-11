alphabet = {
    "A": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "B": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "C": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "D": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "E": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "F": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "G": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "H": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "I": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "J": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "K": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "L": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "M": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "N": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "O": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "P": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "Q": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "R": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "S": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "T": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "U": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "V": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "W": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "X": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "Y": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
    "Z": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
}


def validate_letters(name: str, value: str, allow_empty: bool = False) -> None:
    """
    Check that ``value`` is a ``str`` made only of the ASCII letters A-Z / a-z.

    Raises ``TypeError`` if ``value`` is not a ``str`` and ``ValueError`` if it is
    empty (unless ``allow_empty``) or contains any other character.

    >>> validate_letters("key", "marvin")
    >>> validate_letters("text", "", allow_empty=True)
    >>> validate_letters("key", None)
    Traceback (most recent call last):
        ...
    TypeError: key must be a str, not NoneType
    >>> validate_letters("key", "")
    Traceback (most recent call last):
        ...
    ValueError: key must not be empty
    >>> validate_letters("key", "ab1")
    Traceback (most recent call last):
        ...
    ValueError: key must contain only the letters A-Z, found '1'
    """
    if not isinstance(value, str):
        msg = f"{name} must be a str, not {type(value).__name__}"
        raise TypeError(msg)
    if not value and not allow_empty:
        msg = f"{name} must not be empty"
        raise ValueError(msg)
    for char in value:
        if not (char.isascii() and char.isalpha()):
            msg = f"{name} must contain only the letters A-Z, found {char!r}"
            raise ValueError(msg)


def generate_table(key: str) -> list[tuple[str, str]]:
    """
    Build the list of Porta tables used by ``key``, one per key letter.

    ``key`` must be a non-empty ``str`` of ASCII letters (upper or lower case).

    >>> generate_table('marvin')  # doctest: +NORMALIZE_WHITESPACE
    [('ABCDEFGHIJKLM', 'UVWXYZNOPQRST'), ('ABCDEFGHIJKLM', 'NOPQRSTUVWXYZ'),
     ('ABCDEFGHIJKLM', 'STUVWXYZNOPQR'), ('ABCDEFGHIJKLM', 'QRSTUVWXYZNOP'),
     ('ABCDEFGHIJKLM', 'WXYZNOPQRSTUV'), ('ABCDEFGHIJKLM', 'UVWXYZNOPQRST')]
    >>> generate_table('MARVIN') == generate_table('marvin')
    True
    >>> generate_table('')
    Traceback (most recent call last):
        ...
    ValueError: key must not be empty
    >>> generate_table('mar vin')
    Traceback (most recent call last):
        ...
    ValueError: key must contain only the letters A-Z, found ' '
    >>> generate_table('ma5vin')
    Traceback (most recent call last):
        ...
    ValueError: key must contain only the letters A-Z, found '5'
    >>> generate_table('\u00df')
    Traceback (most recent call last):
        ...
    ValueError: key must contain only the letters A-Z, found '\xdf'
    >>> generate_table(None)
    Traceback (most recent call last):
        ...
    TypeError: key must be a str, not NoneType
    >>> generate_table(b'marvin')
    Traceback (most recent call last):
        ...
    TypeError: key must be a str, not bytes
    """
    validate_letters("key", key)
    return [alphabet[char] for char in key.upper()]


def encrypt(key: str, words: str) -> str:
    """
    Encrypt ``words`` with the Porta cipher using ``key``.

    Input contract: ``key`` must be a non-empty ``str`` of ASCII letters and
    ``words`` must be a ``str`` of ASCII letters (spaces, digits and punctuation
    are not supported). Upper and lower case are treated the same, and the result
    is always upper case. An empty ``words`` gives an empty string.

    >>> encrypt('marvin', 'jessica')
    'QRACRWU'
    >>> encrypt('MaRvIn', 'JeSsIcA')
    'QRACRWU'
    >>> encrypt('marvin', '')
    ''
    >>> encrypt('', 'jessica')
    Traceback (most recent call last):
        ...
    ValueError: key must not be empty
    >>> encrypt('mar1in', 'jessica')
    Traceback (most recent call last):
        ...
    ValueError: key must contain only the letters A-Z, found '1'
    >>> encrypt(123, 'jessica')
    Traceback (most recent call last):
        ...
    TypeError: key must be a str, not int
    >>> encrypt('marvin', None)
    Traceback (most recent call last):
        ...
    TypeError: words must be a str, not NoneType
    >>> encrypt('marvin', 'hello world')
    Traceback (most recent call last):
        ...
    ValueError: words must contain only the letters A-Z, found ' '
    >>> encrypt('marvin', 'abc123')
    Traceback (most recent call last):
        ...
    ValueError: words must contain only the letters A-Z, found '1'
    """
    validate_letters("words", words, allow_empty=True)
    table = generate_table(key)
    cipher = ""
    count = 0
    for char in words.upper():
        cipher += get_opponent(table[count], char)
        count = (count + 1) % len(table)
    return cipher


def decrypt(key: str, words: str) -> str:
    """
    Decrypt ``words`` with ``key``. The Porta cipher is reciprocal, so this is the
    same operation as ``encrypt`` and has the same input contract.

    >>> decrypt('marvin', 'QRACRWU')
    'JESSICA'
    >>> decrypt('', 'QRACRWU')
    Traceback (most recent call last):
        ...
    ValueError: key must not be empty
    >>> decrypt('marvin', 'QRA1')
    Traceback (most recent call last):
        ...
    ValueError: words must contain only the letters A-Z, found '1'
    """
    return encrypt(key, words)


def get_position(table: tuple[str, str], char: str) -> tuple[int, int]:
    """
    >>> get_position(generate_table('marvin')[0], 'M')
    (0, 12)
    """
    # `char` is either in the 0th row or the 1st row
    row = 0 if char in table[0] else 1
    col = table[row].index(char)
    return row, col


def get_opponent(table: tuple[str, str], char: str) -> str:
    """
    >>> get_opponent(generate_table('marvin')[0], 'M')
    'T'
    """
    row, col = get_position(table, char.upper())
    if row == 1:
        return table[0][col]
    else:
        return table[1][col] if row == 0 else char


if __name__ == "__main__":
    import doctest

    doctest.testmod()  # Fist ensure that all our tests are passing...
    """
    Demo:

    Enter key: marvin
    Enter text to encrypt: jessica
    Encrypted: QRACRWU
    Decrypted with key: JESSICA
    """
    key = input("Enter key: ").strip()
    text = input("Enter text to encrypt: ").strip()
    cipher_text = encrypt(key, text)

    print(f"Encrypted: {cipher_text}")
    print(f"Decrypted with key: {decrypt(key, cipher_text)}")
