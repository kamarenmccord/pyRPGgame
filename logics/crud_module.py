
import shelve
import os
from datetime import datetime
import time

from .settings import *

"""
create read write delete module
"""

# shelve.open('saveFile', 'w,r,c,n')
# w: read write
# r: read only
# c: create if does not exist
# n: delete old file and create a new file


def get_file_list():
    if os.path.exists(f'./{DIRECTORY}'):
        files = os.listdir(f'./{DIRECTORY}')
        file_list = []
        if files:
            for file in files:
                if 'save_file+' in file:
                    file_list.append(file)
        if file_list:
            return file_list
    return 'no files'


def get_newest_file():
    files = get_file_list()
    if type(files) != list:
        return 'no files'

    currentEpoch = time.mktime(datetime.today().timetuple())

    if len(files) > 0:
        # where file == 'save_file+{epoch}'
        prevEpoch = files[0][10:]
        # go though timestamps to find true newest file sorted or not
        for file in files:
            datestamp = file[10:]
            if currentEpoch - float(datestamp) < currentEpoch - float(prevEpoch):
                prevEpoch = datestamp
        return f'save_file+{prevEpoch}'
    return files[0]


def get_oldest_file():
    files = get_file_list()
    if type(files) != list:
        return 'no files'

    currentEpoch = time.mktime(datetime.today().timetuple())

    if len(files) > 0:
        oldEpoch = files[0][10:]
        for file in files:
            datestamp = file[10:]
            if currentEpoch - float(datestamp) > currentEpoch - float(oldEpoch):
                oldEpoch = datestamp
        return f'save_file+{oldEpoch}'
    return f'save_file+{files[0][10:]}'


def save_game(game):
    """ creates files up to num10 then asks to overwrite
        create only a limited prev saves """

    if not os.path.exists('./save_dir'):
        os.mkdir('./save_dir')
        return 'no folder'

    files = get_file_list()
    # use a datetime only allow 10 files erase any files that are over ten, the oldest file first
    if len(files) == 0:
        return 'no files found'

    if len(files) > SAVELIMIT:
        # prompt user if overwrite is true
        # create a screen that prompts user to overwrite data

        # if true create new save then del saveLimit
        # remove oldest file
        while len(files) > SAVELIMIT:
            os.remove(f'./save_dir/{get_oldest_file()}')
            files = get_file_list()

    os.chdir('./save_dir')
    save_data = shelve.open(f'save_file+{time.mktime(datetime.today().timetuple())}', 'c')
    # save essential data
    data = {}
    data['gameData'] = {'map': game.mapLevel}
    data['playerData'] = {'stats': game.player.stats, 'pos': game.player.pos}
    data['partyData'] = []
    for obj in game.party:
        # adding the important stats
        data['partyData'].append({'name': obj.name, 'imageFile': obj.imageFile,
                                  'stats': obj.stats, 'max_hp': obj.max_hp,
                                  'id': obj.id_num})

    save_data['game_data'] = data
    save_data.close()
    os.chdir('../')
    return True


def load_game():
    """ reads the database and returns game data then goes to loading for said data """

    # return the required data to start the game where player left off
    if os.path.exists('./save_dir'):
        files = os.listdir('./save_dir')
        save_file = get_newest_file()
        game_data = shelve.open(f'./save_dir/{save_file}', 'r')
        # return the game object
        return game_data['game_data']
    return 'no saves found'


# how to use this module
if __name__ == '__main__':
    class testObj:
        def __init__(self):
            self.name = 'bob'
            self.saveLimit = 10

