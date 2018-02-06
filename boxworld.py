from abstract import IGame
from random import randint, shuffle

class BoxWorld(IGame): 
    '''
    Implementation of the toy blocks world. 
    The world has 3 blocks (enumerate them however you’d like, but I would suggest ‘a’, ‘b’, and ‘c’).
    
    Devise a way to represent a state.
    (for example, [‘abc’] might represent the state where a is on top of b, which is on top of c). 
    
    Keep in mind that the relative position of a block or stack of
    blocks on the table (left or right) is irrelevant; therefore if you use a list then [‘ab’,
    ‘c’] and [‘c’, ‘ab’] would represent the same state of the world. 
    '''
    def __init__(self, boxes):
        self.state = boxes  # List[str] # char
        self.size = len(self.state)

    def __str__(self):
        return str(self.state)
        
    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.state)

    def __iter__(self):
        for b in self.state:
            yield b

    def __hash__(self):
        hash_ = 0
        for x in range(self.size):
            s = self.state[x]
            if len(s) > 1:
                hash_ += int(''.join([str(ord(x)) for x in s]))
            else:           
                hash_ += ord(s)
        return hash_  & 0x7F

    def __eq__(self, other):
        return set(self.state) == set(other.state)

    def __getitem__(self, v):
        if v < len(self):
            return self.state[v]
        raise IndexError('index out of bounds')

    def successors(self):
        states = [ ]
        for x in range(self.size):
            s = self.state[x]
            remainder = self.state[:x] + self.state[x+1:]
            if len(s) == 1: # stack
                for c in range(self.size):
                    if c == x: continue
                    _remainder = self.state[:x] + self.state[x+1:]
                    index = ''.join(_remainder).find(self.state[c])
                    _remainder.pop(index)
                    states.append(BoxWorld( [s + self.state[c]] + _remainder))
            elif len(s) > 1:  # unstack
                states.append( BoxWorld( [s[0], s[1:]] +  remainder ))
        return states
        
    @staticmethod
    def random_state(n=3, iter=100):
        n = 3  # our box world always has 3 elements
        ascii_offset = 65
        state = BoxWorld( [chr(x) for x in range(ascii_offset, ascii_offset+n)] )
        for _ in range(randint(0, iter-1)): # random iterations
            new_states = state.successors()
            state = new_states[ randint(0, len(new_states)-1) ]
        return state

    @staticmethod
    def start_state(n=3):
        return BoxWorld.random_state(n)
        
    @staticmethod
    def end_state(n=3):
        return BoxWorld.random_state(n)
        
    @staticmethod
    def play(start_state, goal_state):
        states = [ start_state ]
        goal_state = goal_state
        while states:
            print('number of parent states: ', len(states))
            state = states[randint(0, len(states)-1)]
            states = state.successors()
            print('current state: ', state)
            for s in states: 
                if state == goal_state:
                    print('found goal state: ', state)
                    return
                print('\t', s)
            print()
        
    @staticmethod
    def main():
        start_state = BoxWorld.random_state()
        end_state = BoxWorld.random_state()
        BoxWorld.play(start_state, end_state)
