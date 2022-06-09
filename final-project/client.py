import pygame
from network import Network
import pickle
pygame.font.init()

thumbthumb = pygame.image.load(r"./assets/thumbthumb.png")
thumbfist = pygame.image.load(r"./assets/thumbfist.png")
fistthumb = pygame.image.load(r"./assets/fistthumb.png")
fistfist = pygame.image.load(r"./assets/fistfist.png")

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class State:
    def __init__(self, state, x, y, bgcolor):
        self.state = state
        self.x = x
        self.y = y
        self.bgcolor = bgcolor

class Button:
    def __init__(self, text, x, y, color, size, fontsize):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.tempcolor = color
        self.width = size[0]
        self.height = size[1]
        self.fontsize = fontsize

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("opensans", self.fontsize)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def set_color(self, color):
        self.color = color

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

class MoveBtn:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.move = [fistfist, thumbfist, fistthumb, thumbthumb]
        self.index = 0

    def draw(self, win):
        win.blit(self.move[self.index], (self.x + round(self.width/2) - round(self.move[self.index].get_width()/2), self.y + round(self.height/2) - round(self.move[self.index].get_height()/2)))

    def get_obj(self):
        return self.move[self.index]

    def set_move(self, move):
        self.index = move

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            if self.index < 3:
                self.index = self.index + 1
            else:
                self.index = 0
            return True
        else:
            return False

class NumberBtn(Button):
    def __init__(self, text, x, y, color, size, fontsize):
        super().__init__(text, x, y, color, size, fontsize)

class ConfirmBtn(Button):
    def __init__(self, text, x, y, color, size, fontsize):
        super().__init__(text, x, y, color, size, fontsize)

lock = Button("Lock", 280, 440, (150, 150, 150), (130, 40), 32)

movebtns = [
    MoveBtn(100, 350, (160, 80)), 
    MoveBtn(400, 350, (160, 80))
    ]

btns = [
    Button("0", 130, 565, (0, 74, 173), (50, 50), 40), 
    Button("1", 230, 565, (0, 74, 173), (50, 50), 40), 
    Button("2", 330, 565, (0, 74, 173), (50, 50), 40),
    Button("3", 430, 565, (0, 74, 173), (50, 50), 40),
    Button("4", 530, 565, (0, 74, 173), (50, 50), 40),
    ]

def redrawWindow(win, game, p):
    win.fill((201,226,101))

    if not(game.is_connected()):
        font = pygame.font.SysFont("opensans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("opensans", 60)
        text = font.render("Your Move", 1, (0, 74, 173))
        win.blit(text, (80, 250))

        text = font.render("Opponents", 1, (0, 74, 173))
        win.blit(text, (380, 250))

        p1move = game.get_player_move(0)
        p2move = game.get_player_move(1)

        # print(p1move, p2move)
        
        move1 = movebtns[0]
        move2 = movebtns[1]
        
        if game.bothWent():
            move1.set_move(p1move)
            move2.set_move(p2move)
            text1 = move1.get_obj()
            text2 = move2.get_obj()
        else:
            if p == 0:
                if p1move == 0:
                    move1.set_move(0)
                else:
                    move1.set_move(p1move)
                text1 = move1.get_obj()
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))

            if p == 1:
                if p2move == 0:
                    move2.set_move(0)
                else:
                    move2.set_move(p2move)
                text2 = move2.get_obj()
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))
        
        if game.is_ready():
            lock.set_color((0, 74, 173))
        else:
            lock.set_color((150, 150, 150))

        lock.draw(win)

        if p == 0:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
        else:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))

        font = pygame.font.SysFont("opensans", 80)
        turn = game.get_turn()
        if p == turn:
            turn = font.render("Your Turn!!", 1, (0,0,0))
            win.blit(turn, (200, 100))

            font = pygame.font.SysFont("opensans", 60)
            text = font.render("Pick Number", 1, (0, 74, 173))
            win.blit(text, (220, 500))            

            for btn in btns:
                btn.draw(win)
        else:
            turn = font.render("Opponent Turn!!", 1, (0,0,0))
            win.blit(turn, (120, 100))

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send({"action": "run", "message": "data"})
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            winner = game.winner()
            try:
                for movebtn in movebtns:
                    movebtn.set_move(0)
                game = n.send({"action": "reset", "message": "data"})
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("opensans", 90)
            if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif winner == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))

            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if lock.click(pos) and game.is_connected():
                    n.send({"action": "lock", "player": player})

                for btn in btns:
                    if btn.click(pos) and game.is_connected():
                        n.send({"action": "choice", "player": player, "message": str(btn.text)})

                for movebtn in movebtns:
                    if movebtn.click(pos) and game.is_connected():
                        print("You are player", player)
                        print("movebtn.index", movebtn.index)
                        n.send({"action": "move", "message": str(movebtn.index)})
                        
        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("opensans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()