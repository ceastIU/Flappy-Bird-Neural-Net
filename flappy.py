from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
import math
# For input lines 275

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 150 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
PIPEDETERMINTISIC = True
DISPLAYSCREEN = True
DISPLAYWELCOME = True
GAMEOVERSCREEN = False
NUMBERBIRDS = 5
FIRST = True
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK, PAUSE
    pygame.init()
    PAUSE = False;
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    IMAGES['ball'] = pygame.image.load('assets/sprites/ball.png').convert_alpha()

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)
    birds = {}
    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        for i in range(NUMBERBIRDS):
            randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
            IMAGES['Bird '+str(i)] = (
                pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
            )
        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hitmask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        for i in range(NUMBERBIRDS):
            HITMASKS['Bird '+str(i)] = (
                getHitmask(IMAGES['Bird '+str(i)][0]),
                getHitmask(IMAGES['Bird '+str(i)][1]),
                getHitmask(IMAGES['Bird '+str(i)][2]),
            )
        movementInfo = showWelcomeAnimation()
        birds_m = mainGame(movementInfo, birds)
        birds = showGameOverScreen(birds_m)
        print("Birds main: ", birds)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    birdIndex = 0
    # Cycles the birds wings
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['Bird '+str(birdIndex)][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 2, 'dir': 1}

    while True:
        if DISPLAYSCREEN:
            SOUNDS['wing'].play()
            return {
                'playery': playery + playerShmVals['val'],
                'basex': 80,
                'playerIndexGen': playerIndexGen,
            }
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': 80,
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            birdIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites

        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['Bird ' + str(0)][birdIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def pause():
    PAUSE = True

    while PAUSE:
        for event in pygame.event.get():
            if event.type == KEYDOWN and (event.key == K_p):
                PAUSE = False

def mainGame(movementInfo, birds):
    score = birdIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    initx, inity = int(SCREENWIDTH * 0.2), movementInfo['playery']
    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]
    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    initVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    initMaxVelY =  10   # max vel along Y, max descend speed
    initMinVelY =  -8   # min vel along Y, max ascend speed
    initAccY    =   1   # players downward accleration
    initRot     =  45   # player's rotation
    initVelRot  =   3   # angular speed
    initRotThr  =  20   # rotation threshold
    initFlapAcc =  -9   # players speed on flapping
    birdFlapped = False # True when player flaps
    printIterator = 0

    crashedBirds = 0    # Number of birds crashed so far
    print("NUMBER birds = ", len(birds))
    if len(birds) == 0:
        birds = generateBirds({}, {}, FIRST, initx, inity, birdIndex, initVelY,initAccY,initRot)
    # for i in range(NUMBERBIRDS):
    #     genetic = random.randint(0, 100)
    #     print(i)
    #     yplus = random.randint(30,90)
    #     birds["Bird " + str(i)] = Bird(initx, inity + yplus, birdIndex, "Bird "+str(i), initVelY,initAccY,initRot,birdFlapped, genetic)
    # #FIRST = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                for bird in birds:
                    bird = birds[bird]
                    if bird.y > -2 * IMAGES[bird.key][0].get_height():
                        bird.velY = bird.flapAcc
                        bird.flapped = True
                        SOUNDS['wing'].play()
            if event.type == KEYDOWN and (event.key == K_p):
                pause()


        # neural_out
        #neural_input_x = playerx - lowerPipes[0]['x'] - 50
        #neural_input_y = playery - lowerPipes[0]['y'] - 50

        ####

        # neural_out = False
        # if playery > lowerPipes[0]['y'] - 50:
        #     playerVelY = playerFlapAcc
        #     playerFlapped = True
        #     SOUNDS['wing'].play()
        bird_passed = False
        for bird in birds:
            bird = birds[bird]
            if bird.moving:
                crashTest = checkCrash(bird, upperPipes, lowerPipes)

            if crashTest[0] and bird.moving:
                print(bird.key, "tuned off")
                bird.moving = False
                bird.distFromOpen = abs((lowerPipes[0]['y'] - PIPEGAPSIZE / 2) - bird.y)
                crashedBirds += 1

            if crashedBirds == len(birds) -1:
                fitness = rankBirdsFitness(birds)
                birds = generateBirds(birds, fitness, False, initx, inity, birdIndex, initVelY, initAccY,initRot)
                print("Birds: ", birds)
                return birds
                # return {
                #     'y': birds["Bird 0"].y,
                #     'groundCrash': crashTest[1],
                #     'basex': basex,
                #     'upperPipes': upperPipes,
                #     'lowerPipes': lowerPipes,
                #     'score': score,
                #     'VelY': birds["Bird 0"].velY,
                #     'Rot': birds["Bird 0"].rot
                # }

            birdMidPos = bird.x + IMAGES[bird.key][0].get_width() / 2
            neural_input_x = lowerPipes[0]['x'] - (IMAGES['pipe'][0].get_width() /4) - bird.x
            if neural_input_x < 0:
                neural_input_x = lowerPipes[1]['x'] - (IMAGES['pipe'][1].get_width() /4) - bird.x
            neural_input_y = (lowerPipes[0]['y'] - PIPEGAPSIZE / 2) - bird.y

            #if bird.y - random.randint(15,55) > lowerPipes[0]['y'] - 50 and bird.moving:
            if bird.flaps(neural_input_x, neural_input_y):
                bird.velY = bird.flapAcc
                bird.flapped = True
                SOUNDS['wing'].play()

            if not bird.moving:
                bird.x += pipeVelX
            else:
                bird.distTraveled -= pipeVelX

            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= birdMidPos < pipeMidPos + 4:
                    if not bird_passed:
                        score += 1
                        bird_passed = True
                        SOUNDS['point'].play()
                    bird.score += 1

            if bird.moving:
                if bird.rot > -90:
                    bird.rot -= bird.velRot
                if bird.velY < bird.maxVelY and not bird.flapped:
                    bird.velY += bird.accY
                if bird.flapped:
                    bird.flapped = False
                    bird.rot = 45

                # more rotation to cover the threshold (calculated in visible rotation)
                #playerRot = 45
                #bird.rot = 45

                bird.height = IMAGES[bird.key][bird.index].get_height()
                bird.y += min(bird.velY, BASEY - bird.y - bird.height)
        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            for bird in birds:
                bird = birds[bird]
                bird.index = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX
        # if printIterator % 30 == 0:
        #     bird = birds["Bird 0"]
        #     print(bird.key)
        #     inputx = upperPipes[0]['x'] - bird.x
        #     inputy = (upperPipes[0]['y'] - lowerPipes[0]['y']) - bird.y
        #     print("Player (x, y) - (", bird.x, ",",bird.y,")")
        #     print('l', lowerPipes[0]['y'])
        #     print('u', upperPipes[0]['y'])
        #     print("Input x", inputx)
        #     print("Input y", inputy)
        # printIterator += 1

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)

        for bird in birds:
            bird = birds[bird]
        # Player rotation has a threshold
            visibleRot = bird.rotThr
            if bird.rot <= bird.rotThr:
                visibleRot = bird.rot
        
            playerSurface = pygame.transform.rotate(IMAGES[bird.key][bird.index], visibleRot)
            SCREEN.blit(playerSurface, (bird.x, bird.y))

        if DISPLAYSCREEN:
            pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(birds):
    """crashes the player down ans shows gameover image"""
    # score = crashInfo['score']
    # playerx = SCREENWIDTH * 0.2
    # playery = crashInfo['y']
    # playerHeight = IMAGES['Bird 0'][0].get_height()
    # playerVelY = crashInfo['VelY']
    # playerAccY = 2
    # playerRot = crashInfo['Rot']
    # playerVelRot = 7
    #
    # basex = crashInfo['basex']
    #
    # upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']
    #
    # # play hit and die sounds
    # SOUNDS['hit'].play()
    # if not crashInfo['groundCrash']:
    #     SOUNDS['die'].play()

    while True:
        if not GAMEOVERSCREEN:
            return birds
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or True:
                return birds
        # # player y shift
        # if playery + playerHeight < BASEY - 1:
        #     playery += min(playerVelY, BASEY - playery - playerHeight)
        #
        # # player velocity change
        # if playerVelY < 15:
        #     playerVelY += playerAccY
        #
        # # rotate only when it's a pipe crash
        # if not crashInfo['groundCrash']:
        #     if playerRot > -90:
        #         playerRot -= playerVelRot
        #
        # # draw sprites
        # SCREEN.blit(IMAGES['background'], (0,0))
        #
        # for uPipe, lPipe in zip(upperPipes, lowerPipes):
        #     SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
        #     SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
        #
        # SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # showScore(score)
        #
        # playerSurface = pygame.transform.rotate(IMAGES['Bird 0'][1], playerRot)
        # SCREEN.blit(playerSurface, (playerx,playery))
        #
        # FPSCLOCK.tick(FPS)
        # pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    if not PIPEDETERMINTISIC:
        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
    else:
        gapY = int(BASEY * 0.2) + 50
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(bird, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    bi = bird.index
    bird.width = IMAGES[bird.key][0].get_width()
    bird.height = IMAGES[bird.key][0].get_height()

    # if player crashes into ground
    if bird.y + bird.height >= BASEY - 1:
        return [True, True]
    else:

        birdRect = pygame.Rect(bird.x, bird.y,
                      bird.width, bird.height)

        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS[bird.key][bi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(birdRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(birdRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                print("COLLIDE")
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def generateBirds(birds, fitness,  FIRST, initx, inity, birdIndex, initVelY,initAccY,initRot ):
    if FIRST:
        for i in range(NUMBERBIRDS):
            genetic = random.randint(0, 100)
            yplus = random.randint(30, 90)
            birds["Bird " + str(i)] = Bird(initx, inity + yplus, birdIndex, "Bird " + str(i), initVelY, initAccY,
                                           initRot, genetic)
    else:
        print("New Gene")
        newGeneration = {}
        winners = fitness[0:4]
        print(winners)
        first = birds[winners[0][0]]
        second = birds[winners[1][0]]
        third = birds[winners[2][0]]
        fourth = birds[winners[3][0]]
        newGeneration['Bird 0'] = first
        first.key = 'Bird 0'
        newGeneration['Bird 1'] = second
        newGeneration['Bird 2'] = third
        newGeneration['Bird 4'] = fourth
        newGeneration['Bird 5'] = Bird(initx, inity, birdIndex, "Bird " + str(5), initVelY, initAccY, initRot, crossOver(first,second))
        birds = newGeneration
        print(newGeneration.keys() )
    for bird in birds:
        print("Bird generate birds", birds[bird].key)
    return birds

def crossOver(bird1, bird2):
    return (bird1.genetic + bird2.genetic) / 2


def rankBirdsFitness(birds):
    fitness = []
    for bird in birds:
        bird = birds[bird]
        if len(fitness) == 0:
            fitness.append((bird.key, bird.calculate_fitness()))
        else:
            inserted = False
            birdFitness = (bird.key, bird.calculate_fitness())
            for i in range(len(fitness)):
                if fitness[i][1] < birdFitness[1]:
                    fitness.insert(i, birdFitness)
                    inserted = True
                print(fitness)
            if not inserted:
                fitness.append(birdFitness)
    return fitness

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask


class Bird:
    def __init__(self,initx, inity, index, key, initVelY,initAccY,initRot,genetic):
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

    def calculate_fitness(self):
        return self.score + self.distTraveled - self.distFromOpen

    def flaps(self, inputX, inputY):
        return inputY + self.genetic < 0
        #return random.random() > .9




if __name__ == '__main__':
    main()
