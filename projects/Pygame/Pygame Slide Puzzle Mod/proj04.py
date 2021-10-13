# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Student: Simon X Camilo
# Professor: Redacted
# Class: Redacted

# Features of mod: Fullscreen(f), Design change, music(m to mute), volume, sound effects, scores, easter

# Reset = gets the game to where it started, but the solution would be the same
# Start a new game = will start a game completely from the beggining, and the solution will change

### This table of contents doesn't work that much. Kind of useless

from win32api import GetSystemMetrics
import pygame, sys, random
from pygame.locals import *
from pygame import mixer

### Quick shortcuts to change game ###

# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 80 # Size of the squares, the main game (not the menu)
# Window Size
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
# Full screen sizes
FULLWIDTH = GetSystemMetrics(0)
FULLHEIGHT = GetSystemMetrics(1)
FULLTILESIZE = TILESIZE * int(FULLWIDTH/720)
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
NIGHT =         (  0,   0,  20)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
RED =           (255,  31,  41)
GRAY =          ( 50,  50,  50)
SUBTLEGREEN =   (  0,  10,   0)

BGCOLOR = NIGHT
TILECOLOR = RED
TEXTCOLOR = WHITE
BORDERCOLOR = BLACK
BASICFONTSIZE = 20 # also the size of the square
FULLFONTSIZE = BASICFONTSIZE * int(FULLWIDTH/720)

BUTTONCOLOR = RED
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = RED

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# press w 10 times simultaneously to change music

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# plays music the moment you open the game
mixer.init() 
pygame.mixer.music.load('proj04.ogg') #Place the music you want on the same folder as the game, and change the name so it matches
pygame.mixer.music.play(-1)

### core game and a lot of stuff ###

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, FULLSCREEN, MUSIC, VOLUME, WELCOME, score, EASTER

    ### Game display ###

    pygame.init()
    EASTER = 0
    WELCOME = True
    FULLSCREEN = False
    MUSIC = True
    VOLUME = 1.0
    score = 0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state.
    allMoves = [] # list of moves made from the solved configuration

    while True: # main game loop
    ### You win v ###
        slideTo = None # the direction, if any, a tile should slide
        if WELCOME:
            msg = 'Click or use arrow keys to slide, F for fullscreen, M to mute, -+ to change volume' # contains the message that shows at the top.
        else:
            msg = 'score: '+str(score)
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved! Your score is '+str(score)
            
        drawBoard(mainBoard, msg)

    ### Game user actions ###

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

    ### button presses ###
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
                        allMoves = []
                        score = 0
                        EASTER = 0
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                        allMoves = []
                else:
    ### mouse controls ###
                    # check if the clicked tile was next to the blank spot
                    score = score + 1
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

    ### Gets key that was pressed ###

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                score = score + 1
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    WELCOME = False
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sample_0007.wav'))
                    slideTo = LEFT
                    EASTER = 0
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    WELCOME = False
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sample_0007.wav'))
                    slideTo = RIGHT
                    EASTER = 0
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    WELCOME = False
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sample_0007.wav'))
                    slideTo = UP
                    if event.key in (K_w, K_w):
                        EASTER = EASTER + 1
                        if EASTER == 10:
                            score = score - 10
                            pygame.mixer.music.load('calm4.ogg')
                            pygame.mixer.music.play(-1)
                            EASTER = -100
                    else:
                        EASTER = 0
                elif event.key in (K_w, K_w):
                        WELCOME = False
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sample_0006.wav'))
                        EASTER = EASTER + 1
                        if EASTER == 10:
                            score = score - 10
                            pygame.mixer.music.load('calm4.ogg')
                            pygame.mixer.music.play(-1)
                            EASTER = -100
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    WELCOME = False
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sample_0007.wav'))
                    slideTo = DOWN
                    EASTER = 0
                # checks if the user wants the game to be fullscreen, and makes it fullscreen
                elif event.key in (K_f, K_F11):
                    score = score - 1
                    if not FULLSCREEN: # Turns fullscreen
                        FULLSCREEN = True
                        
                        XMARGIN = int((FULLWIDTH - (FULLTILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int((FULLHEIGHT - (FULLTILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        
                        DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        BASICFONT = pygame.font.Font('freesansbold.ttf', FULLFONTSIZE)

                        # Store the option buttons and their rectangles in OPTIONS.
                        # note: It sets the position (not the size)
                        RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, FULLWIDTH - 120 - (FULLFONTSIZE*3), FULLHEIGHT - 90 - (FULLFONTSIZE*2.5))
                        NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, FULLWIDTH - 120 - (FULLFONTSIZE*3), FULLHEIGHT - 60 - (FULLFONTSIZE*2))
                        SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, FULLWIDTH - 120 - (FULLFONTSIZE*3), FULLHEIGHT - 30 - (FULLFONTSIZE*1.5))
                        
                        drawBoard(mainBoard, msg)
                    elif FULLSCREEN: # Turns windowed
                        FULLSCREEN = False
                        
                        XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
                        YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
                        
                        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

                        # Store the option buttons and their rectangles in OPTIONS.
                        RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
                        NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
                        SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
                        
                        drawBoard(mainBoard, msg)
                # Music
                elif event.key in (K_m, K_m):
                    score = score - 1
                    if MUSIC: # Pauses music
                        MUSIC = False
                        pygame.mixer.music.pause()
                    elif not MUSIC: # Resumes music fadingm in
                        MUSIC = True
                        pygame.mixer.music.unpause()
                #change volume
                elif event.key in (K_EQUALS, K_KP_PLUS):
                    score = score - 1
                    VOLUME = VOLUME + 0.1
                    pygame.mixer.music.set_volume(VOLUME)
                    pygame.mixer.Channel(1).set_volume(VOLUME)
                    pygame.mixer.Channel(2).set_volume(VOLUME)
                elif event.key in (K_MINUS, K_KP_MINUS):
                    score = score - 1
                    VOLUME = VOLUME - 0.1
                    pygame.mixer.music.set_volume(VOLUME)
                    pygame.mixer.Channel(1).set_volume(VOLUME)
                    pygame.mixer.Channel(2).set_volume(VOLUME)
                else:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('Sample_0006.wav'))


        if slideTo:
            slideAnimation(mainBoard, slideTo, 'score: '+str(score), 8) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#Quit game

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

### Solves the game ###

def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board

### Tells the game what square is blank ###

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)

### so... This just moves the square I guess. ###

def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    if FULLSCREEN:
        left = XMARGIN + (tileX * FULLTILESIZE) + (tileX - 1)
        top = YMARGIN + (tileY * FULLTILESIZE) + (tileY - 1)
        return (left, top)
    elif not FULLSCREEN:
        left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
        top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
        return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            if FULLSCREEN:
                tileRect = pygame.Rect(left, top, FULLTILESIZE, FULLTILESIZE)
            elif not FULLSCREEN:
                        tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    if FULLSCREEN:
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, FULLTILESIZE, FULLTILESIZE))
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(FULLTILESIZE / 2) + adjx, top + int(FULLTILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)
    elif not FULLSCREEN:
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
        textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    if FULLSCREEN:
        width = BOARDWIDTH * FULLTILESIZE
        height = BOARDHEIGHT * FULLTILESIZE
    elif not FULLSCREEN:
        width = BOARDWIDTH * TILESIZE
        height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

### stars a new game ###

def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()