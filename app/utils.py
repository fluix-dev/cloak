import random

BRAILLE_ALPHABET = "⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⢷⢸⢹⢺⢻⢼⢽⢾⢿⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿"


def gen_braille(chars=8):
    return ''.join(random.choice(BRAILLE_ALPHABET) for _ in range(chars))
