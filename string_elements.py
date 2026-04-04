string = input("Enter the string: ")

unique_chars = []
for ch in string:
    if ch not in unique_chars:
        unique_chars.append(ch)

small_char = []
cap_char = []
dig = []
symbol = []
vowels = []
consonants = []

is_vowel = "aeiouAEIOU"

for ch in unique_chars:
    if ch.islower():
        small_char.append(ch)
        if ch in is_vowel:
            vowels.append(ch)
        else:
            consonants.append(ch)

    elif ch.isupper():
        cap_char.append(ch)
        if ch in is_vowel:
            vowels.append(ch)
        else:
            consonants.append(ch)

    elif ch.isdigit():
        dig.append(ch)

    else:
        symbol.append(ch)

print("\nLower case characters :", small_char)
print("Upper case characters :", cap_char)
print("Digits :", dig)
print("Symbols :", symbol)
print("Vowels :", vowels)
print("Consonants :", consonants)