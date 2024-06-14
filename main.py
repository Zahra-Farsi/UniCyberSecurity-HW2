import random
def s_box_1(x):
    return (x + 1) % 256

def s_box_2(x):
    return x ^ 0xA5

def s_box_3(x):
    return (x * 3) % 256

def round_function(r, k):
    blocks = [(r >> (8 * i)) & 0xFF for i in range(8)]
    blocks = [s_box_1(blocks[0]), s_box_2(blocks[1]), s_box_3(blocks[2])] + blocks[3:]
    result = sum([blocks[i] << (8 * i) for i in range(8)])
    result ^= k
    return result

def generate_subkeys(key):
    subkeys = []
    for i in range(16):
        rotated_key = ((key << i) & (2**256 - 1)) | (key >> (256 - i))
        subkey = rotated_key ^ key
        subkeys.append((subkey >> 128) & (2**128 - 1))  
    return subkeys

def feistel_encrypt(plaintext, key):
    l, r = (plaintext >> 64) & (2**64 - 1), plaintext & (2**64 - 1)
    subkeys = generate_subkeys(key)
    for i in range(16):
        l, r = r, l ^ round_function(r, subkeys[i])
    ciphertext = (l << 64) | r
    return ciphertext


plaintext = 0x0123456789ABCDEF0123456789ABCDEF
key = 0xFEDCBA9876543210FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210  

ciphertext = feistel_encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext:032X}")
