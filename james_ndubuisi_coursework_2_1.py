# -*- coding: utf-8 -*-
"""James Ndubuisi Coursework 2.1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fcGkOhpn7nnkU8f4RQSkmQUFfjvHWGn4
"""



"""# F29AI Coursework 2.1

**Deadline:** on Friday, 30th Nov 2023

**How to Submit:** To be submitted via Canvas – Submission are timestamped: all submission after the deadline will be considered late


## **Very important information (Do not miss any points)**:
1. You can NOT edit this file, copy it to your own google collab account and edit it there.
2. Your work have to be submitted in **Canvas** with a link to your google collab, otherwise your work won't be marked. Directly emailing to lecturer will NEVER work.
3. Read carefully the instruction before each section, if you missed some tasks, you may lose marks. For example, if you are required to print some contents, please JUST print what asked.
4. It is highly recoommended that you ONLY filled the functions or code blocks highlighted with the comments "-- your code here --", which is the easiest way to complete all tasks. However, as long as all the tasks are completed, you are fine.
5. Your whole notebook will be tested using the "Runtime->Run all" option. No one will run each cell one after another. Make sure your notebook can be executed by one click. Only the results generated by the "Runtime->Run all" action.
6. You MUST fill the following information, otherwise your work won't be marked.
7. Only do one version of this coursework, if you submit a Java version too, we will ignore your Python version.
8. The tasks you need to complete will be shown in <font color="blue"> Blue </font>, with marks attached to it. Do not miss them.
9. You are allowed, actually encouraged to use ChatGPT for the tasks of <font color="blue"> Value Interation ONLY </font>, but allowed to use that too for QLearn. In this case, you must share the FULL conversation with ChatGPT by paste the link in the following form. One example is this [link](https://chat.openai.com/share/4f4c94ea-ca6a-47de-a4ae-5cc285b85d7d). If you use other LLMs, paste the screenshots of your conversation by inserting a new text cell below (before the "task" section).
10. Do NOT generate the code using ChatGPT for policy iteration and q-learn. Once discovered, your marks for this two parts will be gone.
11. This is an <font color="red"> INDIVIDUAL </font> work, any submissions that are similar enough will be considered as IP case.

<font color="red"> Any questions about the above information, or about DEBUG process won't be answered by default!

Remember: this python version of coursework won't have other official support.</font>

---
---
"""



"""## Your Information"""

#@title Student Information
First_name = "James" #@param {type:"string"}
Family_name = "Ndubuisi " #@param {type:"string"}
University_email = "jn2033@hw.ac.uk" #@param {type:"string"}
Student_no = "H00379625" #@param {type:"string"}

#@markdown - If you used ChatGPT for Value Iteration tasks share your conversation link below (optional).
GPT_conversation_link = "" #@param {type:"string"}

print(GPT_conversation_link)

"""---
---

## **Tasks**
* In this coursework, you will implement Value Iteration, Policy Iteration that plan/learn to play 3x3 Tic-Tac-Toe game. You will test your agents against other rule-based agents that are provided. You can also play against all the agents including your own agents to test them.
* A general framework for the game and agents is provided. Run each code cell below in order, when you see a <>

### Part 0: Environment: packages, constants, basic code
"""

import os

import numpy as np
import pickle
from abc import ABC, abstractmethod

# Constants for the game
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
GAME_ROW, GAME_COL = 3, 3

"""#### 0.1: The ***Game*** class:

play(): simulate one game

*show_board* indicate whether the states are printed during play
"""

