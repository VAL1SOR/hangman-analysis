import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
import plotly.express as px
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D

# Load words from file
with open("words_alpha.txt", "r") as file:
    words = [line.strip() for line in file if len(line.strip()) > 2]  # Keep words with at least 3 letters

# Group words by (first, last, length) combination
word_groups = defaultdict(list)
for word in words:
    word_groups[(word[0], word[-1], len(word))].append(word)

# Precompute letter usefulness for each (first, last, length) group
letter_usefulness_cache = {}

def compute_letter_usefulness(word_list):
    if not word_list:
        return []
    
    key = tuple(sorted(word_list))
    if key in letter_usefulness_cache:
        return letter_usefulness_cache[key]
    
    letter_usefulness = {}
    unique_word_sets = set()
    
    for word in word_list:
        middle_letters = set(word[1:-1])  # Get unique middle letters
        unique_word_sets.add(frozenset(middle_letters))  # Store unique letter sets
        
        for letter in middle_letters:
            letter_usefulness[letter] = letter_usefulness.get(letter, 0) + 1

    # Compute "usefulness score" (higher score = better guess)
    for letter in letter_usefulness:
        letter_usefulness[letter] /= sum(1 for word_set in unique_word_sets if letter in word_set)

    best_letters = sorted(letter_usefulness, key=letter_usefulness.get, reverse=True)
    letter_usefulness_cache[key] = best_letters
    return best_letters

# Function to play Hangman for a given target word, respecting (first, last, length) group
def play_hangman(target_word, word_list):
    best_letters = compute_letter_usefulness(word_list)
    known_letters = set(target_word[0] + target_word[-1])
    remaining_words = set(word_list)

    wrong_attempts = 0
    guessed_letters = set()

    while len(remaining_words) > 1:
        if not best_letters:
            break
        
        # Choose letter with highest elimination power
        letter_scores = {l: sum(1 for w in remaining_words if l in w) for l in best_letters if l not in known_letters and l not in guessed_letters}
        if not letter_scores:
            break
        next_guess = min(letter_scores, key=letter_scores.get)  # Minimize words remaining
        
        guessed_letters.add(next_guess)
        if next_guess not in target_word:
            wrong_attempts += 1
        
        remaining_words = {word for word in remaining_words if next_guess in word[1:-1]}
        if next_guess in target_word:
            known_letters.add(next_guess)

    if wrong_attempts > 5:
        return wrong_attempts, target_word  # Failed to guess
    return wrong_attempts, None  # Successfully guessed

# Run normal simulation but respect (first, last, length) group
wrong_attempts_per_round = []
failed_words = []
num_rounds = 1000
random.shuffle(words)
test_words = words[:num_rounds]
heatmap_data = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

for word in test_words:
    word_list = word_groups.get((word[0], word[-1], len(word)), [])
    if not word_list:
        continue  # Skip if no words exist for this group
    
    wrong_attempts, failed_word = play_hangman(word, word_list)
    wrong_attempts_per_round.append(wrong_attempts)
    if failed_word:
        failed_words.append(failed_word)
    
    heatmap_data[word[0]][word[-1]][len(word)] += wrong_attempts / len(word_list)

# Save failed words to file
with open("failed.txt", "w") as file:
    for word in failed_words:
        file.write(word + "\n")

print(f"Failed words saved to failed.txt ({len(failed_words)} words).")

# Generate 3D heatmap data
alphabet = list("abcdefghijklmnopqrstuvwxyz")
word_lengths = sorted(set(len(word) for word in words))

data_points = []
for start, end_dict in heatmap_data.items():
    for end, length_dict in end_dict.items():
        for length, avg in length_dict.items():
            data_points.append([start, end, length, avg])

df = np.array(data_points, dtype=object)
fig = px.scatter_3d(
    x=df[:, 0], y=df[:, 1], z=df[:, 2], color=df[:, 3],
    labels={"x": "Starting Letter", "y": "Ending Letter", "z": "Word Length", "color": "Avg Wrong Attempts"},
    title="Average Wrong Attempts per (Start, End, Length) Combination",
    color_continuous_scale="coolwarm"
)
fig.show()

# Plotting the results for wrong attempts per round
fig, ax = plt.subplots(figsize=(14, 7))
x_indexes = np.arange(len(wrong_attempts_per_round))
ax.bar(x_indexes, wrong_attempts_per_round, color='blue', label="Wrong Attempts per round")

# Plot the average line
avg_wrong_attempts = np.mean(wrong_attempts_per_round)
ax.axhline(avg_wrong_attempts, color='red', linestyle='dashed', label=f"Avg Wrong Attempts: {avg_wrong_attempts:.2f}")

# Plot the threshold line
ax.axhline(6, color='green', linestyle='dashed', label=f"Threshold: 6 Wrong Attempts")

# Labels and title
ax.set_xlabel("Round Number")
ax.set_ylabel("Wrong Attempts")
ax.set_title(f"Hangman Bot Simulation: Wrong Attempts per Round (Respecting First & Last Letter Pair & Length)")
ax.legend()

# Show plot
plt.show()
