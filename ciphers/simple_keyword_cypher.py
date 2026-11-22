def remove_duplicates(key: str) -> str:
    """
    Removes duplicate alphabetic characters in a keyword (letter is ignored after its
    first appearance).

    :param key: Keyword to use
    :return: String with duplicates removed

    >>> remove_duplicates('Hello World!!')
    'Helo Wrd'
    """

    key_no_dups = ""
    for ch in key:
        if ch == " " or (ch not in key_no_dups and ch.isalpha()):
            key_no_dups += ch
    return key_no_dups


def create_cipher_map(key: str) -> dict[str, str]:
    """
    Returns a cipher map given a keyword.

    :param key: keyword to use
    :return: dictionary cipher map

    >>> cmap = create_cipher_map('Goodbye!!')
    >>> len(cmap)
    26
    >>> cmap['A']
    'G'
    >>> cmap['B']
    'O'
    >>> cmap['Z']
    'Z'
    >>> identity = create_cipher_map('')
    >>> identity['A']
    'A'
    """
    # Create a list of the letters in the alphabet
    alphabet = [chr(i + 65) for i in range(26)]
    # Remove duplicate characters from key
    key = remove_duplicates(key.upper())
    offset = len(key)
    # First fill cipher with key characters
    cipher_alphabet = {alphabet[i]: char for i, char in enumerate(key)}
    # Then map remaining characters in alphabet to
    # the alphabet from the beginning
    for i in range(len(cipher_alphabet), 26):
        char = alphabet[i - offset]
        # Ensure we are not mapping letters to letters previously mapped
        while char in key:
            offset -= 1
            char = alphabet[i - offset]
        cipher_alphabet[alphabet[i]] = char
    return cipher_alphabet


def encipher(message: str, cipher_map: dict[str, str]) -> str:
    """
    Enciphers a message given a cipher map.

    :param message: Message to encipher
    :param cipher_map: Cipher map
    :return: enciphered string

    >>> encipher('Hello World!!', create_cipher_map('Goodbye!!'))
    'CYJJM VMQJB!!'
    """
    return "".join(cipher_map.get(ch, ch) for ch in message.upper())


def decipher(message: str, cipher_map: dict[str, str]) -> str:
    """
    Deciphers a message given a cipher map

    :param message: Message to decipher
    :param cipher_map: Dictionary mapping to use
    :return: Deciphered string

    >>> cipher_map = create_cipher_map('Goodbye!!')
    >>> decipher(encipher('Hello World!!', cipher_map), cipher_map)
    'HELLO WORLD!!'
    """
    # Reverse our cipher mappings
    rev_cipher_map = {v: k for k, v in cipher_map.items()}
    return "".join(rev_cipher_map.get(ch, ch) for ch in message.upper())


def process_cipher(message: str, key: str, option: str) -> str:
    """
    Enciphers or deciphers a message using a keyword cipher.

    :param message: Message to encipher or decipher
    :param key: Keyword for cipher map generation
    :param option: 'e' for encipher, 'd' for decipher
    :return: Enciphered or deciphered message
    :raises KeyError: If option is invalid

    >>> process_cipher('Hello World!!', 'Goodbye!!', 'e')
    'CYJJM VMQJB!!'
    >>> process_cipher('CYJJM VMQJB!!', 'Goodbye!!', 'd')
    'HELLO WORLD!!'
    >>> process_cipher('Hello World!!', 'Goodbye!!', 'E')
    'CYJJM VMQJB!!'
    >>> process_cipher('Hello', 'Key', 'x')
    Traceback (most recent call last):
        ...
    KeyError: 'invalid input option'
    """
    clean_option = option.strip()[:1].lower()
    operations = {"e": encipher, "d": decipher}
    if clean_option not in operations:
        raise KeyError("invalid input option")
    cipher_map = create_cipher_map(key)
    return operations[clean_option](message, cipher_map)


def main() -> None:
    """
    Handles I/O

    :return: void
    """
    message = input("Enter message to encode or decode: ").strip()
    key = input("Enter keyword: ").strip()
    option = input("Encipher or decipher? E/D:").strip()
    print(process_cipher(message, key, option))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