class Game:
    """
    Define the tictactoe game. The function and variable names should be self explained.

    @author: chenxy
    """
    def __init__(self, player_x, player_o, show_board=False):
        self.board = np.zeros((GAME_ROW, GAME_COL), dtype=int)
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = self.player_x
        self.winner = None
        self.show_board = show_board
        self.turn = 0

    def get_empty_positions(self):
        return [(i, j) for i in range(GAME_ROW) for j in range(GAME_COL) if self.board[i, j] == EMPTY]

    def is_winner(self, player):
        symbol = player.symbol
        for i in range(GAME_ROW):
            if np.all(self.board[i, :] == symbol) or np.all(self.board[:, i] == symbol):
                return True
        if np.all(np.diag(self.board) == symbol) or np.all(np.diag(np.fliplr(self.board)) == symbol):
            return True
        return False

    def is_draw(self):
        return np.all(self.board != EMPTY)

    def make_move(self, position):
        if self.board[position] != EMPTY:
            # Don't raise an exception, just return indicating an invalid move
            return False
        self.board[position] = self.current_player.symbol
        return True

    def switch_player(self):
        self.current_player = self.player_x if self.current_player == self.player_o else self.player_o

    def get_hash(self, board=None):
        if board is None:
            board = self.board
        return ','.join(str(int(elem)) for elem in board.flatten())

    def reset(self):
        self.__init__(self.player_x, self.player_o, self.show_board)

    def is_terminal(self):
        # Check for a win in rows, columns, and diagonals
        for i in range(GAME_ROW):
            if np.all(self.board[i] == self.current_player.symbol) or \
               np.all(self.board[:, i] == self.current_player.symbol):
                return True
        if np.all(np.diag(self.board) == self.current_player.symbol) or \
           np.all(np.diag(np.fliplr(self.board)) == self.current_player.symbol):
            return True
        # Check for a draw (no empty positions left)
        if not np.any(self.board == EMPTY):
            return True
        return False

    def play(self):
        self.reset()
        while True:
          position = self.current_player.move(self)
          if not self.make_move(position):  # If move is invalid, skip to next turn
            raise Exception("Something is wrong! No empty positions now!")
          self.turn+=1

          if self.is_terminal():
              if self.is_winner(self.current_player):
                  self.winner = self.current_player.symbol
                  print(f"Player {self.current_player.symbol} wins!")
                  break  # Exit the loop immediately after a win

              if self.is_draw():
                  print("It's a draw!")
                  break  # Exit the loop immediately after a draw

          if self.show_board:
              print(f"Turn {self.turn}: Player {self.current_player.symbol}")
              self.print_board()

          self.switch_player()

        if self.show_board:
            self.print_board()  # Show the final board state

    def print_board(self):
        symbols = {EMPTY: ' ', PLAYER_X: 'X', PLAYER_O: 'O'}
        for i in range(GAME_ROW):
            print('|' + '|'.join(symbols[s] for s in self.board[i]) + '|')
        print()

"""#### 0.2 Agent abstract class, all *agents* class inherit this one.
* *RandomAgent*: perform random action
* *AggressiveAgent*: choose the winning action
* *DefensiveAgent*: stop opponent's winning action
"""

class Agent(ABC):
    def __init__(self, symbol):
        self.symbol = symbol
        self.states_value = {}  # State values used by ValueIterationAgent

    @abstractmethod
    def move(self, game):
        pass

    def save_policy(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.states_value, f)

    def load_policy(self, file_name):
        with open(file_name, 'rb') as f:
            self.states_value = pickle.load(f)

class RandomAgent(Agent):
    def move(self, game):
        empty_cells = game.get_empty_positions()
        if not empty_cells:
            raise ValueError("No more moves left to play.")
        # Select a random move from the list of empty cells
        return empty_cells[np.random.randint(len(empty_cells))]

class AggressiveAgent(Agent):
    def __init__(self, symbol):
        super().__init__(symbol)

    def move(self, game):
        empty_positions = game.get_empty_positions()
        board_copy = game.board.copy()
        for position in empty_positions:
            board_copy[position] = self.symbol
            if game.is_winner(self):
                return position
            board_copy[position] = EMPTY  # Reset the position after check

        # If no winning move found, return a random move
        return empty_positions[np.random.choice(len(empty_positions))]

class DefensiveAgent(Agent):
    def __init__(self, symbol):
        super().__init__(symbol)

    def move(self, game):
        opponent_symbol = PLAYER_O if self.symbol == PLAYER_X else PLAYER_X
        empty_positions = game.get_empty_positions()
        board_copy = game.board.copy()

        # First, check if the opponent has a winning move and block it
        for position in empty_positions:
            board_copy[position] = opponent_symbol
            if game.is_winner(self.__opponent()):
                return position  # Block the opponent's winning move
            board_copy[position] = EMPTY  # Reset the position after check

        # If no blocking move is necessary, choose a random move
        return empty_positions[np.random.choice(len(empty_positions))]

    def __opponent(self):
        # Private helper method to create a 'dummy' opponent with the opposite symbol
        return RandomAgent(PLAYER_O if self.symbol == PLAYER_X else PLAYER_X)

