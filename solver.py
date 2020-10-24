from utils import *

class Solver():

    def __init__(self):
        self.memory = {}
    
    def solve(self,game):
        hashed = hash(game.position)
        if hashed in self.memory:
            return self.memory[hashed]
        else:
            if game.PrimitiveValue() != Value.UNDECIDED:
                self.memory[hashed] = (game.PrimitiveValue(), 0)
                return self.memory[hashed]
            else:
                sub_pos = []
                children =[]
                for move in game.GenerateMoves():
                    newGame = game.DoMove(move)
                    children.append(newGame)
                for child in children:
                    if hash(child.position) in self.memory:
                        sub_pos.append(self.memory[hash(child.position)])
                    else:
                        sub_pos.append(self.solve(child))
                values = [item[0] for item in sub_pos]
                if Value.LOSE in values:
                    remoteness  = 1 + min([item[1] for item in sub_pos if item[0] == Value.LOSE])
                    self.memory[hashed] = (Value.WIN, remoteness)
                elif Value.TIE in values:
                    remoteness = 1 + max([item[1] for item in sub_pos if item[0] == Value.TIE])
                    self.memory[hashed] = (Value.TIE, remoteness)
                else:
                    remoteness = 1 + max([item[1] for item in sub_pos])
                    self.memory[hashed] =  (Value.LOSE, remoteness)
                print(len(self.memory))
                return self.memory[hashed]
    
    def printMemory(self,game):
        self.solve(game)
        print(self.memory)
    
    def printAnalysis(self,game,total_remote):
        self.solve(game)
        vals = [value for value in self.memory.values()]
        tot_win = 0
        tot_lose = 0
        tot_ties = 0
        print('-' * 43)
        print("{:<10s}{:>8s}{:>8s}{:>8s}{:>8s}".format('Remoteness', 'Win', 'Lose', 'Tie', 'Total'))
        print('-' * 43)
        for i in range(total_remote)[::-1]:
            win = len([item for item in vals if item[0] == "win" and item[1] == i])
            tot_win += win
            losses = len([item for item in vals if item[0] == "lose" and item[1] == i])
            tot_lose += losses
            ties = len([item for item in vals if item[0] == "tie" and item[1] == i])
            tot_ties += ties
            total = win + losses + ties
            print("{:<10d}{:>8d}{:>8d}{:>8d}{:>8d}".format(i,win,losses,ties,total))
        print('-' * 43)
        tot = tot_win + tot_lose + tot_ties
        print("{:<10s}{:>8d}{:>8d}{:>8d}{:>8d}".format('Total',tot_win,tot_lose,tot_ties,tot))











