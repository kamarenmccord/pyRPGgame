
GAME_TITLE = 'Kams testing RPG'

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (150, 25, 21)
GREEN = (0, 255, 0)
DARKGREEN = (0, 131, 36)
BLUE = (0, 0, 255)
LIGHTBLUE = (39, 192, 219)
GREY = (224, 244, 244)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN = (153, 155, 102)
DARKBROWN = (102, 51, 0)
BATTLEBACKGROUND_COLOR = 230, 255, 255

# screen size
WIDTH = 1024
HEIGHT = 768

# map settings
TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = WIDTH / TILESIZE

# system settings
DIRECTORY = 'save_dir'
MOB_DIR = 'mobs'
SAVELIMIT = 10  # allow up to 10 previous save files

# game settings
CLIPPING_BUFFER = +0  # increase to push player farther from wall collisions
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
MAINCHARIMAGES = ['player_down1.png', 'player_down2.png', 'player_down3.png', 'player_left1.png', 'player_left2.png',
                  'player_left3.png', 'player_up1.png', 'player_up2.png', 'player_up3.png', 'player_right1.png',
                  'player_right2.png', 'player_right3.png']

# global settings for instances
MAX_LEVEL = 100

# item icons
ICONS = {'potions': ['potions5.jpg', 'potions4.jpg']}
ICONS_FOLDER = 'logics/icons'
