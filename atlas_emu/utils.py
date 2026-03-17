# Bitwise utilities for Atlas's 48-bit and 24-bit words

MASK_48 = 0xFFFFFFFFFFFF
MASK_24 = 0xFFFFFF
MSB_48 = 1 << 47
MSB_24 = 1 << 23

def mask_48(val):
    """Keep only the bottom 48 bits."""
    return val & MASK_48

def mask_24(val):
    """Keep only the bottom 24 bits (B-store/Address size)."""
    return val & MASK_24

def to_signed_24(val):
    """Convert a 24-bit unsigned integer to a signed Python integer."""
    val &= MASK_24
    if val & MSB_24:
        return val - (1 << 24)
    return val

def from_signed_24(val):
    """Convert a signed Python integer to a 24-bit unsigned integer."""
    return val & MASK_24

def split_instruction(word):
    """
    Atlas instruction format (48 bits):
    F (10) | Ba (7) | Bm (7) | S (24)
    """
    f = (word >> 38) & 0x3FF
    ba = (word >> 31) & 0x7F
    bm = (word >> 24) & 0x7F
    s = word & MASK_24
    return f, ba, bm, s

def join_instruction(f, ba, bm, s):
    """Construct a 48-bit instruction word."""
    word = (f & 0x3FF) << 38
    word |= (ba & 0x7F) << 31
    word |= (bm & 0x7F) << 24
    word |= (s & MASK_24)
    return word
