class Musician(object):
    def __init__(self, sounds):
        self.sounds = sounds

    def solo(self, length):
        for i in range(length):
            print(self.sounds[i % len(self.sounds)], end=" ")
        print()

class Bassist(Musician): # The Musician class is the parent of the Bassist class
    def __init__(self):
        # Call the __init__ method of the parent class
        super().__init__(["Twang", "Thrumb", "Bling"])

class Guitarist(Musician):
    def __init__(self):
        # Call the __init__ method of the parent class
        super().__init__(["Boink", "Bow", "Boom"])

    def tune(self):
        print("Be with you in a moment")
        print("Twoning, sproing, splang")

# Extend the example code to add a Drummer class.
class Drummer(Musician):
    def __init__(self):
        super().__init__(["Boom", "Plow", "Boom"])

# Drummers should be able to solo, count to four, and spontaneously combust.
    def countToFour(self):
        for n in range(1,5):
            print(n)

    def spontaneouslyCombust(self):
        del self

# Then add a Band class.
class Band(Musician):
    def __init__(self):
        super().__init__(["Twang", "splang", "Boom"])

    def hireMusician(self):
        pass

    def fireMusician(self):
        pass

    def playSolos(self):
        self.Drummer.countToFour()
        self.solo(6)



# Bands should be able to hire and fire musicians, and have the musicians play their solos after the drummer has counted time.





if __name__ == '__main__':
    # nigel = Guitarist()
    # nigel.solo(7)
    # print(nigel.sounds)
    nigel = Drummer()
    nigel.spontaneouslyCombust()
    nigel.solo(6)



