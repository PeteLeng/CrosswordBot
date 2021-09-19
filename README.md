# The Crossword Bot
A tool for generating crosswords.

# Demonstration
<img src="https://user-images.githubusercontent.com/77133684/133922297-784bc166-5734-4452-bd49-ffa0d4d030b9.png" alt="alt text" width="500" height="500">

# User manual
- Input words into the text box on the left.
- Click the "Assemble the words" button to generate the crossword.
- Crossword will be displayed in the grid on the right.
- Adjust the size of the grid using the "+" or "-" button on the top control menu.
- Switch between different patterns using "NEXT" or "PREV" button in the control menu.
- Click the "VIEW" button to previw the crossword with all the letters blanked out.
- Click save to generate a pdf file of the crossword.

# Implementations
- Random selection sorting.
The idea of frequency score is introduced to sort the list of words using randomized selection.
In order to maximize the words unsed in the crossword while introducing a degree of randomness.
- DFS search
The crossword problem is inherently exponential, a DFS generator is implemented to save runtime while and preverse the variaties of patterns.

# Dependency
No extra packages except python and numpy

# Testing
- Generate a text file of 10 random words using "rand_words.py".
- Run "app.py" in packages.
- Follow the user manual.