"""#### 0.3: Useful and example functions:
Some may never been called
"""

def get_hash(board=None):
    return ','.join(str(int(elem)) for elem in board.flatten())


def get_hashes(boards):
    return [get_hash(board) for board in boards]

def valid_state(board, symbol):

    # check the board state is valid
    if symbol==PLAYER_X:
        return (np.sum(board==PLAYER_X)==np.sum(board==PLAYER_O))
    if symbol==PLAYER_O:
        return (np.sum(board==PLAYER_X)-np.sum(board==PLAYER_O)==1)

def next_symbol(board):
    if (np.sum(board==PLAYER_X)==np.sum(board==PLAYER_O)):
        return PLAYER_X
    else:
        return PLAYER_O

def is_terminal(board):
    # Check for a win in rows, columns, and diagonals
    for i in range(GAME_ROW):
        if abs(np.sum(board[i, :])) == 3 or abs(np.sum(board[:, i])) == 3:
            return True
    if abs(sum(np.diag(board))) == 3 or abs(sum(np.diag(np.fliplr(board)))) == 3:
        return True
    # Check for a draw
    if not np.any(board == EMPTY):
        return True
    return False

def get_reward(board, symbol):
    # Define opponent's symbol
    opponent_symbol = PLAYER_O if symbol == PLAYER_X else PLAYER_X

    # Check for current player's win
    for i in range(GAME_ROW):
        if sum(board[i, :]) == GAME_ROW * symbol or sum(board[:, i]) == GAME_COL * symbol:
            return 1
    if sum(np.diag(board)) == GAME_ROW * symbol or sum(np.diag(np.fliplr(board))) == GAME_COL * symbol:
        return 1

    # Check for opponent's win
    for i in range(GAME_ROW):
        if sum(board[i, :]) == GAME_ROW * opponent_symbol or sum(board[:, i]) == GAME_COL * opponent_symbol:
            return -1
    if sum(np.diag(board)) == GAME_ROW * opponent_symbol or sum(np.diag(np.fliplr(board))) == GAME_COL * opponent_symbol:
        return -1

    # Check for a draw
    if is_terminal(board):
        return 0

    # For non-terminal states, the immediate reward is 0.
    return 0


def get_empty_positions(board):
    return [(i, j) for i in range(GAME_ROW) for j in range(GAME_COL) if board[i, j] == EMPTY]

def generate_next_boardstates(board, symbol):

    # check the board state is valid
    if symbol==PLAYER_X:
        assert(np.sum(board==PLAYER_X)==np.sum(board==PLAYER_O))
    if symbol==PLAYER_O:
        assert(np.sum(board==PLAYER_X)-np.sum(board==PLAYER_O)==1)

    # generate all next board states
    all_empty_positions = get_empty_positions(board)
    all_boards = np.tile(board, (len(all_empty_positions), 1, 1))
    all_indices = np.concatenate(
        [
            np.expand_dims(np.arange(len(all_empty_positions)), axis=1),
            np.array(all_empty_positions)
        ], axis=1
        )
    all_boards[all_indices[:,0], all_indices[:,1], all_indices[:,2]] = symbol
    all_boards = np.split(all_boards, all_boards.shape[0], axis=0)
    return [np.squeeze(board) for board in all_boards]

def generate_all_states(board, all_states=None, stop_step=None):

    # assert(valid_state(board, symbol)) # validate the states and symbol

    if all_states is None:
        # all_states = {}
        boards = [board]
        state_hashes = [get_hash(board)]
        p0 = 0
        p1 = 1
        p2 = p1
        step = 0
        step_symbol = next_symbol(board)

    while p0!=p1:
      for p_state in range(p0,p1):
          # print(step)
          # print('p_state:', p_state)
          # print('board:', boards[p_state])
          # print('step_symbol:', step_symbol)
          # print(p1-p0)
          # print('------------------------')
          if is_terminal(boards[p_state]):
              continue
          next_boards = generate_next_boardstates(boards[p_state], step_symbol)
          next_hashes = get_hashes(next_boards)

          # print(next_boards)

          boards+=next_boards
          state_hashes+=next_hashes
          p2 += len(next_boards)

      step_symbol = PLAYER_X if step_symbol == PLAYER_O else PLAYER_O
      p0 = p1
      p1 = p2
      step+=1

      if stop_step is not None:
        if step == stop_step:
          break
    return dict(zip(state_hashes, boards))

