import hashlib

def gen_hash(orig_substr: str, dig_sz: int) -> str:
    h = hashlib.blake2b(digest_size=dig_sz)
    h.update(orig_substr.encode())

    return h.hexdigest()
