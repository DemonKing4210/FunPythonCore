import random

words = ["apple", "grape", "lemon", "mango", "peach"]
secret = random.choice(words)
attempts = 6

print("Welcome to Wordle! Guess the 5-letter Fruits.")

while attempts > 0:
    guess = input(f"\nAttempt {7 - attempts}/6: ").lower()

    if len(guess) != 5 or not guess.isalpha():
        print("Please enter a valid 5-letter word.")
        continue

    result = ""
    for i in range(5):
        if guess[i] == secret[i]:
            result += f"[{guess[i].upper()}]"  # correct spot
        elif guess[i] in secret:
            result += f"({guess[i]})"  # wrong spot
        else:
            result += f" {guess[i]} "  # not in word

    print("Result:", result)

    if guess == secret:
        print("🎉 You guessed it!")
        break

    attempts -= 1

if guess != secret:
    print("💀 You lost. The word was:", secret)