"""#### 0.4: Fenerate all states using the function **generate_all_states** and save the states hush table in the local path for the future use."""

state_hush_fname = "all_states_hush1.txt"
if os.path.isfile(state_hush_fname):
    with open(state_hush_fname, 'rb') as f:
        all_states = pickle.load(f)

else:
  temp_board = np.zeros((GAME_ROW, GAME_COL))
  all_states = generate_all_states(temp_board)

  # same hush table of all the states
  with open(state_hush_fname, 'wb') as f:
      pickle.dump(all_states, f)

print("In total, ", len(all_states), "states")

"""---
---

### <font color="blue"> **Task 1 (7 marks)**:</font> Value Iteration

#### <font color="blue"> **Question 1:** </font> Write a value iteration agent in ValueIterationAgent which has been partially specified for you. Here you need to implement the train() & get_reward() methods. The former should perform **planning* using *value iteration and the latter should extract the policy and compute state values.
"""

class ValueIterationAgent(Agent):
    def __init__(self, symbol, discount_factor=0.9, living_reward=-0.01):
        super().__init__(symbol)
        if 'all_states' in globals():
            self.all_states = all_states
        elif os.path.isfile(state_hush_fname):
            with open(state_hush_fname, 'rb') as f:
                self.all_states = pickle.load(f)
        else:
            raise Exception("No state hushes! Either run the code by order or create the state hush yourself")

        self.discount_factor = discount_factor  # Discount factor for future rewards
        self.living_reward = living_reward  # Reward for living (negative for penalty)
        self.value_function = {state: 0 for state in all_states.keys()}  # Initialize state values to 0

        # self.all_states = all_states  # All possible states
        self.win_reward=10.0;
        self.lose_reward=-50.0;
        self.living_reward=-1.00;
        self.draw_reward=0.0;

        self.policy = {}  # Initialize policy

    def get_reward(self, board, symbol):
        # Define opponent's symbol
        opponent_symbol = PLAYER_O if symbol == PLAYER_X else PLAYER_X

        # Check for current player's win
        for i in range(GAME_ROW):
            if sum(board[i, :]) == GAME_ROW * symbol or sum(board[:, i]) == GAME_COL * symbol:
                return self.win_reward
        if sum(np.diag(board)) == GAME_ROW * symbol or sum(np.diag(np.fliplr(board))) == GAME_COL * symbol:
            return self.win_reward

        # Check for opponent's win
        # -- Your Code Here ---

        # Check for a draw
        # -- Your Code Here --

        # For non-terminal states, the immediate reward is 0.
        return 0

    def train(self, threshold=0.00001):
        # Value iteration algorithm
        # -- Your Code Here--

    def move(self, game):
        # Return the move based on the current policy
        current_state = game.get_hash()
        if current_state in self.policy:
            return self.policy[current_state]
        else:
            # In case current state is not in the policy, choose a random move
            empty_positions = game.get_empty_positions()
            return empty_positions[np.random.choice(len(empty_positions))]

"""#### <font color="blue">Q1.1 (3/7): Run the following example of a Value Iteration "X" player against a Random "O" agent </font>



"""

player_x = ValueIterationAgent(PLAYER_X)  # This is the value iteration agent
player_o = RandomAgent(PLAYER_O)  # This is the random agent

game = Game(player_x, player_o)
# print(game.board)

# Compute the policy using value iteration only for the value iteration agent
player_x.train()  # We only need to compute this for player O

# Play the game

game.play()

