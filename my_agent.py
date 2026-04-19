from agent import Agent
from oxono import Game
import time

class MyAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
    
    def act(self, state, remaining_time):
        return self.AlphaBetaSearch(state, remaining_time)
    
    def evaluate(self, state):
        if Game.is_terminal(state):
            util = Game.utility(state, self.player)
            return util * 10000 #huge score if game is decided
        
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
            opponent_color_count = 0


            my_x_count=0
            opponent_x_count=0
            my_o_count=0
            opponent_o_count=0

            for i in group:
                if i != None:
                    symbol, who = i

                    if who==player:
                        our_color_count += 1
                    else:
                        opponent_color_count += 1

                    if symbol=="x":
                        if who == player:
                            my_x_count += 1
                        else:
                            opponent_x_count += 1
                    if symbol=="o":
                        if who == player:
                            my_o_count += 1
                        else:
                            opponent_o_count += 1

            color_score = 0
            if opponent_color_count == 0:
                if our_color_count == 1:
                    color_score = 1
                if our_color_count == 2:
                    color_score = 10
                if our_color_count == 3:
                    color_score = 100

            if our_color_count == 0:
                if opponent_color_count==3:
                    color_score = -500
                if opponent_color_count==2:
                    color_score = -20
                if opponent_color_count == 1:
                    color_score = -1

            symbol_score = 0

            #x symbol
            if opponent_x_count == 0:
                if my_x_count == 2:
                    symbol_score += 10
                if my_x_count == 3:
                    symbol_score += 100

            if my_x_count == 0:
                if opponent_x_count == 2:
                    symbol_score += -10
                if opponent_x_count == 3:
                    symbol_score += -200

            #o symbol
            if opponent_o_count == 0:
                if my_o_count == 2:
                    symbol_score += 10
                if my_o_count == 3:
                    symbol_score += 100

            if my_o_count == 0:
                if opponent_o_count == 2:
                    symbol_score += -10
                if opponent_o_count == 3:
                    symbol_score += -200
            
            

            return color_score + symbol_score
    
    def AlphaBetaSearch(self, state, remaining_time):
        # Iterative deepening: 
        # Answer is refined progressively
        # Ensure an answer within a time limit (real-time decision)
        self.start_time = time.perf_counter()  
        self.time_limit = remaining_time * 0.08
        best = list(Game.actions(state))[0]
        depth = 1

        while True:
            try:
                v, action = self.max_value(state, float('-inf'), float('inf'), depth)
                if action is not None:
                    best = action
                depth += 1
                if depth > 6: 
                    break
            except TimeoutError:
                break
            
        
        return best
    
    def max_value(self, state, alpha, beta, depth):
        if time.perf_counter() - self.start_time >= self.time_limit:
            raise TimeoutError()
        
        if Game.is_terminal(state):
            return Game.utility(state, self.player), None
        if depth == 0:
            return self.evaluate(state), None
        
        v = float('-inf')
        action = None
        
        for a in Game.actions(state):
            new_state = state.copy()
            Game.apply(new_state, a)
            v2, _ = self.min_value(new_state, alpha, beta, depth-1)
            if v2 > v:
                v, action = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, action
        return v, action
    
    def min_value(self, state, alpha, beta, depth):
        if time.perf_counter() - self.start_time >= self.time_limit:
            raise TimeoutError()
        
        if Game.is_terminal(state):
            return Game.utility(state, self.player), None
        if depth == 0:
            return self.evaluate(state), None
        
        v = float('inf')
        action = None
        
        for a in Game.actions(state):
            new_state = state.copy()
            Game.apply(new_state, a)
            v2, _ = self.max_value(new_state, alpha, beta, depth-1)
            if v2 < v:
                v, action = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, action
        return v, action
