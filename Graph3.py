import matplotlib.pyplot as plt
import numpy as np

# Dictionary to store letter usefulness
letter_usefulness = {}

# Read words from file
with open("words_alpha.txt", "r") as file:
    unique_word_sets = set()  # Store unique middle-letter sets for uniqueness scoring

    for word in file:
        word = word.strip()  # Remove trailing newline
        
        if len(word) > 2:  # Ensure word has at least 3 letters
            middle_letters = set(word[1:-1])  # Get unique letters excluding first & last
            
            unique_word_sets.add(frozenset(middle_letters))  # Track unique letter combinations
            
            for letter in middle_letters:
                letter_usefulness[letter] = letter_usefulness.get(letter, 0) + 1

# Compute "usefulness score" by considering how uniquely letters help filter words
for letter in letter_usefulness:
    letter_usefulness[letter] /= sum(1 for word_set in unique_word_sets if letter in word_set)

# Sort letters by usefulness score
sorted_letters = sorted(letter_usefulness.keys(), key=lambda l: letter_usefulness[l], reverse=True)
letter_scores = [letter_usefulness[l] for l in sorted_letters]

# Setup figure
fig, ax = plt.subplots(figsize=(12, 6))

# Bar chart
x_indexes = np.arange(len(sorted_letters))
ax.bar(x_indexes, letter_scores, color='blue')

# Labels and title
ax.set_xlabel('Letter')
ax.set_ylabel('Usefulness Score')
ax.set_title('Best Letters to Guess in Hangman (Middle Letters Only)')
ax.set_xticks(x_indexes)
ax.set_xticklabels(sorted_letters)

# Show plot
plt.show()
