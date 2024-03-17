import os

# Используем ранее определенные S-блоки
S_BOXES = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
]

def gost28147_89_encrypt_block(key, block):
    assert len(block) == 8
    assert len(key) == 32

    n1, n2 = int.from_bytes(block[:4], 'little'), int.from_bytes(block[4:], 'little')

    for i in range(32):
        subkey = int.from_bytes(key[i % 8 * 4:(i % 8 + 1) * 4], 'little')
        result = n1 ^ subkey
        for j in range(8):
            result = (result >> 4 * j & 0xF) << 4 * j | S_BOXES[j][result >> 4 * j & 0xF]
        result = (result << 11 | result >> (32 - 11)) & 0xFFFFFFFF
        result ^= n2
        if i != 31:
            n2, n1 = n1, result
        else:
            n2 = result

    return n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

def gost28147_89_decrypt_block(key, block):
    assert len(block) == 8
    assert len(key) == 32

    n1, n2 = int.from_bytes(block[:4], 'little'), int.from_bytes(block[4:], 'little')

    for i in reversed(range(32)):
        subkey = int.from_bytes(key[i % 8 * 4:(i % 8 + 1) * 4], 'little')
        result = n1 ^ subkey
        for j in range(8):
            result = (result >> 4 * j & 0xF) << 4 * j | S_BOXES[j][result >> 4 * j & 0xF]
        result = (result << 11 | result >> (32 - 11)) & 0xFFFFFFFF
        result ^= n2
        if i != 31:
            n2, n1 = n1, result
        else:
            n2 = result

    return n2.to_bytes(4, 'little') + n1.to_bytes(4, 'little')

def gost28147_89_encrypt_file(key, input_file, output_file):
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while block := fin.read(8):
            if len(block) < 8:
                block += b'\x00' * (8 - len(block))  # Padding
            encrypted_block = gost28147_89_encrypt_block(key, block)
            fout.write(encrypted_block)

def gost28147_89_decrypt_file(key, input_file, output_file):
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        while block := fin.read(8):
            decrypted_block = gost28147_89_decrypt_block(key, block)
            fout.write(decrypted_block)

# Пример использования
key = os.urandom(32)  # Генерируем случайный 256-битный ключ
gost28147_89_encrypt_file(key, 'input.txt', 'decrypted.txt')
gost28147_89_decrypt_file(key, 'decrypted.txt', 'encrypted.txt')