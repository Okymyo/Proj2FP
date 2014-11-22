import pygame
import math

# Define original font size
FONTSIZE = 35

# Define some colors

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

PASTEL   = ( 249, 247, 235)
GOLD     = ( 231, 186,   9)
BOARD    = ( 172, 157, 143)

FONT     = (  99,  91,  82)

# Define tile info

TILE_INFO    = {0    : (( 192, 179, 165), FONT),
                2    : (( 234, 222, 209), FONT),
                4    : (( 232, 218, 188), FONT),
                8    : (( 237, 161, 102), WHITE),
               16    : (( 229, 121,  67), WHITE),
               32    : (( 245, 102,  73), WHITE),
               64    : (( 226,  66,  42), WHITE),
              128    : (( 239, 209,  89), WHITE),
              256    : (( 234, 196,  71), WHITE),
              512    : (( 221, 181,  33), WHITE),
             1024    : (( 234, 188,  36), WHITE),
             2048    : (( 231, 186,  11), WHITE),
             'other' : ((  47,  44,  38), WHITE)}

def draw_square(screen, color, x, y, width, radius = 5):
    if width < 2 * radius:
        pygame.draw.ellipse(screen, color, [x,y,width,width], 5)
    else:
        pygame.draw.rect(screen, color, [x + radius, y, width - 2 * radius, width], 0)
        pygame.draw.rect(screen, color, [x, y + radius, width, width  - 2 * radius], 0)
        pygame.draw.ellipse(screen, color, [x, y, 2 * radius, 2 * radius], 0)
        pygame.draw.ellipse(screen, color, [x + width - 2 * radius, y, 2 * radius, 2 * radius], 0)        
        pygame.draw.ellipse(screen, color, [x, y + width - 2 * radius, 2 * radius, 2 * radius], 0)
        pygame.draw.ellipse(screen, color, [x + width - 2 * radius, y + width - 2 * radius, 2 * radius, 2 * radius], 0)


class tile():
    
    def __init__(self, value):
        self.__value = value

        if value < 4096:
            self.__color     = TILE_INFO[value][0]
            self.__fontcolor = TILE_INFO[value][1]
        else:
            self.__color     = TILE_INFO['other'][0]
            self.__fontcolor = TILE_INFO['other'][1]

        if value < 100:
            self.__fontsize  = FONTSIZE
        else:
            self.__fontsize  = int(2 * FONTSIZE / (math.log10(value) + 1))            

        self.__text = pygame.font.SysFont('arialroundedmtbold', self.__fontsize, False, False)
        self.__text = self.__text.render(str(value), True, self.__fontcolor)
            
            
    def draw(self, screen, l, c):
        draw_square(screen, self.__color, 20 + (c - 1) * 75, 190 + (l - 1) * 75, 65, 4)
        if self.__value > 0:
            text_rect = self.__text.get_rect()
            text_rect.centerx = 53 + (c - 1) * 75
            text_rect.centery = 223 + (l - 1) * 75
            screen.blit(self.__text, text_rect) 

class window_2048():
    
    def __init__(self):
        
        # Initialize pygame
        pygame.init()
        
        # Initialize game window
        size = (330, 500)
        self.__screen = pygame.display.set_mode(size)        
        pygame.display.set_caption("2048")
        
        # Initialize clock
        self.__clock = pygame.time.Clock()
        
        # Initial canvas: background
        self.__screen.fill(PASTEL)
        
        # Initial canvas: 2048 tile
        draw_square(self.__screen, GOLD,   10, 10,  90, 8)

        text = pygame.font.SysFont('arialroundedmtbold', 30, False, False)
        text = text.render("2048", True, WHITE)        
        text_rect = text.get_rect()
        text_rect.centerx = 55
        text_rect.centery = 55

        self.__screen.blit(text, text_rect)
        
        # Initial canvas: clean board
        draw_square(self.__screen, BOARD, 10, 180, 310, 8)
                
    
    def get_play(self):
        
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                return 'Q'
    
            # User pressed down on a key
            elif event.type == pygame.KEYDOWN:
                # Figure out if it was an arrow key.
                if event.key == pygame.K_LEFT:
                    return 'W'
    
                if event.key == pygame.K_RIGHT:
                    return 'E'
    
                if event.key == pygame.K_UP:
                    return 'N'
    
                if event.key == pygame.K_DOWN:
                    return 'S'

                if event.key == pygame.K_q:
                    return 'Q'
                
    
    def draw_tile(self, value, l, c):
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        
        tile(value).draw(self.__screen, l, c)
        pygame.display.flip()

    def draw_score(self, score, x, y):
        self.__screen.fill(PASTEL, (x-100, y-20, 200, 28))
        text = pygame.font.SysFont('arialroundedmtbold', 30, False, False)
        text = text.render("Score: "+str(score), True, BOARD)        
        text_rect = text.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.__screen.blit(text, text_rect)
        
    def step(self):
        self.__clock.tick(30)
