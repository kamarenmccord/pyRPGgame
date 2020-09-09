
GAME_TITLE = 'Kams testing RPG'

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN = (153, 155, 102)
DARKBROWN = (102, 51, 0)
BATTLEBACKGROUND_COLOR = 230, 255, 255
BACKDROP_BLUE = './logics/backdrop.jpg'

# screen size
WIDTH = 1024
HEIGHT = 768

# map settings
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = WIDTH / TILESIZE

# system settings
DIRECTORY = 'save_dir'
SAVELIMIT = 10  # allow up to 10 previous save files

# game settings
CLIPPING_BUFFER = 10  # increase to push player farther from wall collisions
FPS = 60
TITLE = 'GAME NAME'
BGCOLOR = TAN
USE_PREVIOUS_DATA = False
STEPSIZE = TILESIZE*2
BATTLECHANCE = 0.15
ENEMYVARIANCE = 3  # increase to get harder enemies

# fonts
FONTSMENU = 'overpass-regular.otf'
FONTSBATTLE = 'overpass-regular.otf'

# player settings
PLAYERSPEED = 200
MAINCHARIMAGE = 'd-kin-front.png'

# global settings for instances
MAX_LEVEL = 100
