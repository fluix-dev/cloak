import random

BRAILLE_ALPHABET = "⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⢷⢸⢹⢺⢻⢼⢽⢾⢿⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿"


def gen_braille(chars=6):
    return ''.join(random.choice(BRAILLE_ALPHABET) for _ in range(chars))
