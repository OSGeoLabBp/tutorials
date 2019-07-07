arabic = {'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400,
          'CM': 900, 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,
          'D': 500, 'M': 1000}
keys = list(arabic.keys())
#keys = ('IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'I', 'V', 'X', 'L', 'C', 'D', 'M')
roman = sorted(list(zip(arabic.values(), arabic.keys())))[::-1]
#roman = ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
#         (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
#         (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))

def toroman(n):
    """ convert integer to its roman equivalent e.g. 456 -> CDLVI
    """
    result = ""
    for item in roman:
        while n >= item[0]:
            result += item[1]
            n -= item[0]
    return result

def toint(s):
    """ Convert roman number to int """
    result = 0
    s = s.upper()
    for key in keys:
        while key in s:
            result += arabic[key]
            s = s.replace(key, "", 1)
    return result

print(toroman(456))
print(toint('CDLVI'))
