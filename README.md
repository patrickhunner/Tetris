## Project Description

This is a playable tetris clone developed with pygame. It follows the original BPS scoring/leveling system but with the added features of being able to see 3 pieces ahead and saving pieces.

## How to Run:

### Cloning

Here is an overview of how to run the project (Prerequisite is that you have installed [Python3](https://www.python.org/downloads/):

    ```bash
    # Go to the project directory
    cd /path/to/repo/project
    
    # Clone the repository
    git clone https://github.com/patrickhunner/Tetris
    
    # Run the project (./build/web-app <port> <web folder>)
    python3 tetris.py
    ```
  
## Bugs

Currently, due to poor initial design, the game will not end when you have lost but rather crash due to an overload of pieces being created. This problem would be a way to contribute to the project or I will hopefully come back around and fix it soon.
