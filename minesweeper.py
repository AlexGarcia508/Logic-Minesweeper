import itertools
import random

"""
Logic-Minesweeper
"""
"""
CECS 451 Sec 02
Student Names:
Alex Garcia
Chase Calero
Shivkumar Manek
Travis Nguyen
Vincent Tran

Summary:
In this project understanding how the 3 classes utilized by the minesweeper AI worked together
was crucial to making progress. Implementing functions for Sentence class was straightforward,
but implementing functions for minesweeper AI class was a more challenging task specifically add_knowledge.

Step 4 and 5 for the add_knowledge function required a bit more critical thinking compared to any other part.
Step 4 asked us to reference the knowledge database and make applicable changes to cells to either a safe or mine.
However, we took care of that within the functions mark_mine and mark_safe under the class Sentence. We further
looked towards the knowledge base for step 5 in order to add new sentences via inferences from existing knowledge.
We examined every sentence to check for contradictions and redundancies then made the appropriate changes.
"""

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines_known = set()
        self.safes_known = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines_known

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes_known

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.mines_known.add(cell)
        if cell in self.cells:
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.safes_known.add(cell)
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def nearby_cells(self, cell):
        """
        New function added.
        Returns the number of cells that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep set of nearby cells
        surrounding_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update set if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    surrounding_cells.add((i, j))

        return surrounding_cells

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # step 1
        self.moves_made.add(cell)

        #step 2
        self.mark_safe(cell)

        # step 3
        surrounding_cells = self.nearby_cells(cell)

        new_sentence = Sentence(surrounding_cells, count)
        self.knowledge.append(new_sentence)

        # step 4
        # cells and count are the same
        if count == len(surrounding_cells):
            for cell in surrounding_cells:
                self.mark_mine(cell)
        elif count == 0:
            for cell in surrounding_cells:
                self.mark_safe(cell)

        # mark_mine and mark_safe take care of updating rest knowledgebase

        # step 5
        redundant_indices = []
        for i, sentence in enumerate(self.knowledge):
            if sentence.cells.issubset(new_sentence.cells):
                # mine implication of all cells in previous sentence based on new knowledge
                redundant_cells = sentence.cells - new_sentence.cells
                for redundant_cell in redundant_cells:
                    self.mark_safe(redundant_cell)
                redundant_indices.append(i)
            elif new_sentence.cells.issubset(sentence.cells):
                # mine implication of all cells in new sentence based on previous knowledge
                redundant_cells = new_sentence.cells - sentence.cells
                for redundant_cell in redundant_cells:
                    self.mark_safe(redundant_cell)
                redundant_indices.append(i)

        # remove redundancy
        self.knowledge = [self.knowledge[i] for i in range(len(self.knowledge)) if i not in redundant_indices]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        remaining_cells = list(itertools.product(range(self.height), range(self.width)))
        remaining_cells = [cell for cell in remaining_cells if cell not in self.moves_made and cell not in self.mines]

        if remaining_cells:
            return random.choice(remaining_cells)
        else:
            return None
