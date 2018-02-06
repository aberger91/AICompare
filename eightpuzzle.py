from abstract import IGame
from random import shuffle, randint

    
class EightPuzzle(IGame):
    '''
    A simple “estimator” function for the 8-puzzle game is to count the number of
    tiles that are in the right place. (This estimator evaluates to an integer between 0 and 8). 
    
    Devise a better estimator function than this for 8-puzzle. “Manhattan
    distance” is a better estimator that was mentioned in class (although I haven’t
    shown you any data which supports that assertion). 
    
    You may choose a different estimator, but it must work better 
    than simply counting the number of tiles that are in the right place.
    '''
    def __init__(self, tiles):
        self.tiles = tiles.copy()

    def __str__(self):
        answer = ''
        for i in range(9):
            answer += '{} '.format(self.tiles[i])
            if (i+1)%3 == 0:
                answer += '\n'
        return answer

    def __repr__(self):
        return 'EightPuzzle({})'.format(self.tiles)

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(self.tiles[0])
        
    def __getitem__(self, v):
        return self.tiles[v]

    def successors(self):
        successor_states = [ ]
        neighbors = {
                     0:[1,3],
                     1:[0,2,4],
                     2:[1,5],
                     3:[0,4,6],
                     4:[1,3,5,7],
                     5:[2, 4,8],
                     6:[3,7],
                     7:[4,6,8],
                     8:[5,7]
                     }
        zero_loc = self.tiles.index(' ')
        for loc in neighbors[zero_loc]:
            state = EightPuzzle(self.tiles)
            state.tiles[zero_loc] = state.tiles[loc]
            state.tiles[loc] = ' '
            successor_states.append(state)
        return successor_states

    def evaluation(self):
        correct = 9
        end_state = EightPuzzle.end_state()
        for i in range(correct-1):
            if self.tiles[i] != end_state[i]:
                correct -= 1
        return correct

    def _get_index_of(self, v):
        return self.tiles.index(str(v))

    def manhatten_distance(self):
        '''
        compute the sum of the manhatten distances for all squares
        '''
        goal = EightPuzzle.end_state()
        distances = [(self._get_index_of(x), goal._get_index_of(x)) for x in range(1, len(self.tiles))]
        result = sum(abs(current_index%3 - goal_index%3) + abs(current_index//3 - goal_index//3) \
                     for current_index, goal_index in distances)
        return result
    
    @staticmethod
    def end_state(dummy=0):
        return EightPuzzle(['1', '2', '3', '8', ' ', '4', '7', '6', '5'])

    @staticmethod
    def start_state(distance=1):
        already_visited = [ EightPuzzle.end_state() ]
        state = EightPuzzle.end_state()
        for i in range(distance):
            successors = state.successors()
            for s in successors:
                if s in already_visited:
                    successors.remove(s)
            shuffle(successors)
            state = successors[0]
            already_visited.append(state)
        return state
    
    @staticmethod
    def main(distance=1):
        states = [ EightPuzzle.start_state(distance) ]
        goal_state = EightPuzzle.end_state()
        while states:
            print('number of parent states: ', len(states))
            state = states[randint(0, len(states)-1)]
            states = state.successors()
            print('current state: \n', state)
            for s in states: 
                if state == goal_state:
                    print('found goal state: \n', state)
                    return
                print(s)
            print()
