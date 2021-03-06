
""" a place to store all my todo's """

# TODO: if savelimit files exist, prompt user to overwrite

# TODO: create overworld map

# TODO: put in map hooks to enter new places (buldings, maps, etc.)
#   - create door object with params(rect, connecting_map)
#   - functions for (collisions, changing map, changing state)
#   - add col points to map (like doors)
#   - when point is inside player col box trigger event
#   - col box should { change player/game state to warping(prevents going back),
#                      take a point and direction to warp to,
#                      load new map and position player at point in direction facing
#                       turn off warp status after stepping off col point
#                     }

# TODO: add more enemies and put them in zones

# TODO: add sound effects/ musics/ prettify

# Fixed: BUGFIX:: after saving pause is not held causing movement of plyr while menu is up
# DONE: add a id property to pickup npcs so that they can have same name and not stack
# DONE: added pickup-able npcs
# DONE: add a notification icon above player when obj is intractable
# DONE: rewrite popup window to do word wraping
# DONE: npc's and party chars
#       -load up sprites
#       -add speaking
# DONE: BUILD UP THE INVENTORY SCREEN
#       -after bag is selected on main menu (see other goal)
# DONE: verify quit in app.py
#       -fix broken escape function
# DONE: add a game menu that pops up on right for options like checking inv, saving, etc.
#       -add inventory
#       -add stats screen
# DONE: dialogue pop-up box
# BYPASSED: add collision box for player to wall collisions
# DONE: save_game data then successfully load data
# DONE: fix collision with save zone in char file
# DONE: tie strings to the crud module so game can be loaded after saving
# DONE: spawn player at point other than spawn point when loading map
# DONE: triggers for battle screen
#       Done: collisions to enter
#       DONE: enter battle
# DONE: build battle screen
# DONE: add an inventory for player to keep items
# DONE: build stats functions
#       - leveling up multiplier function triggered via player class stats property
#       - enemy stats
# DONE: title screen
#       + push words over on hover effect
#       + draw cursor
#       - get background
#       + add selection retention
#       + start game
#       + delete the cursor after selection
# DONE: player animation while walking

""" UPDATE IDEAS """
# TODO: create recover save screen
#        - convert epoch to datetime (for cleaner prints)

# TODO: create load screen

# DONE: add scrolling to inventory screens
