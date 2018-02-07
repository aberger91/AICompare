

def minimax(node, index, search, is_max, depth):
    '''
    Minimax is a kind of backtracking algorithm that is used in decision making and game theory 
    to find the optimal move for a player, assuming that your opponent also plays optimally. 
    It is widely used in two player turn based games such as Tic-Tac-Toe, Backgamon, Mancala, Chess, etc.

    In Minimax the two players are called maximizer and minimizer. 
    The maximizer tries to get the highest score possible while the minimizer tries to get the 
    lowest score possible while minimizer tries to do opposite.

    Every board state has a value associated with it. 
    In a given state if the maximizer has upper hand then, the score of the board will tend to be some positive value. 
    If the minimizer has the upper hand in that board state then it will tend to be some negative value. 
    The values of the board are calculated by some heuristics which are unique for every type of game.
    '''
    if node == depth:
        return search[ node ]
    
    if is_max:
        return max( minimax(node+1, index*2, search, False, depth),
                    minimax(node+1, index*2+1, search, False, depth) )
    else:
        return min( minimax(node+1, index*2, search, True, depth),
                    minimax(node+1, index*2+1, search, True, depth) )

if __name__ == '__main__':
    def log2n(n):
        return 0 if n==1 else 1 + log2n( n/2 )

    search = [3, 4, 6, 8, 9, 2, 2, 23]
    depth = log2n(len(search))

    opt = minimax(0, 0, search, True, depth)
    print('The optimal choice is: ', opt)  # 8
