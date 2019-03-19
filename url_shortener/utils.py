from base64 import b64encode, b64decode


KEY = 42


def encode(number: int) -> str:
    number = number ^ KEY
    bin_number = number.to_bytes(
        ((number.bit_length() + 7) // 8) + 1,
        byteorder='big',
        signed=True
    )
    return b64encode(bin_number).decode()


def decode(text: str) -> int:
    bin_number = b64decode(text)
    number = int.from_bytes(bin_number, byteorder='big', signed=True)
    return number ^ KEY
