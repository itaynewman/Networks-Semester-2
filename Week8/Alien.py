

def custom_cipher_decipher(string, caesar_key):
    error_number = int(caesar_key[-3:])
    result = []
    for i, char in enumerate(string):
        if i % 2 != 0 or not char.isalpha():
            result.append(char)
        else:
            new_char = chr((ord(char) - ord('a') - error_number) % 26 + ord('a')) if char.islower() else chr((ord(char) - ord('A') - error_number) % 26 + ord('A'))
            result.append(new_char)
    return ''.join(result)


def main():
    print(custom_cipher_decipher("zrrnj sldnht! wo iqiwidth d fope bdcn, poedsh hnweu whh qape oi rnh rf tke poaqews iq whh vooau vyvthm.", "ERR003"))


if __name__ == '__main__':
    main()
