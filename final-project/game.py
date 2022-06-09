class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.connect = False
        self.ready = False
        self.turn = 0
        self.id = id
        self.moves = [0, 0]
        self.wins = [0,0]
        self.ties = 0
        self.choice = None

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def reset_game(self):
        self.ready = False
        self.choice = None

    def is_ready(self):
        return self.ready

    def get_turn(self):
        return self.turn

    def get_choice(self):
        return self.choice

    def toggle_turn(self):
        if self.turn == 0:
            self.turn = 1
        elif self.turn == 1:
            self.turn = 0

    def play(self, player, move):
        self.moves[player] = move
    
    def select(self, choice):
        self.choice = choice
        self.ready = True

    def lock(self, player):
        if self.ready:
            if player == 0:
                self.p1Went = True
            else:
                self.p2Went = True

    def is_connected(self):
        return self.connect

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):    
        p1 = (self.moves[0] + 1) / 2
        p2 = (self.moves[1] + 1) / 2

        winner = -1
        if int(p1) + int(p2) == self.choice:
            winner = self.turn

        print(p1, p2, int(p1) + int(p2), self.choice)
        print("winner : ", winner)
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False