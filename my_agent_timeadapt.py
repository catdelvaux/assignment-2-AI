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
        self.start_time = time.perf_counter()  #move starts
        #self.time_limit = remaining_time * 0.08 # tried 0.05, 0.1

        actions = list(Game.actions(state)) #legal actions
        best = actions[0] #default action
        depth = 1

        #time management
        reserve = 1.0 #keep one sec for the rest of the game
        base = 0.015 #minimum thinking time per move
        fraction = 0.03*remaining_time #3% of remaining time
        bonus = min(0.2, 0.0005 * len(actions)) #more time if there are many possible moves, cap at 0.02

        self.time_limit = min (0.15, max (0.01, base + fraction + bonus)) #never spend more that 0.15 in a move, or less than 0.01

        #mpre conservative if low on time 
        if remaining_time < 5:
            self.time_limit=min(self.time_limit, 0.03) #if we have less that 5 secs, reduc think time
        if remaining_time < 2:
            self.time_limit=min(self.time_limit, 0.015) #less that 2 secs

        self.time_limit = min(self.time_limit, max(0.005, remaining_time - reserve)) #never use the last reserve seconds

        #adaptative depth: when time is low we reduce depth
        max_depth=6
        if remaining_time<5:
            max_depth=5
        if remaining_time<2:
            max_depth=4
        
        #iterative deepening
        while True:
            try:
                v, action = self.max_value(state, float('-inf'), float('inf'), depth) 
                if action is not None:
                    best = action
                depth += 1
                #if depth > 6: #tried 4
                if depth>max_depth:
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
