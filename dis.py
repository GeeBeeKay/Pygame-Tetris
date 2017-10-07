import random, sys, os, pygame
# coding=UTF8

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0,0,255)
CYAN  = (0,255,255)

PINK = (255, 255, 0)
YELLOW = (255, 128, 0)

WHITE = (235, 235, 235)

BLACK = (16,16,16)

colors = [(0,0,0), (100, 100, 100), BLUE, CYAN, GREEN, PINK, YELLOW,RED, (175, 175,175) ]

RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def rotate(x): return list(list(x)[::-1] for x in zip(*x))

path = os.path.split(__file__)[0]+"/"

running = True

class Screen:
    def __init__(self):

        self.isgameover = False
        self.endit = False

        self.danger = False
        self.danger_anim = 0

        self.lines = []
        self.score = 100
        self.x = 6
        self.y = 0
        self.block = 21
        self.speed = 1
        self.level = 1
        self.blocks = Block()
        self.player = self.blocks.block1

        self.y_speed = 12
        self.curr_y = 0
        pygame.mixer.init(44100, -16, 2, 2048)
        self.downsound = pygame.mixer.Sound(path + "down.wav")
        self.gameoversound = pygame.mixer.Sound(path + "end.wav")
        self.tetrissound = pygame.mixer.Sound(path +"tetris.wav")
        pygame.mixer.music.load(path +"background.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.isplaying = True

        self.lvl = 1
        self.nextlvl = 8

        self.scribbles = pygame.image.load(path + "t.jpg")
        self.bg = pygame.image.load(path + "bg.jpg")

        for y in range(27):
            list = []
            for x in range(18):
                if y == 26:
                    list.append(8)
                else:
                    list.append(0)
            list[0] = 8
            list [17] = 8
            self.lines.append(list)
        self.fullline = self.lines[26]
        self.emptyline = [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]

    def drawscreen(self):
        x = 0
        y = 0
        for line in self.lines:
            row = ""
            for l in line:
               if not l == 0:
                   self.screen.blit(colorize(self.scribbles, colors[l]), [(x) * self.block + 5, (y) * self.block+5])
               elif not l == 0:
                    pygame.draw.rect(self.screen, (colors[l]), pygame.Rect((x) * self.block + 5, (y) * self.block+5,self.block, self.block))
               x += 1
            y += 1
            x = 0

    def isvalid(self, direction_x, direction_y):
        x = self.x + direction_x
        origx = x
        y = self.y + direction_y


        out = True

        for chunk_y in self.player:
            for chunk_x in chunk_y:
                if not chunk_x == 0:
                    if not self.lines[y][x] == 0:
                        out = False
                x += 1
            y += 1
            x = origx

        return out

    def canrotate(self):
        x = self.x
        origx = x
        y = self.y
        player = rotate(self.player)

        out = True

        for chunk_y in player:
            for chunk_x in chunk_y:
                if not chunk_x == 0:
                    if not self.lines[y][x] == 0:
                        out = False
                x += 1
            y += 1
            x = origx

        return out

    def newblock(self):
        self.downsound.play()
        self.checktetris()
        self.x = random.randint(1,14)
        self.y = 0
        self.player = self.blocks.randblock()
        n = True
        if not self.isvalid(0,0):
            n = False
            for i in range(1,14):
                self.checktetris()
                self.x = i
                self.y = 0
                if self.isvalid(0,1):
                    n = True
                    break

        if n == False:
            self.gameoversound.play()
            self.isgameover = True


        b = 0
        for i in [self.lines[0], self.lines[1], self.lines[2], self.lines[3]]:
            for l in i:
                if l == 0:
                    b += 1

        if b < 63:
            self.danger = True
        else:
            self.danger = False



    def moveplayer(self, inp):

        x = self.x
        origx = x
        y = self.y

        for chunk_y in self.player:
            for chunk_x in chunk_y:
                if not chunk_x == 0:
                    self.lines[y][x] = 0
                x += 1
            y += 1
            x = origx

        #-------------move one down

        if not inp == None:
            inp = inp.upper()
            if inp == "W":
                if self.canrotate():
                    self.player = rotate(self.player)
            elif inp == "D":
                if self.isvalid(1, 0):
                    self.x += 1
            elif inp == "A":
                if self.isvalid(-1, 0):
                    self.x -= 1

        if self.isvalid(0, 1):
            if self.curr_y == 0 or inp == "S":
                self.y += 1
                self.curr_y = self.y_speed
            else:
                self.curr_y -= 1

        else:


            x = self.x
            origx = x
            y = self.y
            for chunk_y in self.player:
                for chunk_x in chunk_y:
                    if not chunk_x == 0:
                        self.lines[y][x] = chunk_x
                    x += 1
                y += 1
                x = origx

            self.newblock()


        #------------create piece in level

        x = self.x
        origx = x
        y = self.y
        for chunk_y in self.player:
            for chunk_x in chunk_y:
                if not chunk_x == 0:
                    self.lines[y][x] = chunk_x
                x += 1
            y += 1
            x = origx

    def checktetris(self):
        multi = 1
        y = 0
        for line in self.lines:
            if y == 26:
                break
            if not 0 in line:
                self.lines.remove(line)
                self.lines.insert(1, [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8])
                self.score += 30 * multi + 100
                multi = multi * 2
                self.nextlvl -= 1
                self.tetrissound.play()
            y += 1



    def update(self):
        FPS = 20
        pygame.init()
        fpsClock = pygame.time.Clock()

        #myfont = pygame.font.SysFont('Sans', 52)
        myfont = pygame.font.Font(path+  "alphabetized cassette tapes.ttf",62)
        myfont_small = pygame.font.Font(path + "alphabetized cassette tapes.ttf", 48)

        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        surface = pygame.Surface(self.screen.get_size())
        surface = surface.convert()
        surface.fill((255, 255, 255))
        clock = pygame.time.Clock()

        self.newblock()

        while True:
          if not self.isgameover:
            move = ""
            keys = pygame.key.get_pressed()  # checking pressed keys


            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.endit = True
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        move = "W"
                    if event.key == pygame.K_q:
                        if self.isplaying:
                            pygame.mixer.music.fadeout(2)
                            self.isplaying = False
                        else:
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                            self.isplaying = True




            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_DOWN]:
                move = "S"
            if keys[pygame.K_LEFT]:
                move = "A"
            if keys[pygame.K_RIGHT]:
                move = "D"

            self.moveplayer(move)

            pygame.display.flip()
            pygame.display.update()

            #self.screen.fill((255, 255, 255))
            self.screen.fill((255,255,255))
            self.screen.blit(self.bg, [5, 5])

            score = str(self.score)
            while len(score) < 5:
                score = "0"+str(score)

            textsurface = myfont.render('Score: '+score, True, BLACK)
            self.screen.blit(textsurface, (450, 50))
            textsurface = myfont.render('Level: {}'.format(self.lvl), True, BLACK)
            self.screen.blit(textsurface, (540, 100))
            if self.danger:
                self.danger_anim += 1
                if self.danger_anim > 8:
                    textsurface = myfont.render('DANGER!', True, RED)
                    self.screen.blit(textsurface, (510, 300))
                    if self.danger_anim > 16:
                        self.danger_anim = 0
            textsurface = myfont_small.render('Press Q to toggle music', True, BLUE)
            self.screen.blit(textsurface, (555, 555))
            self.drawscreen()

            if self.nextlvl <= 0:
                self.nextlvl = 8
                self.lvl += 1
                if self.y_speed > 1:
                    self.y_speed -= 1



          else:
              events = pygame.event.get()
              for event in events:
                  if event.type == pygame.QUIT:
                      pygame.quit()
                      sys.exit()
                  if event.type == pygame.KEYUP:
                      if event.key == pygame.K_r:
                          self.endit = True
              pygame.display.flip()
              pygame.display.update()

              # self.screen.fill((255, 255, 255))
              self.screen.fill((255, 255, 255))
              self.screen.blit(self.bg, [5, 5])

              for i in range(20):
                  pygame.draw.polygon(self.screen, (0,0,0), [[i * 40 - random.randint(0, 20), 570],[i * 40 +20- random.randint(0, 15), 550- random.randint(10, 60)],[i * 40 + 40- random.randint(0, 30), 570]])
              c = random.randint(128, 255)
              fill_gradient(self.screen, (0,0,0), (c,c,c), pygame.Rect(0, 570, 800, 30))
                  #pygame.draw.polygon

              score = str(self.score)
              while len(score) < 5:
                  score = "0" + str(score)

              textsurface = myfont.render('____________________________________________________________', True, BLACK)
              self.screen.blit(textsurface, (0, 270))


              textsurface = myfont.render('Game Over', True, RED)
              self.screen.blit(textsurface, (333, 150))
              textsurface = myfont.render("Press r to restart!", True, GREEN)
              self.screen.blit(textsurface, (283, 220))
              textsurface = myfont.render('Final Score: ', True, BLACK)
              self.screen.blit(textsurface, (333, 350))
              textsurface = myfont.render(str(score), True, CYAN)
              self.screen.blit(textsurface, (363, 395))



          fpsClock.tick(FPS)
          if self.endit:
              break

class Block:
    def __init__(self):
        self.block1 = [[1,1],
                       [1,1]]
        self.block2 = [[0, 2, 0],
                       [0, 2, 0],
                       [0, 2, 2]]
        self.block3 = [[0, 3, 0],
                       [0, 3, 0],
                       [3, 3, 0]]
        self.block4 = [[4, 4, 0],
                       [0, 4, 4],
                       [0, 0, 0]]
        self.block5 = [[0, 5, 5],
                       [5, 5, 0],
                       [0, 0, 0]]
        self.block6 = [[0, 6, 0],
                       [0, 6, 0],
                       [0, 6, 0],
                       [0, 6, 0]]
        self.block7 = [[0, 0, 0],
                       [7, 7, 7],
                       [0, 7, 0]]

    def randblock(self):
        return [self.block1, self.block2, self.block3, self.block4, self.block5, self.block6, self.block7][random.randint(0,6)]


def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse

    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom
    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
            )
            fn_line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
            )
            fn_line(surface, color, (col, y1), (col, y2))

def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image

while running:
	s = Screen()
	s.update()
