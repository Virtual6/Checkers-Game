from BoardClasses import Move
from BoardClasses import Board
import copy
import math
from random import randint

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,row,col,p):
        self.row = row
        self.col = col
        self.p = p
        self.board = Board(row,col,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        tree_depth = 4
        
		# for beta alpha pruning
		alpha = -math.inf
        beta = math.inf
        
		# best moves list
		best_moves = []
        
		# Get best moves
		for row in moves:
            for move in row:
                board_duplicated = copy.deepcopy(self.board)
                board_duplicated.make_move(move, self.color)
                curr = self.minValue(board_duplicated, tree_depth - 1, alpha, beta)
                if curr > alpha:
                    alpha = curr
                    best_moves = [move]
                elif curr == alpha:
                    best_moves.append(move)
		
		# Pick a random move from among the best moves
		best_move = best_moves[randint(0, len(best_moves)-1)]
        # Make the move
		self.board.make_move(best_move, self.color)
        return best_move
	
	
	def edgeValue(self, board, color):
        value = 0
        for m, row in enumerate(board.board):
            for k, col in enumerate(row):
                if board.board[m][k].get_color().lower() == color:
                    king_checker = board.board[m][k].is_king
                    if king_checker:
                        value = value + 0.02
                    if m == 0 or k == 0 or m == self.row - 1 or k == self.col - 1:
                        value = value + 0.01
        return value
    

     
        moves = board.get_all_possible_moves(self.opponent[self.color])
        if tree_depth == 0:
            return self.valuate(board)
        if len(moves) == 0:
            if board.is_win(self.color):
                return math.inf - 1
            else:
                return -math.inf + 1

        value = math.inf
        for row in moves:
            for move in row:
                board_duplicated = copy.deepcopy(board)
                board_duplicated.make_move(move, self.opponent[self.color])
                value = min(value, self.maxValue(board_duplicated, tree_depth - 1, alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return beta

    def valuate(self,board):
        res = 0
        if self.color == 1:
            res = res + board.black_count - board.white_count + self.edgeValue(board, "b")
        else:
            res = res + board.white_count - board.black_count + self.edgeValue(board, "w")

        return res
		
		
	def minimax(self, depth, board, is_max, alpha, beta, player):
		# Get player's all possible moves
		possible_moves = board.get_all_possible_moves(player)

		if depth == 0:
			return self.evaluate(board)
		elif len(possible_moves) == 0:
			if board.is_win(self.color):
				return math.inf - 1
			else:
				return -math.inf + 1

		if is_max:
			max_ = -math.inf
			for row in possible_moves:
				for move in row:
					board_copied = copy.deepcopy(board)
					board_copied.make_move(move, player)
					max_ = max(max_,
							   self.minimax(depth - 1, board_copied, False, alpha, beta, self.get_opponent()))
					if max_ >= beta:
						return max_
					alpha = max(alpha, max_)
			return max_
	
	def maxValue(self, board, tree_depth, alpha, beta):
        moves = board.get_all_possible_moves(self.color)
        if tree_depth == 0:
            return self.valuate(board)
        elif len(moves) == 0:
            if board.is_win(self.color):
                return math.inf - 1
            else:
                return -math.inf + 1

        value = -math.inf
        for row in moves:
            for move in row:
                board_duplicated = copy.deepcopy(board)
                board_duplicated.make_move(move, self.color)
                value = max(value, self.minValue(board_duplicated, tree_depth - 1, alpha, beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
        return value
		
	def get_player(self):
		return self.color

	def get_opponent(self):
		return self.opponent[self.color]

	@staticmethod
	def is_valid(move):
		return len(move) > 0
