import matplotlib.pyplot as plt
import numpy as np

# Dictionary to store letter frequencies
letter_count = {}

# Read words from file
with open("words_alpha.txt", "r") as file:
    for word in file:
        word = word.strip()  # Remove trailing newline
        
        if len(word) > 2:  # Ensure word has at least 3 letters
            inner_letters = set(word[1:-1])  # Get unique letters excluding first & last
            
            for letter in inner_letters:
                letter_count[letter] = letter_count.get(letter, 0) + 1

# Sort by frequency
sorted_letters = sorted(letter_count.keys(), key=lambda l: letter_count[l], reverse=True)
letter_freq = [letter_count[l] for l in sorted_letters]

# Setup figure
fig, ax = plt.subplots(figsize=(12, 6))

# Bar chart
x_indexes = np.arange(len(sorted_letters))
ax.bar(x_indexes, letter_freq, color='blue')

# Labels and title
ax.set_xlabel('Letter')
ax.set_ylabel('Frequency')
ax.set_title('Letter Frequency (Excluding First and Last Letters of Words)')
ax.set_xticks(x_indexes)
ax.set_xticklabels(sorted_letters)

# Show plot
plt.show()
