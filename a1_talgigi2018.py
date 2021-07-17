from math import inf as infinity
from random import choice


#Tree of the Romania Map
#Name of the city followed by an array of conections [distance, name]\
map = {
    'Oradea':{'Zerind':71,'Sibiu': 151},
    'Zerind':{'Oradea':71, 'Arad':75},
    'Arad':{'Zerind':75,'Sibiu':140,'Timisoara':118},
    'Timisoara':{'Arad':118,'Lugoj':111},
    'Lugoj':{'Timisoara':111,'Mehadia':70},
    'Mehadia':{'Lugoj':70,'Dobreta':75},
    'Dobreta':{'Mehadia':75,'Craiova':120},
    'Sibiu':{'Oradea':151,'Arad':140,'Rimnicu Vilcea':80,'Fagaras':99},
    'Rimnicu Vilcea':{'Sibiu':80,'Pitesti':97,'Craiova':146},
    'Craiova':{'Rimnicu Vilcea':146,'Pitesti':138},
    'Fagaras':{'Sibiu':99,'Bucharest':211},
    'Pitesti':{'Rimnicu Vilcea':97,'Bucharest':101,'Craiova':138},
    'Bucharest':{"Fagaras":211,'Bucharest':101,'Giurgiu':90,'Urziceni':85},
    'Giurgiu':{'Bucharest':90},
    'Urziceni':{'Bucharest':85,'Hirsova':98,'Vaslui':142},
    'Hirsova':{'Urziceni':98,'Eforie':86},
    'Eforie':{'Hirsova':86},
    'Vaslui':{'Urziceni':142,'Iasi':92},
    'Iasi':{'Vaslui':92,'Neamt':87},
    'Neamt':{'Iasi':87}
}

#Straight Line Value
slv = {
    'Arad': 366,
    'Bucharest': 0,
    'Craiova': 160,
    'Dobreta':242,
    'Eforie':161,
    'Fagaras':176,
    'Giurgiu':77,
    'Hirsova':151,
    'Iasi': 226,
    'Lugoj': 244,
    'Mehadia':241,
    'Neamt': 234,
    'Oradea':380,
    'Pitesti':100,
    'Rimnicu Vilcea':193,
    'Sibiu':253,
    'Timisoara':329,
    'Urziceni':80,
    'Vaslui':199,
    'Zerind':374
}



HUMAN = -1
AI = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(board):
    if wins(board, AI):
        score = +1
    elif wins(board, HUMAN):
        score = -1
    else:
        score = 0

    return score

