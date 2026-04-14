from agent import Agent
from oxono import Game
import random

class OurAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
    
    def act(self, state, remaining_time):
        actions = list(Game.actions(state))
        return random.choice(actions)
    
    def evaluate(self, state):
        our_score = 0
        opponent_score = 0

        for i in range(6):
            for j in range(3):
                group = [state.board[i][j], state.board[i][j+1], state.board[i][j+2], state.board[i][j+3]]

                our_score += self.score_group(group, self.player)
                opponent_score += self.score_group(group, 1 - self.player)

        for j in range(6):
            for i in range(3):
                group = [state.board[i][j], state.board[i+1][j], state.board[i+2][j], state.board[i+3][j]]

                our_score += self.score_group(group, self.player)
                opponent_score += self.score_group(group, 1 - self.player)


        return our_score - opponent_score

    def score_group(self, group, player):
            our_color_count = 0
            our_symbol_count = 0

            opponent_color_count = 0
            opponent_symbol_count = 0

            for i in group:
                if i != None:
                    if i[1]==player:
                        our_color_count += 1
                    else:
                        opponent_color_count += 1

            color_score = 0
            if opponent_color_count == 0:
                if our_color_count == 1:
                    color_score = 1
                if our_color_count == 2:
                    color_score = 10
                if our_color_count == 3:
                    color_score = 100
            
            return color_score