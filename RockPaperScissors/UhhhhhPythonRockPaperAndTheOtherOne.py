import random

# Get player input
user_action = input("Enter a choice (rock, paper, scissors): ").lower()

# Define possible actions for the computer
possible_actions = ["rock", "paper", "scissors"]

# Computer makes a random choice
computer_action = random.choice(possible_actions)

print("You chose **{user_action}**, computer chose **{computer_action}**")

# Determine the winner
if user_action == computer_action:
    print("Both players selected {user_action}. It's a **tie**!")
elif user_action == "rock":
    if computer_action == "scissors":
        print("Rock smashes scissors! You **win**!")
    else:
        print("Paper covers rock! You **lose**.")
elif user_action == "paper":
    if computer_action == "rock":
        print("Paper covers rock! You **win**!")
    else:
        print("Scissors cuts paper! You **lose**.")
elif user_action == "scissors":
    if computer_action == "paper":
        print("Scissors cuts paper! You **win**!")
    else:
        print("Rock smashes scissors! You **lose**.")
else:
    print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")
