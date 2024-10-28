# IMPORTS
import random
import pygame
import time

from requests import session



# GLOBAL CONSTANTS
winVal = 2048

WIDTH = 745
HEIGHT = 945

blck_sz = 150
blck_indent = 15

start_x = 50
start_y = 250

"""
directions
"""
UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6



# FONT SIZES
smallFontSz = 50
fontSz = 100
titleFontSz = 160



# COLOUR FORMATS
txt_clr1 = (119, 110, 101)
txt_clr2 = (225, 225, 225)

clrList = {
       0: (205, 193, 180),
       2: (238, 228, 218),
       4: (237, 224, 200),
       8: (242, 177, 121),
      16: (245, 149,  99),
      32: (246, 124,  95),
      64: (246,  94,  59),
     128: (237, 207, 114),
     256: (237, 204,  97),
     512: (237, 200,  80),
    1024: (237, 197,  63),
    2048: (237, 194,  46),
    4096: ( 60,  58,  50),
    8192: ( 60,  58,  50)     # (no., ( R, G, B)), 0 for bg
    }



# FUNCTIONS
def resetGrid():
    grd = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]

    for x in range(0, 2):    
        addNewBlock(grd)

    return grd

def updateBest(scr):
    
    best = scr
    best_file.truncate(0)
    best_file.write(str(scr))

def hasWon(grd):

    """
    returns true if the player has won
    false otherwise
    """

    for r in range(len(grd)):
        for c in range(len(grd[r])):
            if grd[r][c] == winVal:
                return True

    return False
            
def inBounds(grid, row, col):

    """
    returns true if the specific block coords are in bounds of the grid
    """

    return ((len(grid) > row >= 0) and (len(grid[row]) > col >= 0))

def genBlock(grd):
    
    """
    finds a random empty block in a given 2D grid
    """
    
    blck = ( random.randrange( 0, len(grd)), random.randrange( 0, len(grd)))
    while grd[blck[0]][blck[1]] != 0 :
        blck = genBlock(grd)

    return blck

def setBlock(grd, blck, val):

    """
    sets the given value in the grid in the specified block
    """
    
    grd[blck[0]][blck[1]] = val

def addNewBlock(grd):

    """
    add a new block
    to the grid
    in a random position
    with the no. 2 and a 10% chance of being 4
    """
    
    newBlck = genBlock(grd)

    if (random.randrange(0,10)) == 9:
        newVal = 4
    else :
        newVal = 2
        
    setBlock(grd, newBlck, newVal)

def shiftBlock(grd, r_from, c_from, r_to, c_to):

    """
    shifts the elements of one grid block to another
    """
    
    grd[r_to][c_to] = grd[r_from][c_from]
    grd[r_from][c_from] = 0
    
def shiftGrid(grd, direction):

    """
    shifts each element in the grid to a specified direction
    """

    if direction == UP:
        for r in range(len(grd)):
            for c in range(len(grd[r])):

                if (inBounds(grd, r-1, c)): 
                    if (grd[r-1][c] == 0):
                        shiftBlock(grd, r, c, r-1, c)
                        
                        if (inBounds(grd, r-2, c)):
                            if (grd[r-2][c] == 0):
                                shiftBlock(grd, r-1, c, r-2, c)

                                if (inBounds(grd, r-3, c)):
                                    if (grd[r-3][c] == 0):
                                        shiftBlock(grd, r-2, c, r-3, c)
                            
    
    elif direction == DOWN:
        for r in range(len(grd)-1, -1, -1):
            for c in range(len(grd[r])):

                if (inBounds(grd, r+1, c)): 
                    if (grd[r+1][c] == 0):
                        shiftBlock(grd, r, c, r+1, c)
                        
                        if (inBounds(grd, r+2, c)):
                            if (grd[r+2][c] == 0):
                                shiftBlock(grd, r+1, c, r+2, c)

                                if (inBounds(grd, r+3, c)):
                                    if (grd[r+3][c] == 0):
                                        shiftBlock(grd, r+2, c, r+3, c)

    elif direction == RIGHT:
        for r in range(len(grd)):
            for c in range(len(grd[r])-1, -1, -1):

                if (inBounds(grd, r, c+1)): 
                    if (grd[r][c+1] == 0):
                        shiftBlock(grd, r, c, r, c+1)
                        
                        if (inBounds(grd, r, c+2)):
                            if (grd[r][c+2] == 0):
                                shiftBlock(grd, r, c+1, r, c+2)

                                if (inBounds(grd, r, c+3)):
                                    if (grd[r][c+3] == 0):
                                        shiftBlock(grd, r, c+2, r, c+3)

    elif direction == LEFT:
        for r in range(len(grd)):
            for c in range(len(grd[r])):

                if (inBounds(grd, r, c-1)): 
                    if (grd[r][c-1] == 0):
                        shiftBlock(grd, r, c, r, c-1)
                        
                        if (inBounds(grd, r, c-2)):
                            if (grd[r][c-2] == 0):
                                shiftBlock(grd, r, c-1, r, c-2)

                                if (inBounds(grd, r, c-3)):
                                    if (grd[r][c-3] == 0):
                                        shiftBlock(grd, r, c-2, r, c-3)