def wins(boardState, player):
    """
        This functions checks to see if a player has won 
        by checking all possible winning combinations
    """
    win_state = [
        [boardState[0][0], boardState[0][1], boardState[0][2]],
        [boardState[1][0], boardState[1][1], boardState[1][2]],
        [boardState[2][0], boardState[2][1], boardState[2][2]],
        [boardState[0][0], boardState[1][0], boardState[2][0]],
        [boardState[0][1], boardState[1][1], boardState[2][1]],
        [boardState[0][2], boardState[1][2], boardState[2][2]],
        [boardState[0][0], boardState[1][1], boardState[2][2]],
        [boardState[2][0], boardState[1][1], boardState[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
        Setting move into the board array.
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
        Minimax algorithm runs to determine which play for the AI player
        has the best "score". The score is determined by prediciting the outcome of later possible moves 
        inputs:
            board - 2D array representing a tic tac toe board
            depth - The number of times the Recurive function will run to
            player - -1 or 1 to determine which player is player
    """
    
    if player == AI:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or wins(state, HUMAN) or wins(state, AI):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == AI:
            if score[2] > best[2]:
                best = score 
        else:
            if score[2] < best[2]:
                best = score  

    return best

def printBoard(board, ai_letter, human_letter):
    """
        This functons prints the current board
        inputs:
            board- 2D array representing a tic tac toe board
            ai_letter/human_letter - String that represents if they are X or o
    """
    chars = {
        -1: human_letter,
        +1: ai_letter,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    print("1-3\t  {}  |  {}  |  {}".format(chars[board[0][0]], chars[board[0][1]], chars[board[0][2]]))
    print(' \t_____|_____|_____')
 
    print(" \t     |     |")
    print("4-6\t  {}  |  {}  |  {}".format(chars[board[1][0]], chars[board[1][1]], chars[board[1][2]]))
    print(' \t_____|_____|_____')
 
    print(" \t     |     |")
 
    print("7-9\t  {}  |  {}  |  {}".format(chars[board[2][0]], chars[board[2][1]], chars[board[2][2]]))
    print(" \t     |     |")
    print('\n' + str_line)
    

def ai_turn(ai_letter, human_letter):
    """
        This function is what runs when it is the AI turn
        Check to see if the game is over 
        Then runs the minimax algo to see which postion if the best 
        inputs: 
            ai_letter/human_letter - String that represents if they are X or o
    """
    depth = len(empty_cells(board))
    if depth == 0 or wins(board, HUMAN) or wins(board, AI):
        return

    print("AI Choosing")
    printBoard(board, ai_letter, human_letter)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, AI)
        x, y = move[0], move[1]

    if valid_move(x, y):
        board[x][y] = AI


def human_turn(ai_letter, human_letter):
    """
        This function is what runs when it is the humans turn
        Check to see if the game is over 
        then as for an input 1-9 to place thier X
        inputs: 
            ai_letter/human_letter - String that represents if they are X or o
    """
    depth = len(empty_cells(board))
    if depth == 0 or wins(board, HUMAN) or wins(board, AI):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    printBoard(board, ai_letter, human_letter)

    while move < 1 or move > 9:
        try:
            move = int(input('Select a position 1-9: '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except KeyError or ValueError as e:
            print('Bad choice: ' + e)

def clearBoard():
    global board
    board = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],]
    
    
def tictactoe():
    """
        This is the main function for TicTacToe Game
        A hunman will play against an AI using the minimax algo
    """
    clearBoard()
    human_letter = 'X' 
    ai_letter = 'O'  
    print("\nWelcome to Tic Tac Toe where you will be playing an AI!\nYou will be X and the AI will be O.\nOnce the game starts select a x (1-3) and y (1-3) position on the board to place your X on the board.\n")
    runAgain = ""
    
    while runAgain != "Y" or runAgain != "y":
        
        while len(empty_cells(board)) > 0 and not wins(board, HUMAN) and not wins(board, AI):
            human_turn(ai_letter, human_letter)
            ai_turn(ai_letter, human_letter)

        if wins(board, HUMAN):
            printBoard(board, ai_letter, human_letter)
            print('YOU WIN!')
        elif wins(board, AI):
            printBoard(board, ai_letter, human_letter)
            print('YOU LOSE!')
        else:
            printBoard(board, ai_letter, human_letter)
            print('DRAW!')

        runAgain = input('Would you like to run again? (Y/N): ')
        if runAgain == "Y" or runAgain == "y":
            tictactoe()
            
        else:
            exit()
            
#############################################           
#Shortest Route Functions below
#############################################

def a_star(startNode, endNode):
    """
        A* search alogthirm 
        inputs:
            Start node - name of the city the path will start from
            endNode - name of the city the path will end at (always Bucharest) 
    """
    path = []
    q = []
    q.append(startNode)
    
    while q is not []:
        currentNode = q.pop(0)
        path.append(currentNode)
        children = list(map[currentNode].keys())
        if endNode in children:
            path.append(endNode)
            return path
        
        shortest_distance = children[0]
        for node in children:
            if slv[node] + map[currentNode][node] < slv[shortest_distance] + map[currentNode][shortest_distance] :
                shortest_distance = node
        q.append(shortest_distance)

def bfs_total(path):
    total = 0
    for i in range(0, len(path)-1):
        try:
            length = map[path[i]][path[i+1]]
            total = total + length
        except IndexError as e:
            print(e)
    return total


def BFS(startNode, endNode):
    """
        Breath for search alogthirm 
        inputs:
            Start node - name of the city the path will start from
            endNode - name of the city the path will end at (always Bucharest) 
    """
    path = []
    q = []
    q.append(startNode)
    parent = [startNode]
    unvisited = list(map.keys())
    unvisited.remove(startNode)
    while q != []:
        currentNode = q.pop(0)
        path.append(currentNode)
        adjacent = list(map[currentNode].keys())
        if endNode in adjacent:
            path.append(endNode)
            break
        for node in adjacent:
            if node in unvisited:
                q.append(node)
                unvisited.remove(node)
    
    temp = []
    temp.append(path[len(path)-1])
    currentNode = path[len(path)-1]
    for i in range(len(path)-1, -1, -1):
        if currentNode in list(map[path[i-1]].keys()):
            currentNode = path[i-1]
            temp = [path[i-1]] + temp
    
    path = temp
    
    return path
                

#Greedy BFS
"""
def BFS(startNode, endNode):
    path = []
    q = []
    q.append(startNode)
    
    while q is not []:
        currentNode = q.pop(0)
        path.append(currentNode)
        children = list(map[currentNode].keys())
        if endNode in children:
            path.append(endNode)
            return path
        
        shortest_distance = children[0]
        for node in children:
            if slv[node] < slv[shortest_distance]:
                shortest_distance = node
        q.append(shortest_distance)
"""

def children(visted, startNode, endNode, path):
    """
        Recurive function to find the childern of each node 
        for Depth for search alogthirm
        inputs:
            Start node - name of the city the path will start from
            endNode - name of the city the path will end at (always Bucharest) 
            path - array of names in the path
            visited = array of all already visitied cities 
    """
    if startNode not in visted:
        if endNode in startNode:
            visted.append(startNode)
            return visted
        elif endNode in visted:
            return visted
        else:
            visted.append(startNode)
        for node in list(map[startNode].keys()):
            children(visted, node, endNode, path)
    return visted
    

def DFS(startNode, endNode):
    """
        Depth for search alogthirm 
        inputs:
            Start node - name of the city the path will start from
            endNode - name of the city the path will end at (always Bucharest) 
    """
    path = []
    visted = []
    path.append(startNode)
    return children(visted, startNode, endNode, path)
   
   
def totalPath(path):
    """
        returns the total of all edges in the path
        input: a array of connected city names
    """
    total = 0
    for i in range(0, len(path)-1):
        length = map[path[i]][path[i+1]]
        total = total + length
    return total

def shortest_route():
    """
        This is the main function for the shortest route problem.
        Asks for the city name input and checks if it exists
        Asks for what algorithm to use and checks if exists
    """
    #Starting statement
    print("##############################\n\n The Shortest Route \n This app implements 3 searching algorthirms (A*, BFS, DFS) to find \n the shortest route to the destination of Bucharest. \n\n##############################")

    cityName = input("What city would you like to depart from? ")
    #TODO:Check if city name exists
    while cityName not in map.keys():
        cityName = input("Please enter a valid city name: ")
    
    algo = input("What algorithm would you like to use? (A/B/D for A*/BFS/DFS)")
    while algo not in ["A", "B", "D"]:
        algo = input('Please enter a A/B/D for A*/BFS/DFS: ')\

    if algo == "A":
        path= a_star(cityName, 'Bucharest')
        print("Using A* the path is: " + str(path))
        print("With a total of " + str(len(path)) + " iterations")
        for i in range(0, len(path)-1):
            print(str(path[i]) + " " + str(map[path[i]][path[i+1]]) + " to")
        print("With a total length of: " + str(totalPath(path)))
        
    elif algo == "B":
        path= BFS(cityName, 'Bucharest')
        print("Using BFS the path is: " + str(path))
        for i in range(0, len(path)-1):
            print(str(path[i]) + " " + str(map[path[i]][path[i+1]]) + " to")
        print("With a total length of: " + str(totalPath(path)))
        print("With a total of " + str(len(path)) + " iterations")
        
    else:
        path= DFS(cityName, 'Bucharest')
        print("Using DFS the path is: " + str(path))
        print("With a total of " + str(len(path)) + " iterations")
        for i in range(0, len(path)-1):
            print(str(path[i]) + " " + str(map[path[i]][path[i+1]]) + " to")
        print("With a total length of: " + str(totalPath(path)))
        
    runAgain = input('Would you like to run again? (Y/N): ')
    if runAgain == "Y" or runAgain == "y":
        shortest_route()
    else:
        print("ending...")
        


def main():
    """
        Comment off the function you would NOT like to run
    """
    shortest_route()
    #tictactoe()
    
main()