
class Inventory:
    # default class for the players inventory
    def __init__(self):
        self.all_pockets = {'misc': [], 'key_items': [], 'healing': [], 'weapons': []}

    def __str__(self):
        a_list = []
        for each, item in self.all_pockets.items():
            a_list.append((each, item))

        return f'{a_list}'

    def add(self, something):
        # add something to a given pocket
        for key, value in something.items():
            for pocket, contents in self.all_pockets.items():
                if key == pocket:
                    pocket.contents.append(value)