def mergeBlock(grd, r_from, c_from, r_to, c_to):

    """
    merges the elements of two given blocks
    """
    
    val = grd[r_from][c_from] + grd[r_to][c_to]
    
    grd[r_from][c_from] = 0
    grd[r_to][c_to] = val

def mergeGrid(grd, direction, scr):

    """
    merges consecutive elements in a give direction
    """
    
    if direction == UP:
        for r in range(len(grd)):
            for c in range(len(grd[r])):

                if (inBounds(grd, r+1, c)):
                    if (grd[r][c] == grd[r+1][c]):
                        mergeBlock(grd, r+1, c, r, c)
                        scr = scr + (grd[r][c])

    elif direction == DOWN:
        for r in range(len(grd)-1, -1, -1):
            for c in range(len(grd[r])):

                if (inBounds(grd, r-1, c)):
                    if (grd[r][c] == grd[r-1][c]):
                        mergeBlock(grd, r-1, c, r, c)
                        scr = scr + (grd[r][c])

    elif direction == RIGHT:
        for r in range(len(grd)):
            for c in range(len(grd[r])-1, -1, -1):

                if (inBounds(grd, r, c-1)):
                    if (grd[r][c] == grd[r][c-1]):
                        mergeBlock(grd, r, c-1, r, c)
                        scr = scr + (grd[r][c])

    elif direction == LEFT:
        for r in range(len(grd)):
            for c in range(len(grd[r])):

                if (inBounds(grd, r, c+1)):
                    if (grd[r][c] == grd[r][c+1]):
                        mergeBlock(grd, r, c+1, r, c)
                        scr = scr + (grd[r][c])

    return scr
        
def drawWin(win, grd, score):

    """
    updates the pygame win based on the current grid situation
    """

    win.fill((250, 248, 239))

    pygame.draw.rect(win, (187, 173, 160), (start_x - blck_indent, start_y - blck_indent, (blck_sz*4) + (blck_indent*5), (blck_sz*4) + (blck_indent*5)), border_radius = 15)

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', fontSz)
    title_font = pygame.font.SysFont('comicsans', titleFontSz)
    small_font = pygame.font.SysFont('comicsans', smallFontSz)

    title = title_font.render("2048", 1, txt_clr1)
    
    pygame.draw.rect(win, clrList[2], (start_x - blck_indent - 10, 20, title.get_width() + 20, title.get_height() + 20), border_radius = 10)

    win.blit(title, (start_x - blck_indent, 35))

    for r in range(0, len(grd)):
        for c in range(0, len(grd[r])):
            target_x = (start_x + c * blck_sz + c * blck_indent)
            target_y = (start_y + r * blck_sz + r * blck_indent)
            
            pygame.draw.rect(win, clrList[grd[r][c]], (target_x, target_y, blck_sz, blck_sz))
            if (grd[r][c] != 0) :
                if (grd[r][c] == 2 or grd[r][c] == 4):
                    blck_lbl = font.render(str(grd[r][c]), 1, txt_clr1)
                    win.blit(blck_lbl, (target_x + (blck_sz/2) - (blck_lbl.get_width()/2), target_y + (blck_sz/2) - (blck_lbl.get_height()/2)) )
                else :  
                    blck_lbl = font.render(str(grd[r][c]), 1, txt_clr2)
                    win.blit(blck_lbl, (target_x + (blck_sz/2) - (blck_lbl.get_width()/2), target_y + (blck_sz/2) - (blck_lbl.get_height()/2)) )
                


