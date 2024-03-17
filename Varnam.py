import os
import secrets

def generate_key(length):
    # Генерируем случайную строку, которая будет использоваться как ключ
    return ''.join([chr(secrets.randbelow(256)) for _ in range(length)])

def vernam_cipher(text, key):
    if len(text) != len(key):
        raise ValueError("Текст и ключ должны быть одинаковой длины")

    # Преобразование строки в список кодов символов
    text_ord = [ord(char) for char in text]
    key_ord = [ord(char) for char in key]

    # Выполнение операции XOR для каждого символа текста и ключа
    cipher_ord = [text_ord[i] ^ key_ord[i] for i in range(len(text_ord))]

    # Преобразование списка кодов символов обратно в строку
    cipher_text = ''.join([chr(ord_val) for ord_val in cipher_ord])

    return cipher_text

def encrypt_decrypt(input_text, key):
    return vernam_cipher(input_text, key)


def main():
    # Заданное сообщение
    message = "PGP — компьютерная программа, позволяющая выполнять операции шифрования кодирования) и цифровой подписи сообщений, файлов и другой информации."
    
    key_length = len(message)
    key = generate_key(key_length)
    print(f"Сгенерированный ключ: {key}")

    encrypted = encrypt_decrypt(message, key)
    print(f"Зашифрованный текст: {encrypted}")

    decrypted = encrypt_decrypt(encrypted, key)
    print(f"Расшифрованный текст: {decrypted}")
    

if __name__ == "__main__":
    main()
