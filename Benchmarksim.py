import matplotlib.pyplot as plt
import numpy as np
import random

# Load words from file
with open("words_alpha.txt", "r") as file:
    words = [line.strip() for line in file if len(line.strip()) > 2]  # Only keep words with at least 3 letters

# Dictionary to store letter usefulness
letter_usefulness = {}

# Compute letter usefulness based on middle letter frequency (ignoring first & last letter)
unique_word_sets = set()

for word in words:
    middle_letters = set(word[1:-1])  # Get unique middle letters
    unique_word_sets.add(frozenset(middle_letters))  # Store unique letter sets
    
    for letter in middle_letters:
        letter_usefulness[letter] = letter_usefulness.get(letter, 0) + 1

# Compute "usefulness score" (higher score = better guess)
for letter in letter_usefulness:
    letter_usefulness[letter] /= sum(1 for word_set in unique_word_sets if letter in word_set)

# Sort letters by usefulness score (best letters first)
best_letters = sorted(letter_usefulness.keys(), key=lambda l: letter_usefulness[l], reverse=True)

# Function to play a single round of Hangman (counting WRONG attempts)
def play_hangman(target_word):
    known_letters = set(target_word[0] + target_word[-1])  # Start with first & last letters known
    remaining_words = [word for word in words if len(word) == len(target_word) and word[0] == target_word[0] and word[-1] == target_word[-1]]

    wrong_attempts = 0
    guessed_letters = set()

    while len(remaining_words) > 1:
        # Pick the best letter that hasn't been guessed
        next_guess = next((l for l in best_letters if l not in known_letters and l not in guessed_letters), None)
        if not next_guess:
            break  # No more useful letters to guess (round failed)

        guessed_letters.add(next_guess)

        # If the guessed letter is NOT in the target word, count it as a wrong attempt
        if next_guess not in target_word:
            wrong_attempts += 1

        # Filter words that contain the guessed letter in an unknown position
        remaining_words = [word for word in remaining_words if any(l == next_guess for i, l in enumerate(word) if i not in [0, len(word) - 1])]

        # If the guessed letter is in the target word, reveal it
        if next_guess in target_word:
            known_letters.add(next_guess)

    # If multiple words are still left, the round is a failure
    if len(remaining_words) > 1:
        return wrong_attempts, target_word  # Failed to guess
    return wrong_attempts, None  # Successfully guessed

# Run the simulation
wrong_attempts_per_round = []
failed_words = []
rounds_above_6 = 0
num_rounds = 1000  # Number of words to test
random.shuffle(words)
test_words = words[:num_rounds]

for i, word in enumerate(test_words):
    wrong_attempts, failed_word = play_hangman(word)
    wrong_attempts_per_round.append(wrong_attempts)
    
    if wrong_attempts > 5:
        rounds_above_6 += 1
    if failed_word:
        failed_words.append(failed_word)  # Store failed words

# Calculate percentage of rounds with more than 6 wrong tries
percentage_above_6 = (rounds_above_6 / num_rounds) * 100

# Plotting the results
fig, ax = plt.subplots(figsize=(14, 7))
x_indexes = np.arange(len(wrong_attempts_per_round))
ax.bar(x_indexes, wrong_attempts_per_round, color='blue', label="Wrong Attempts per round")

# Plot the average line
avg_wrong_attempts = np.mean(wrong_attempts_per_round)
ax.axhline(avg_wrong_attempts, color='red', linestyle='dashed', label=f"Avg Wrong Attempts: {avg_wrong_attempts:.2f}")

# Plot the threshold line
ax.axhline(6, color='green', linestyle='dashed', label=f"Threshold: 6 Wrong Attempts")
ax.text(len(wrong_attempts_per_round) - 1, 6, f"{percentage_above_6:.2f}%", color='green', verticalalignment='bottom')

# Labels and title
ax.set_xlabel("Round Number")
ax.set_ylabel("Wrong Attempts")
ax.set_title(f"Hangman Bot Simulation: Wrong Attempts per Round")
ax.legend()

# Display failed words under the graph
if failed_words:
    failed_text = "Failed Words: " + ", ".join(failed_words)
    ax.text(0.5, -0.3, failed_text, ha='center', va='top', fontsize=10, color='red', 
            transform=ax.transAxes, wrap=True)

# Show plot
plt.show()
