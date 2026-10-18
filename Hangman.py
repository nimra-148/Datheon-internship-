import random

WORDS = ["PYTHON", "CONSOLE", "PROGRAM", "COMPUTER", "KEYBOARD", "DATHEON", "ALGORITHM"]

HANGMAN_PICS = [
"""
     +---+
     |   |
         |
         |
         |
         |

""",
"""
     +---+
     |   |
     O   |
         |
         |
         |

""",
"""
     +---+
     |   |
     O   |
     |   |
         |
         |

""",
"""
     +---+
     |   |
     O   |
    /|   |
         |
         |

""",
"""
     +---+
     |   |
     O   |
    /|\\  |
         |
         |

""",
"""
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |

""",
"""
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |

"""
]

def get_masked_word(secret_word, guessed_letters):
    displayed = []
    for letter in secret_word:
        if letter in guessed_letters:
            displayed.append(letter)
        else:
            displayed.append("_")
    return " ".join(displayed)

def play():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    mistakes = 0
    max_mistakes = 6

    print("=== HANGMAN GAME ===")
    print("Guess the word! You have 6 lives.")

    while True:
        print(HANGMAN_PICS[mistakes])
        masked = get_masked_word(secret_word, guessed_letters)
        print(f"\nWord: {masked}")
        print(f"Guessed: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Mistakes: {mistakes}/{max_mistakes}")

        if "_" not in masked.replace(" ", ""):
            print("\n" + "="*30)
            print(f"VICTORY! Word was: {secret_word}")
            print("="*30)
            break

        if mistakes >= max_mistakes:
            print(HANGMAN_PICS[mistakes])
            print("\n" + "="*30)
            print(f"DEFEAT! Word was: {secret_word}")
            print("="*30)
            break

        guess = input("\nEnter a letter: ").strip().upper()

        if not guess.isalpha() or len(guess) != 1:
            print("Please enter a single letter!")
            continue
        if guess in guessed_letters:
            print("Already guessed!")
            continue

        guessed_letters.add(guess)

        if guess not in secret_word:
            mistakes += 1
            print(f"Wrong! '{guess}' not in word.")

if __name__ == "__main__":
    play()
