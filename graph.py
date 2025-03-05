import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Dictionaries for letter frequencies
total_count = {}   # Counts every occurrence
unique_count = {}  # Counts only once per word

# Read words from file
with open("words_alpha.txt", "r") as file:
    for word in file:
        word = word.strip()  # Remove trailing newline
        seen_letters = set()  # Track letters in this word
        
        for letter in word:
            # Total count (every occurrence)
            total_count[letter] = total_count.get(letter, 0) + 1
            
            # Unique count (only once per word)
            if letter not in seen_letters:
                unique_count[letter] = unique_count.get(letter, 0) + 1
                seen_letters.add(letter)

# Compute average count
average_count = {l: (total_count[l] + unique_count.get(l, 0)) / 2 for l in total_count}

# Initial sorting (by total occurrences)
sorted_letters = sorted(total_count.keys(), key=lambda l: total_count[l], reverse=True)
total_freq = [total_count[l] for l in sorted_letters]
unique_freq = [unique_count.get(l, 0) for l in sorted_letters]
average_freq = [average_count.get(l, 0) for l in sorted_letters]

# Setup figure
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)  # Make space for button

# Bar width
bar_width = 0.3
x_indexes = np.arange(len(sorted_letters))

# Plot bars
bar1 = ax.bar(x_indexes - bar_width, total_freq, bar_width, color='skyblue', label='Total Count')
bar2 = ax.bar(x_indexes, unique_freq, bar_width, color='orange', label='Unique Word Count')
bar3 = ax.bar(x_indexes + bar_width, average_freq, bar_width, color='green', label='Average Count')

# Labels and title
ax.set_xlabel('Letter')
ax.set_ylabel('Frequency')
ax.set_title('Letter Frequency (Sorted by Total Count)')
ax.set_xticks(x_indexes)
ax.set_xticklabels(sorted_letters)
ax.legend()

# Sorting modes: 0 = Total, 1 = Unique, 2 = Average
sort_mode = 0  
sort_labels = ['Total', 'Unique', 'Average']

# Update function for button click
def update_sort(event):
    global sort_mode

    if sort_mode == 0:
        sorted_letters = sorted(unique_count.keys(), key=lambda l: unique_count[l], reverse=True)
        ax.set_title('Letter Frequency (Sorted by Unique Word Count)')
    elif sort_mode == 1:
        sorted_letters = sorted(average_count.keys(), key=lambda l: average_count[l], reverse=True)
        ax.set_title('Letter Frequency (Sorted by Average Count)')
    else:
        sorted_letters = sorted(total_count.keys(), key=lambda l: total_count[l], reverse=True)
        ax.set_title('Letter Frequency (Sorted by Total Count)')

    total_freq = [total_count.get(l, 0) for l in sorted_letters]
    unique_freq = [unique_count.get(l, 0) for l in sorted_letters]
    average_freq = [average_count.get(l, 0) for l in sorted_letters]

    x_indexes = np.arange(len(sorted_letters))
    ax.set_xticks(x_indexes)
    ax.set_xticklabels(sorted_letters)

    # Update bar heights
    for bar, new_h in zip(bar1, total_freq):
        bar.set_height(new_h)
    for bar, new_h in zip(bar2, unique_freq):
        bar.set_height(new_h)
    for bar, new_h in zip(bar3, average_freq):
        bar.set_height(new_h)
    
    fig.canvas.draw_idle()
    sort_mode = (sort_mode + 1) % 3  # Cycle between 0 (Total), 1 (Unique), 2 (Average)
    button.label.set_text(f'Sort by {sort_labels[sort_mode]}')

# Add button
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])  # [x, y, width, height]
button = Button(ax_button, 'Sort by Unique')
button.on_clicked(update_sort)

plt.show()
