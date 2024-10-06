def int2bcd(data):
    if isinstance(data, int):
        data = str(data)
    value = 0
    for c in data:
        value *= 16
        value += int(c)
    return value


def pack_uint(value):
    if value == 0:
        return bytes([0x00])
    data = []
    while value > 0:
        data.insert(0, value & 0xFF)
        value >>= 8
    return bytes(data)


def unpack_uint(data):
    value = 0
    for datum in data:
        value <<= 8
        value += datum
    return value

