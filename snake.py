"""
 Simple snake example.
 
 Sample Python/Pygame Programs

"""
 
import pygame
import argparse
from random import randrange

 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

segment_width = 15
segment_height = 15
segment_margin = 0
speed = 5

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    def __init__(self, x, y):
        super().__init__()
 
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


class Player:

    def __init__(self, length):
        super().__init__()
        self.length = length
        self.snake_segments = []
        self.allspriteslist = pygame.sprite.Group()
        self.x_change = segment_width + segment_margin
        self.y_change = 0

    def onInit(self):
        for i in range(self.length):
            x = 300 - (segment_width + segment_margin) * i
            y = 30
            segment = Segment(x, y)
            self.snake_segments.append(segment)
            self.allspriteslist.add(segment)
    
    def updatePosition(self, x, y):
        self.x_change = x
        self.y_change = y
    
    def eatFood(self, x, y):
        self.length+=1
        segment = Segment(x, y)
        self.snake_segments.insert(0, segment)
        self.allspriteslist.add(segment)

    def draw(self, screen):
        old_segment = self.snake_segments.pop()
        self.allspriteslist.remove(old_segment)
    
        x = self.snake_segments[0].rect.x + self.x_change
        y = self.snake_segments[0].rect.y + self.y_change
        segment = Segment(x, y)
    
        self.snake_segments.insert(0, segment)
        self.allspriteslist.add(segment)
    
        self.allspriteslist.draw(screen)
    
    def getHead(self):
        return self.snake_segments[0].rect

class Grid :
    def __init__(self, width, height, blocksize):
        super().__init__()
        self.width = width
        self.height = height
        self.blocksize = blocksize
        self.color = WHITE

    def draw(self, screen):
        
        for x in range(0,self.width,self.blocksize):
            x = x + self.blocksize
            pygame.draw.line(screen,self.color,(x,0),(x,self.height),1)
        
        
        for y in range(0,self.height,self.blocksize):
            y = y + self.blocksize
            pygame.draw.line(screen,self.color,(0,y), (self.width,y),1)


class Food :

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = GREEN
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, segment_height, segment_width))

class Game:
    windowWidth = 900
    windowHeight = 600

    def __init__(self, needGrid=False):
        super().__init__()
        self.player = Player(5)
        self.running = False
        self.pauseState = False
        self.gameOverState = False
        self.screen = None
        self.clock = None
        self.needGrid = needGrid

    
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Snake Example')
        self.screen = pygame.display.set_mode([self.windowWidth, self.windowHeight])
        self.clock = pygame.time.Clock()
        self.running = True
        self.player.onInit()

        self.food = Food(segment_height, segment_width)
        if(self.needGrid):
            self.grid = Grid(self.windowWidth, self.windowHeight, segment_height)
    
    def onCleanup(self):
        pygame.quit()
    
    def onRender(self):
        self.screen.fill(BLACK)
        self.draw()
        pygame.display.flip()
        self.clock.tick(speed)

    def onLoop(self):
        for i in range(0,self.player.length):
            # print(self.food.x,self.food.y,self.player.snake_segments[i].rect.x, self.player.snake_segments[i].rect.y)
            if self.isCollision(self.food.x,self.food.y,self.player.snake_segments[i].rect.x, self.player.snake_segments[i].rect.y):
                self.player.eatFood(self.food.x, self.food.y)
                self.food.x = randrange(0, self.windowWidth, 15)
                self.food.y = randrange(0, self.windowHeight, 15)
            # if i != 1 and self.isCollision(self.player.snake_segments[0].rect.x,self.player.snake_segments[0].rect.y,self.player.snake_segments[i].rect.x, self.player.snake_segments[i].rect.y):
            #     print(self.player.snake_segments[0].rect.x,self.player.snake_segments[0].rect.y,self.player.snake_segments[i].rect.x, self.player.snake_segments[i].rect.y)
            #     print(i)
            #     print("collision with body")
            #     self.on_cleanup()


    def onExecute(self):
        if self.on_init() == False:
            self._running = False
        
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.updatePosition((segment_width + segment_margin) * -1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.player.updatePosition((segment_width + segment_margin), 0)
                    if event.key == pygame.K_UP:
                        self.player.updatePosition(0, (segment_height + segment_margin) * -1)
                    if event.key == pygame.K_DOWN:
                        self.player.updatePosition(0, (segment_height + segment_margin))
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.pauseState = not self.pauseState
            
            if self.isCollisionWithWall():
                self.gameOverState = True

            if self.pauseState and not self.gameOverState:
                self.pauseGame()
            elif self.gameOverState:
                self.gameOver()
                continue

            else:
                self.onLoop()
                self.onRender()

        self.onCleanup()
        pass

    def draw(self):
        self.player.draw(self.screen)
        self.food.draw(self.screen)
        if self.needGrid:
            self.grid.draw(self.screen)

    def pauseGame(self):
        self.renderText("PAUSED")
        pygame.display.flip()
        self.clock.tick(speed)
        pass

    def renderText(self, textMsg):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(textMsg, True, BLACK, WHITE) 
        textRect = text.get_rect()  
        textRect.center = (self.windowWidth // 2, self.windowHeight // 2) 
        self.screen.blit(text, textRect)

    def isCollision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 <= x2 + segment_height:
            if y1 >= y2 and y1 <= y2 + segment_height:
                return True
        return False
    
    def isCollisionWithWall(self):
        x = self.player.getHead().x
        y = self.player.getHead().y
        if x<0 or x+segment_width>self.windowWidth or y<0 or y+segment_height>self.windowHeight:
            return True
        return False
    
    def gameOver(self):
        self.renderText("GAME OVER")
        pygame.display.flip()
        self.clock.tick(speed)


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", "-g", help="set grid to game")
    args = parser.parse_args()
    
    game = Game(args.grid)
    game.onExecute()