# CHECKS

def canMove(grd, direction):

    """
    Checks if the current grid can move in a certain direction to avoid it from reaching maximum recursion depth
    """

    if direction == RIGHT:
        for r in range(len(grd)):
            for c in range(len(grd[r])-2, -1, -1):
                if ((grd[r][c+1] == 0) and (grd[r][c] != 0)):
                    return True
                elif ((grd[r][c] == grd[r][c+1]) and (grd[r][c] != 0)):
                    return True
                else:
                    pass

    elif direction == LEFT:
        for r in range(len(grd)):
            for c in range(1, len(grd[r])):
                if ((grd[r][c-1] == 0) and (grd[r][c] != 0)):
                    return True
                elif ((grd[r][c] == grd[r][c-1]) and (grd[r][c] != 0)):
                    return True
                else:
                    pass

    elif direction == UP:
        for r in range(1,len(grd)):
            for c in range(len(grd[r])):
                if ((grd[r-1][c] == 0) and (grd[r][c] != 0)):
                    return True
                elif ((grd[r][c] == grd[r-1][c]) and (grd[r][c] != 0)):
                    return True
                else:
                    pass

    elif direction == DOWN:   
        for r in range(len(grd)-2, -1, -1):
            for c in range(len(grd[r])):
                if ((grd[r+1][c] == 0) and (grd[r][c] != 0)):
                    return True
                elif ((grd[r][c] == grd[r+1][c]) and (grd[r][c] != 0)):
                    return True
                else:
                    pass

    return False

def cannotMove(grd):
    return (canMove(grd, UP) == False and canMove(grd, DOWN) == False and canMove(grd, LEFT) == False and canMove(grd, RIGHT) == False)



# INITIALIZE
grid = resetGrid()

win = pygame.display.set_mode(( WIDTH, HEIGHT))
pygame.display.set_caption("2048")

run = True
score = 0



# MAIN
while run:
    if hasWon(grid) :
        score = 0
        run = False

    elif cannotMove(grid):
        time.sleep(5)
        run = False

    else:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP) :
                        if canMove(grid, UP):
                            shiftGrid(grid, UP)
                            score = mergeGrid(grid, UP, score)
                            shiftGrid(grid, UP)
                            addNewBlock(grid)
                    elif (event.key == pygame.K_DOWN) :
                        if canMove(grid, DOWN):
                            shiftGrid(grid, DOWN)
                            score = mergeGrid(grid, DOWN, score)
                            shiftGrid(grid, DOWN)
                            addNewBlock(grid)
                    elif (event.key == pygame.K_LEFT) :
                        if canMove(grid, LEFT):
                            shiftGrid(grid, LEFT)
                            score = mergeGrid(grid, LEFT, score)
                            shiftGrid(grid, LEFT)
                            addNewBlock(grid)
                    elif (event.key == pygame.K_RIGHT) :
                        if canMove(grid, RIGHT):
                            shiftGrid(grid, RIGHT)
                            score = mergeGrid(grid, RIGHT, score)
                            shiftGrid(grid, RIGHT)
                            addNewBlock(grid)
    
    drawWin(win, grid, score)
    pygame.display.update()

pygame.display.quit()
print(f"You won with a score of {score}") if hasWon(grid) else print(f"you lost with a score of {score}")
