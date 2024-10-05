class CipherMaster:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def process_text(self, text: str, shift: int, is_encrypt: bool):
        real_shift = shift if is_encrypt else shift*-1
        ciphered = []
        loop_index = len(self.alphabet)
        for letter in text.lower():
            # Если буква - конвертируем
            if str.isalpha(letter):
                current_index = self.alphabet.find(letter)
                cipher_index = current_index + real_shift
                if cipher_index > loop_index - 1:
                    cipher_index = (current_index + real_shift) % loop_index
                ciphered_letter = self.alphabet[cipher_index]
            else:
                ciphered_letter = letter
            ciphered.append(ciphered_letter)
        return (''.join(ciphered))


cipher_master = CipherMaster()

print(cipher_master.process_text(
        text=str.format('Однажды ревьюер принял проект с '
                        'первого раза, с тех пор я его боюсь'),
        shift=2,
        is_encrypt=True))

print(cipher_master.process_text(
    text='Олебэи яфвнэ мроплж сэжи — э пэй рдв злййвкпш лп нвящывнэ',
    shift=-3,
    is_encrypt=False))
