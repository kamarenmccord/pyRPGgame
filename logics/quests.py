
from .items import Item

""" contains quest objects """


class Quest:
    """ master quest object """
    def __init__(self, npc_obj, description, rewards, journey, finished=False):
        self.npc = npc_obj  # who initializes the quest
        self.index = 0  # what is the next requirement
        self.description = description
        self.journey = journey  # use a json like format, this will contain all quest requirements
        self.rewards = rewards  # a list of rewards for completion
        self.finished = finished

    def is_finished(self):
        return self.finished

    def grant_rewards(self, party, player):
        """ who may be a person or party """
        for gift in self.rewards.keys():
            if gift == 'xp':
                for plyr in party:
                    plyr.stats['xp'] += self.rewards[gift]

            if gift == 'items':
                for item in self.rewards[gift]:
                    player.inventory.add(item)

            if gift == 'money':
                player.stats['currency'] += self.rewards[gift]


class FirstQuest(Quest):
    def __init__(self):
        description = """ read a book, get some points, easy peasy """
        super().__init__(npc_obj='book', description=description, rewards={'xp': 100}, journey={'start': 0})
