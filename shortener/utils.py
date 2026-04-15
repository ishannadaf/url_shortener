import string

BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num):
    if num == 0:
        return BASE62_CHARS[0]

    base62 = []
    base = len(BASE62_CHARS)

    while num:
        num, rem = divmod(num, base)
        base62.append(BASE62_CHARS[rem])

    return ''.join(reversed(base62))