from random import randint

class Character(object):
    def __init__(self, name, load=False):
        self.name = name
        self.password = ""
        self.sex = 'Male'
        self.understanding = 0
        self.diligence = 0
        self.courage = 0
        self.knowledge = 0
        self.expression = 0
        self.weight = randint(100, 115)
        self.height = randint(60, 65)
        if not load:
            print("Player {0} Created..".format(self.name))

    def __str__(self):
      return "{0}".format(self.name)
