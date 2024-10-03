def is_palindrome(text):
    # Ваш код здесь
    s_text = str.lower(text)
    s_text = str.replace(s_text, ' ', '')
    s_text_reverse = s_text[::-1]
    if s_text_reverse == s_text:
        return True
    else:
        return False


# Должно быть напечатано True:
print(is_palindrome('А роза упала на лапу Азора'))
# Должно быть напечатано False:
print(is_palindrome('Не палиндром'))
