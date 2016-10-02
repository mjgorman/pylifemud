class Watch(object):
    def __init__(self):
        self.second = 0
        self.minute = 0
        self.hour = 0
        self.day = 0
        self.month = 1 
        self.year = 1
        
    def __str__(self):
        return "{0} day of the {1} month of the {2} year. {3}:{4}:{5}".format(
            self.day, self.month, self.year, self.hour, self.minute, self.second) 
    
    def update(self):
        self.second += 1

        if self.second == 60:
            self.minute += 1
            self.second = 0
        if self.minute == 60:
            self.hour += 1
            self.minute = 0
            print(self)
        if self.hour == 24:
            self.day += 1
            self.hour = 0
        if self.day == 31:
            self.month += 1
            self.day = 1
        if self.month == 13:
            self.year += 1
            self.month = 1
