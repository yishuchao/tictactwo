from utils import *
from solver import *

class TTT():
    def __init__(self, position = '000000000000000000', player='1', xdouble = False, odouble = False):
        #board is represented with a 18-digit string,
        #if player = '1' means it's x's turn to move o.w. it's o's turn to move
        self.position = position
        self.player = player
        self.xdouble = xdouble
        self.odouble = odouble
        if self.player == '1':
            self.opposite = '2'
        else:
            self.opposite = '1'

    def group(self,position):
        #breaks the board into 9 square each squre is represented with a len-2 string
        grouped = []
        for i in range(18):
            if (i+1) % 2 == 0:
                grouped.append("".join([position[i-1],position[i]]))
        return grouped


    def generateOneMove(self):
        #if the position is '0' then that's a possible move
        #if a square (aka a len-2 string) is '12' or '21' then the player can also make a move 
        possible_moves = []
        board = self.group(self.position)
        for i in range(9): 
            if board[i][0]!='0' and board[i][1] != '0' and board[i][0] != board[i][1]:
                if self.player == board[i][0]:
                    possible_moves.append([2*i+1])
                else:
                    possible_moves.append([2*i])
        for i in range(18):
            if self.position[i] == "0":
                possible_moves.append([i])
        return possible_moves

    def generateTowMoves(self):
        #pick combinations of single moves
        one_moves = self.generateOneMove()
        possible_moves = []
        for i in range(len(one_moves)):
            for j in range(i+1,len(one_moves)):
                    possible_moves.append([one_moves[i][0],one_moves[j][0]])
        return possible_moves + one_moves

    def GenerateMoves(self):
        #generate either 1 or 2 moves depending on if the player has used up their double move or not
        if self.player == "1" and not self.xdouble:
            return self.generateTowMoves()
        elif self.player == "1" and self.xdouble:
            return self.generateOneMove()
        elif self.player == '2' and not self.odouble:
            return self.generateTowMoves()
        elif self.player == "2" and self.odouble:
            return self.generateOneMove()


    def DoMove(self,move):
        #do move by replacing the item at position i of board with self.player and return a new TTT object
        newboard = list(self.position)
        if len(move) == 2:
            newboard[move[0]] = self.player
            firstpos = "".join(newboard)
            if self.complete_triple(firstpos):
                return TTT(firstpos, self.opposite)
            else:
                newboard[move[1]] = self.player
            newpos = "".join(newboard)
            if self.player == "1":
                return TTT(newpos, self.opposite, True, self.odouble)
            elif self.player == "2":
                return TTT(newpos, self.opposite, self.xdouble, True)
        else:
            newboard[move[0]] = self.player
            newpos = "".join(newboard)
            return TTT(newpos, self.opposite, self.xdouble, self.odouble)

    def full_board(self):
        #if all the squares have been claimed then return True else False
        grouped = self.group(self.position)
        checker = [item[0] == item[1] for item in grouped]
        if "0" not in self.position and False not in checker:
            return True
        else:
            return False


    def check_triple(self, str1, str2, str3):
        #check if we have three in a row
        if ("11" in str1 and "11" in str2 and "11" in str3) or ("22" in str1 and "22" in str2 and "22" in str3):
            return True
        else:
            return False

    def complete_triple(self, position):
        sorted_group = self.group(position)
        if self.check_triple(sorted_group[0],sorted_group[1],sorted_group[2]):
            return True
        elif self.check_triple(sorted_group[3], sorted_group[4],sorted_group[5]):
            return True
        elif self.check_triple(sorted_group[6],sorted_group[7],sorted_group[8]):
            return True
        elif self.check_triple(sorted_group[0],sorted_group[3],sorted_group[6]):
            return True
        elif self.check_triple(sorted_group[1],sorted_group[4],sorted_group[7]):
            return True
        elif self.check_triple(sorted_group[2],sorted_group[5],sorted_group[8]):
            return True
        elif self.check_triple(sorted_group[0],sorted_group[4],sorted_group[8]):
            return True
        elif self.check_triple(sorted_group[2],sorted_group[4],sorted_group[6]):
            return True
        else: 
            return False


    def PrimitiveValue(self):
        if self.complete_triple(self.position):
            return Value.LOSE
        elif self.full_board() and not self.complete_triple(self.position):
            return Value.TIE
        else:
            return Value.UNDECIDED
            
    



Solver().printAnalysis(TTT(),28)