"""#### <font color="blue"> Q1.2 (3/7): Based on the example (Game 0: RandomAgent "O" v.s. ValueIterationAgent "X") above, run the following game: </font>
* Game1: RandomAgent "X" v.s. ValueIterationAgent "O"
* Game2: ValueIterationAgent "X" v.s. AggressiveAgent "O"
* Game3: ValueIterationAgent "O" v.s. AggressiveAgent "X"
* Game4: ValueIterationAgent "X" v.s. DefensiveAgent "O"
* Game 5: ValueIterationAgent "O" v.s. DefensiveAgent "X"

Use the one single code cell *below*
"""

# Game 1:

# Game 2:

# Game 3:

# Game 4:

# Game 5:

"""#### <font color="blue"> Q1.3 (1/7): Repeat the games (Game 0-5) above 50 rounds each Game. Using ValueIterationAgent, print out number of *wins*, *losts* and *draw* </font>"""

# Q1.2 1-5:

game.show_board = False # Disable printing board, don't change

# -- Your Code Here ---

"""---
---

### <font color="blue"> **Task 2** (7 marks):</font>  Policy Iteration

Write a Policy Iteration agent in PolicyIterationAgent by implementing the policy_evaluation(), policy_improvement(), train() methods. The policy_evaluation() method should evaluate the current policy (see your lecture notes). The current values for the current policy should be stored in the provided policyValues map. The policy_improvement() method performs the Policy improvement step, and updates curPolicy. The train() method is the planning process, once done, an optimal policy should be saved in the agent object.
"""

import random

class PolicyIterationAgent(Agent):
    def __init__(self, symbol, discount_factor=0.9, living_reward=-0.01):
        super().__init__(symbol)

        if 'all_states' in globals():
            self.all_states = all_states
        elif os.path.isfile(state_hush_fname):
            with open(state_hush_fname, 'rb') as f:
                self.all_states = pickle.load(f)
        else:
            raise Exception("No state hushes! Either run the code by order or create the state hush yourself")

        self.discount_factor = discount_factor  # Discount factor for future rewards
        self.living_reward = living_reward  # Reward for living (negative for penalty)
        self.value_function = {state: 0 for state in all_states.keys()}  # Initialize state values to 0

        # self.all_states = all_states  # All possible states
        self.win_reward=10.0;
        self.lose_reward=-50.0;
        self.living_reward=-1.00;
        self.draw_reward=0.0;

        self.all_states = all_states  # All possible states
        self.discount_factor = discount_factor  # Discount factor for future rewards
        # self.living_reward = living_reward  # Living reward (negative for penalty)
        self.value_function = {state: 0 for state in all_states.keys()}  # Initialize state values to 0
        # self.policy = {state: np.random.choice(get_empty_positions(board))
        #                for state, board in all_states.items() if not is_terminal(board)}  # Random initial policy
        # # Choosing a random tuple from the list of empty positions
        self.policy = {state: random.choice(get_empty_positions(board))
                   for state, board in all_states.items() if not is_terminal(board)}  # Random initial policy

    def get_reward(self, board, symbol):
        # -- Your Code Here ---
        pass

    def policy_evaluation(self, threshold=0.0001):
        # -- Your Code Here ---
        pass

    def policy_improvement(self):
        # -- Your Code Here --

        pass

    def train(self):
        while True:
            self.policy_evaluation()
            if self.policy_improvement():
                break

    def move(self, game):
        # Return the move based on the current policy
        current_state = game.get_hash()
        if current_state in self.policy:
            return self.policy[current_state]
        else:
            # If the current state is not in the policy, choose a random move
            empty_positions = game.get_empty_positions()
            return empty_positions[np.random.choice(len(empty_positions))]

"""#### <font color="blue">Q2.1 (3/7): Run the following: Iteration "X" player against a Random "O" agent </font>"""

player_o = RandomAgent(PLAYER_O)  # This is the random agent
player_x = PolicyIterationAgent(PLAYER_X)  # This is the value iteration agent

# player_x = ValueIterationAgent(PLAYER_X)  # This is the random agent
# player_o = RandomAgent(PLAYER_O)  # This is the value iteration agent

game = Game(player_x, player_o)
# print(game.board)

# Compute the policy using value iteration only for the value iteration agent
player_x.train()  # We only need to compute this for player O

# Play the game

game.play()

