def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = chr((ord(char) + shift - ord('A' if is_upper else 'a')) % 26 + ord('A' if is_upper else 'a'))
        result += char
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)
