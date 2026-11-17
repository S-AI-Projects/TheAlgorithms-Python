"""
Base32 encoding and decoding

https://en.wikipedia.org/wiki/Base32
"""

B32_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


def base32_encode(data: bytes) -> bytes:
    """
    >>> base32_encode(b"Hello World!")
    b'JBSWY3DPEBLW64TMMQQQ===='
    >>> base32_encode(b"123456")
    b'GEZDGNBVGY======'
    >>> base32_encode(b"some long complex string")
    b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY='
    >>> base32_encode(b"")
    b''
    >>> base32_encode(b"f")
    b'MY======'
    >>> base32_encode(b"fo")
    b'MZXQ===='
    >>> base32_encode(b"foo")
    b'MZXW6==='
    >>> base32_encode(b"foob")
    b'MZXW6YQ='
    >>> base32_encode(b"fooba")
    b'MZXW6YTB'
    >>> base32_encode(b"\\xff")
    b'74======'
    """
    if not data:
        return b""
    binary_data = "".join(f"{byte:08b}" for byte in data)
    remainder = len(binary_data) % 5
    if remainder != 0:
        binary_data = binary_data.ljust(len(binary_data) + (5 - remainder), "0")
    b32_chunks = [binary_data[i : i + 5] for i in range(0, len(binary_data), 5)]
    b32_result = "".join(B32_CHARSET[int(chunk, 2)] for chunk in b32_chunks)
    pad_len = (8 - (len(b32_result) % 8)) % 8
    b32_result += "=" * pad_len
    return b32_result.encode("ascii")


def base32_decode(data: bytes) -> bytes:
    """
    >>> base32_decode(b'JBSWY3DPEBLW64TMMQQQ====')
    b'Hello World!'
    >>> base32_decode(b'GEZDGNBVGY======')
    b'123456'
    >>> base32_decode(b'ONXW2ZJANRXW4ZZAMNXW24DMMV4CA43UOJUW4ZY=')
    b'some long complex string'
    >>> base32_decode(b"")
    b''
    >>> base32_decode(b'MY======')
    b'f'
    >>> base32_decode(b'MZXQ====')
    b'fo'
    >>> base32_decode(b'MZXW6===')
    b'foo'
    >>> base32_decode(b'MZXW6YQ=')
    b'foob'
    >>> base32_decode(b'MZXW6YTB')
    b'fooba'
    >>> base32_decode(b'74======')
    b'\\xff'
    >>> base32_decode(b'INVALID!')
    Traceback (most recent call last):
        ...
    ValueError: Non-base32 digit found: '!'
    """
    if not data:
        return b""
    try:
        s = data.decode("ascii").rstrip("=")
    except UnicodeDecodeError:
        msg = "Non-ASCII characters in base32 data"
        raise ValueError(msg) from None

    for char in s:
        if char not in B32_CHARSET:
            msg = f"Non-base32 digit found: {char!r}"
            raise ValueError(msg)

    binary_chunks = "".join(f"{B32_CHARSET.index(char):05b}" for char in s)
    num_bytes = len(binary_chunks) // 8
    return bytes(
        int(binary_chunks[i * 8 : (i + 1) * 8], 2) for i in range(num_bytes)
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
