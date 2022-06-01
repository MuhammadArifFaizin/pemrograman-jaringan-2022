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
    def __init__(self, text, x, y, color, size):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.tempcolor = color
        self.width = size[0]
        self.height = size[1]

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("opensans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

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
    def __init__(self, text, x, y, color, size):
        super().__init__(text, x, y, color, size)

class ConfirmBtn(Button):
    def __init__(self, text, x, y, color, size):
        super().__init__(text, x, y, color, size)

def redrawWindow(win, game, p):
    win.fill((201,226,101))

    if not(game.connected()):
        font = pygame.font.SysFont("opensans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("opensans", 60)
        text = font.render("Your Move", 1, (0, 74, 173))
        win.blit(text, (80, 250))

        text = font.render("Opponents", 1, (0, 74, 173))
        win.blit(text, (380, 250))

        text = font.render("Pick Number", 1, (0, 74, 173))
        win.blit(text, (200, 500))

        p1move = game.get_player_move(0)
        p2move = game.get_player_move(1)

        print(p1move, p2move)
        
        move1 = movebtns[0]
        move2 = movebtns[1]

        move1.set_move(p1move if p1move != None else 0)
        move2.set_move(p2move if p2move != None else 0)
        
        if game.bothWent():
            text1 = move1.get_obj()
            text2 = move2.get_obj()
        else:
            if game.p1Went and p == 0:
                text1 = move1.get_obj()
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))

            if game.p2Went and p == 1:
                text2 = move2.get_obj()
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))

        font = pygame.font.SysFont("opensans", 80)
        turn = font.render("Your Turn!!", 1, (0,0,0))
        win.blit(turn, (200, 100))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        confirm = Button("Done", 250, 630, (0, 74, 173), (150, 50))
        confirm.draw(win)

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

movebtns = [
    MoveBtn(100, 350, (160, 80)), 
    MoveBtn(400, 350, (160, 80))
    ]

btns = [
    Button("0", 100, 550, (0, 74, 173), (50, 50)), 
    Button("1", 200, 550, (0, 74, 173), (50, 50)), 
    Button("2", 300, 550, (0, 74, 173), (50, 50)),
    Button("3", 400, 550, (0, 74, 173), (50, 50)),
    Button("4", 500, 550, (0, 74, 173), (50, 50)),
    ]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("opensans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
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
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send("choice," + btn.text)
                        else:
                            if not game.p2Went:
                                n.send("choice," + btn.text)

                for movebtn in movebtns:
                    if movebtn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send("move," + str(movebtn.index))
                        else:
                            if not game.p2Went:
                                n.send("move," + str(movebtn.index))


        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("opensans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
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