"""#### <font color="blue"> Q2.2 (3/7): Based on the example (Game 0: RandomAgent "O" v.s. PlicyIterationAgent "X") above, run the following game: </font>
* Game1: RandomAgent "X" v.s. PolicyIterationAgent "O"
* Game2: PolicyIterationAgent "X" v.s. AggressiveAgent "O"
* Game3: PolicyIterationAgent "O" v.s. AggressiveAgent "X"
* Game4: PolicyIterationAgent "X" v.s. DefensiveAgent "O"
* Game 5: PolicyIterationAgent "O" v.s. DefensiveAgent "X"

Use the one single code cell *below*
"""

# Game 1:

# Game 2:

# Game 3:

# Game 4:

# Game 5:

"""#### <font color="blue"> Q2.3 (1/7): Repeat the games (Game 0-5) above 50 rounds each Game. Using PolicyIterationAgent, print out number of *wins*, *losts* and *draw* </font>"""

game.show_board = False

# -- Your Code Here ---

"""### <font color="blue"> **Task 2** (6 marks):</font>  Q-Learn

Write a QLearn agent in QLearnIterationAgent. No specific requirements of functions, but the planning process have to be done in a plan() function.
"""

class QLearningAgent(Agent):

    def __init__(self, symbol, alpha=0.4, gamma=0.9, epsilon=0.1, living_penalty=-1):
        super().__init__(symbol)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Epsilon for the epsilon-greedy policy
        self.Q = {}  # Initialize Q-table
        self.living_penalty = living_penalty
        self.win_reward = 10.0
        self.lose_reward = -50.0
        self.draw_reward = 0.0
        self.initial_state = np.zeros((GAME_ROW, GAME_COL), dtype=int)  # Initialize the initial state
        self.current_symbol = symbol  # The symbol of the current player

    # -- Your Code Here---


    def train(self, num_episodes=100000):
        # -- Your Code Here --
        pass


    def hash_state(self, state):
        return str(state.reshape(GAME_ROW * GAME_COL))

    def get_available_actions(self, state):
        return [(i, j) for i in range(GAME_ROW) for j in range(GAME_COL) if state[i, j] == EMPTY]

    def make_move(self, state, action, symbol):
        new_state = np.array(state)
        new_state[action] = symbol
        reward = self.get_reward(new_state, symbol)
        done = is_terminal(new_state)
        return new_state, reward, done


    def move(self, game):
        # Extract the board from the Game object
        board = game.board
        state_hash = self.hash_state(board)
        available_actions = self.get_available_actions(board)

        if not available_actions:
            raise ValueError("No available actions to make a move.")

        # Choose the best action based on the Q-table
        action = self.choose_action(state_hash, available_actions)

        # Convert action to the format expected by Game's make_move method (e.g., (row, col))
        return action

"""#### <font color="blue">Q3.1 (3/6): Run the following example: Iteration "X" player against a Random "O" agent </font>"""

# Initialize the QLearningAgent with its symbol (X or O)
q_learning_agent = QLearningAgent(PLAYER_X)

# Assume there is a random agent for the opponent
random_agent = RandomAgent(PLAYER_O)

# Initialize the game environment with both agents
game = Game(q_learning_agent, random_agent)

# Train the QLearningAgent with a function that simulates playing the game
# The train function would need to be implemented to simulate games within the agent
q_learning_agent.train()

# Use the game's play function to start playing
game.play()

"""#### <font color="blue"> Q3.2 (2/6): Based on the example (Game 0: RandomAgent "O" v.s. QLearnAgent "X") above, run the following game: </font>
* Game1: RandomAgent "X" v.s. QLearnAgent "O"
* Game2: QLearnAgent "X" v.s. AggressiveAgent "O"
* Game3: QLearnAgent "O" v.s. AggressiveAgent "X"
* Game4: QLearnAgent "X" v.s. DefensiveAgent "O"
* Game 5: QLearnAgent "O" v.s. DefensiveAgent "X"

Use the one single code cell *below*
"""

# Game 1:

# Game 2:

# Game 3:

# Game 4:

# Game 5:

"""#### <font color="blue"> Q3.3 (1/7): Repeat the games (Game 0-5) above 50 rounds each Game. Using QLearnAgent, print out number of *wins*, *losts* and *draw* </font>"""

game.show_board = False

# -- Your Code Here --