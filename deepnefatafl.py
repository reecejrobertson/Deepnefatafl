#===========================================================================
#  ?                                ABOUT
#  @author         :  Reece Robertson
#  @email          :  reecejrobertson@gmail.com
#  @repo           :  Deepnetafl
#  @createdOn      :  April 14, 2023
#  @description    :  An implementation of Copenhagen Hnefatafl in PyGame.
#===========================================================================

#===========================================================================
#                            Imports and Initialization
#===========================================================================

import pygame

# Define needed global variables
newGame = True
loggedIn = False
miniGame = False

# Define the colors
BLACK      = (0,0,0)
WHITE      = (255,255,255)
GREY       = (128, 128, 128)
DARK       = (64, 64, 64)
LIGHT      = (203, 206, 203)
GREEN      = (0, 128, 0)
LIGHTGREEN = (0, 206, 0)

# Define needed constants
WIDTH       = 65    # Width of each board square
HEIGHT      = 65    # Height of each board square
MARGIN      = 3     # Defines the margin between board squares
NUM_SQUARES = 11    # Defines the number of board squares per side
RADIUS      = 30    # Defines radius of each piece
STROKE      = 3     # Defines the stroke weight for the pieces

# Compute the size of the window
WINDOW_SIZE = [NUM_SQUARES * (WIDTH + MARGIN) + MARGIN,
               NUM_SQUARES * (HEIGHT + MARGIN) + MARGIN]

# Initialize an empty board to start
board = [['.'] * NUM_SQUARES for _ in range(NUM_SQUARES)]

# Define a variable for this distance of the mouse to the edge of the screen
xDFE = 0    # 'xDFE' = 'xDistanceFromEdge'

# Initiate the PyGame screen and clock
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Copenhagen Hnefatafl")
done = False

#===========================================================================
#                            Rendering Functions
#===========================================================================

def boardGui(mainColor, altColor, clickColor, clickRow, clickColumn,
                hoverColor, hoverRow, hoverColumn):
    """_summary_

    Args:
        mainColor (_type_): _description_
        altColor (_type_): _description_
        clickColor (_type_): _description_
        clickRow (_type_): _description_
        clickColumn (_type_): _description_
        hoverColor (_type_): _description_
        hoverRow (_type_): _description_
        hoverColumn (_type_): _description_
    """

    for boardRow in range(NUM_SQUARES):
        for boardColumn in range(NUM_SQUARES):
            xCoordinate = ((MARGIN + WIDTH) * boardColumn + MARGIN) + xDFE
            yCoordinate = (MARGIN + HEIGHT) * boardRow + MARGIN
            color = mainColor
            if ((boardRow == 0 or boardRow == 10) and 
                (boardColumn == 0 or boardColumn == 10)):
                color = altColor
            if (boardRow == 5) and (boardColumn == 5):
                color = altColor
            if (boardRow == hoverRow) and (boardColumn == hoverColumn):
                color = hoverColor
            if (boardRow == clickRow) and (boardColumn == clickColumn):
                color = clickColor
            pygame.draw.rect(screen, color, 
                                [xCoordinate, yCoordinate, WIDTH, HEIGHT])

def piecesGameBoard(board):
    """_summary_

    Args:
        board (_type_): _description_
    """

    if newGame:
        newGameBoard(board)

def newGameBoard(board):
    """_summary_

    Args:
        board (_type_): _description_
    """

    board = [
    ['.', '.', '.', 'B', 'B', 'B', 'B', 'B', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['B', '.', '.', '.', '.', 'W', '.', '.', '.', '.', 'B'],
    ['B', '.', '.', '.', 'W', 'W', 'W', '.', '.', '.', 'B'],
    ['B', 'B', '.', 'W', 'W', 'K', 'W', 'W', '.', 'B', 'B'],
    ['B', '.', '.', '.', 'W', 'W', 'W', '.', '.', '.', 'B'],
    ['B', '.', '.', '.', '.', 'W', '.', '.', '.', '.', 'B'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'B', 'B', 'B', 'B', 'B', '.', '.', '.']
    ]

    drawPieces(board, BLACK, WHITE)

def drawPieces(board, black, white):
    """_summary_

    Args:
        board (_type_): _description_
        black (_type_): _description_
        white (_type_): _description_
    """

    for x in range(NUM_SQUARES):
        for y in range(NUM_SQUARES):
            xCoord = ((MARGIN + WIDTH) * x + MARGIN + 32) + xDFE
            yCoord = (MARGIN + HEIGHT) * y + MARGIN + 33
            if board[x][y] == 'B':
                pygame.draw.circle(screen, black,
                                    (xCoord, yCoord), RADIUS)
                pygame.draw.circle(screen, white,
                                    (xCoord, yCoord), RADIUS, STROKE)
            if (board[x][y] == 'W') or (board[x][y] == 'K'):
                pygame.draw.circle(screen, white,
                                    (xCoord, yCoord), RADIUS)
                pygame.draw.circle(screen, black,
                                    (xCoord, yCoord), RADIUS, STROKE)
                if board[x][y] == 'K':
                    pygame.draw.line(screen, black, (xCoord - RADIUS, yCoord),
                                        (xCoord + RADIUS, yCoord), STROKE)
                    pygame.draw.line(screen, black, (xCoord, yCoord - RADIUS),
                                        (xCoord, yCoord + RADIUS), STROKE)

#===========================================================================
#                            Event Handler Helpers
#===========================================================================

clickRow = None
clickColumn = None
hoverRow = None
hoverColumn = None

def computeRowAndColumn(pos):
    """_summary_

    Args:
        pos (_type_): _description_

    Returns:
        _type_: _description_
    """

    row = pos[1] // (HEIGHT + MARGIN)
    column = (pos[0] - xDFE) // (WIDTH + MARGIN)
    return row, column

#===========================================================================
#                            Main Program Loop
#===========================================================================

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clickRow, clickColumn = computeRowAndColumn(pos)
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            hoverRow, hoverColumn = computeRowAndColumn(pos)

    screen.fill(LIGHT)
    boardGui(GREY, DARK, GREEN, clickRow, clickColumn,
                LIGHTGREEN, hoverRow, hoverColumn)
    piecesGameBoard(board)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()