import random

from testneural import Net


class Bird:
    def __init__(self,initx, inity, index, key, initVelY,initAccY,initRot,genetic):
        n_inputs = 2
        n_outputs = 1
        #
        self.x              = initx
        self.y              = inity
        self.key            = key
        self.index          = index
        self.width          = 0
        self.height         = 0
        self.moving         = True
        self.velY           = initVelY
        self.maxVelY        = 10   # max vel along Y, max descend speed
        self.minVelY        = -8   # min vel along Y, max ascend speed
        self.accY           = initAccY
        self.rot            = initRot
        self.velRot         = 3   # angular speed
        self.rotThr         = 20   # rotation threshold
        self.flapAcc        = -9   # players speed on flapping
        self.flapped        = True
        self.score          = 0
        self.distTraveled   = 0
        self.distFromOpen   = 0
        self.genetic        = genetic
        self.network        = Net(n_inputs, n_outputs, genetic)

    def calculate_fitness(self):
        return self.score + self.distTraveled - self.distFromOpen

    def flaps(self, inputX, inputY):
        flaps = self.network.propagate((inputX, inputY))[0]
        if self.key == "Bird 0":
            print("Output ", flaps)
        return flaps < .535
        #return random.random() > .9
