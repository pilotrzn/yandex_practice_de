class CipherMaster:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def cipher(self, original_text: str, shift: int):
        ciphered = []
        loop_index = len(self.alphabet)
        for letter in original_text.lower():
            # Если буква - конвертируем
            if str.isalpha(letter):
                current_index = self.alphabet.find(letter)
                cipher_index = current_index + shift
                if cipher_index > loop_index - 1:
                    cipher_index = (current_index + shift) % loop_index
                ciphered_letter = self.alphabet[cipher_index]
            else:
                ciphered_letter = letter
            ciphered.append(ciphered_letter)
        return (''.join(ciphered))

    def decipher(self, cipher_text: str, shift: int):
        return self.cipher(cipher_text, shift*-1)


cipher_master = CipherMaster()

print(cipher_master.cipher(
        original_text=str.format('Однажды ревьюер принял проект с '
                                 'первого раза, с тех пор я его боюсь'),
        shift=2))

print(cipher_master.decipher(
    cipher_text='Олебэи яфвнэ мроплж сэжи — э пэй рдв злййвкпш лп нвящывнэ',
    shift=-3
))
