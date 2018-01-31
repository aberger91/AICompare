#!/usr/bin/python3.6
#%matplotlib inline

from enum import Enum
from random import shuffle
from random import randint
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('ggplot')


class IGame:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('this is an abstract class')
    
    def __repr__(self):
        pass
    
    def __str__(self):
        pass
    
    def __eq__(self, other):
        pass
        
    def __lt__(self, other):
        raise NotImplementedError('this method is not implemented yet')
    
    def __hash__(self):
        raise NotImplementedError('this method is not implemented yet')
    
    def __len__(self):
        pass
    
    def __iter__(self):
        pass
    
    def __getitem__(self):
        pass
    
    def successors(self):
        pass
    
    @staticmethod
    def main(**kwargs):
        raise NotImplementedError('this method is not implemented')
    


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

        
class JealousAgents(IGame):
    '''
    Three actors and their three agents want to cross a river in a boat that is capable
    of holding only two people at a time. Each agent is very aggressive and when
    given the chance would convince an actor to sign a new contract with the new
    agent (“poaching”). Since each agent is worried their rival agents will poach their
    client, we add the constraint that no actor and a different agent can be present by
    themselves on one of the banks, as this is the situation in which poaching occurs.
    '''
    class Person:
        def __init__(self, enum):
            self.enum = enum
            self.is_agent = None
            self.is_actor = None

        def __repr__(self):
            return str(self.enum)

        def __eq__(self, other):
            if isinstance(other, type(self)) \
                and self.enum == other.enum: 
                return True
            return False

    class Agent(Person):
        def __init__(self, enum):
            super().__init__(enum)
            self.is_agent = True
            self.is_actor = False

        def __repr__(self):
            return 'Agnt(%d)' % self.enum

    class Actor(Person):
        def __init__(self, enum):
            super().__init__(enum)
            self.is_agent = False
            self.is_actor = True

        def __repr__(self):
            return 'Actr(%d)' % self.enum


    def __init__(self, starting_shore, destination_shore):
        self.starting_shore = starting_shore.copy()
        self.destination_shore = destination_shore.copy()
        self.number_of_participants = len(self.starting_shore)

    def __str__(self):
        return '|'.join([str(_)for _ in self.starting_shore]) + \
                            ' ~~|_|boat|_|~~ ' + \
               '|'.join([str(_)for _ in self.destination_shore])
                #' __hash__ = %d ' % self.__hash__()

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        a = sum([p.enum for p in self.starting_shore])
        b = sum([p.enum for p in self.destination_shore])
        return (a * b) ^ self.number_of_participants & 0x7F

    def __eq__(self, other):
        def _eq_(other, shore):
            for person in self.starting_shore:
                if person not in other.starting_shore:
                    return False
            return True
        if _eq_(other, self.starting_shore) and \
            _eq_(other, self.destination_shore):
            return True
        return False

    @staticmethod
    def people(n):
        people = [JealousAgents.Actor(x)for x in range(1, n+1)] + \
                    [JealousAgents.Agent(x)for x in range(1, n+1)] 
        return people

    @staticmethod
    def start_state(n=3):
        people = JealousAgents.people(n)
        shuffle(people)
        return JealousAgents(
                 people,
                 [ ]
        )

    @staticmethod
    def end_state(n=3):
        people = JealousAgents.people(n)
        shuffle(people)
        return JealousAgents(
                [ ],
                people
        )

    def _is_valid(self):
        def _agents_cannot_poach(shore):
            if len(shore) == 2:
                person_a, person_b = shore
                if (person_a.is_actor and person_b.is_agent or \
                    person_a.is_agent and person_b.is_actor) and \
                    person_a.enum - person_b.enum != 0:
                    return False
            return True
        if _agents_cannot_poach(self.starting_shore) and \
            _agents_cannot_poach(self.destination_shore):
            return True
        return False

    def successors(self):
        states = [ ]
        for x in range(len(self.starting_shore)):
            person_a = self.starting_shore[x]
            remainder = self.starting_shore[:x] + self.starting_shore[x+1:]
            state = JealousAgents(remainder, [person_a] + self.destination_shore)
            if state._is_valid() and state not in states:
                states.append(state)
            for y in range(len(remainder)):
                person_b = remainder[y]
                state = JealousAgents([person_a] + remainder[:y] + remainder[y+1:], 
                                      [person_b] + self.destination_shore)
                if state._is_valid() and state not in states:
                    states.append(state)
        return states

    @staticmethod
    def generate_solution(n=3):
        print('\n\t', '='*4+' solution for JealousAgents with '+str(n*2)+' players '+'='*4)
        states = [ JealousAgents.start_state(n) ]
        count = 0
        while states:
            state = states[randint(0, len(states)-1)]
            states = state.successors()
            print('('+str(count)+')', state)
            count += 1
        print()

    @staticmethod
    def main():
        JealousAgents.generate_solution(3)
        #JealousAgents.generate_solution(4)
        #JealousAgents.generate_solution(5)
        
        
class Game:
    def __init__(self, game):
        self.game = game
    
    def plot_compare(self, results):
        f = plt.figure()
        ax = f.add_subplot(111)
        for k, v, in results.items():
            ax.plot(range(len(results[k])), results[k], label=k)
        ax.legend(loc='best')
        ax.set_title(self.game.__name__ + ' Trials')
        ax.set_ylabel('# of Searches')
        ax.set_xlabel('Difficulty')
        plt.show()
        
    def compare(self, strategies, easiest=1, hardest=10, trials=10, max_states=1000):
        print('\n', '='*8+' '+self.game.__name__+' '+'='*8)
        print(self.game.__doc__)
        results = {}
        for strat in strategies:
            print(',{}'.format(strat), end="")
            results[strat] = []
        for level in range(easiest, hardest+1):
            print('\n{}'.format(level), end="")
            for strat in strategies:
                total_states = 0
                for trial in range(trials):
                    start = self.game.start_state(level)
                    goal = self.game.end_state(level)
                    total_states += self.search(start, goal, strategy=strat, max_states=max_states)
                results[strat].append(total_states // trials)
                print(',{}'.format(total_states // trials), end='')
        print()
        return results

    def search(self, start, goal, strategy='dfs', max_states=1000):
        count = 0
        to_visit = [ start ]
        visited = set()
        while to_visit:
            state = to_visit.pop()
            if state == goal:
                return count
            elif count >= max_states:
                return count
            elif state in visited:
                pass
            else:
                visited.add(state)
                new_states = state.successors()
                shuffle(new_states)
                if strategy == 'dfs':
                    to_visit += new_states
                elif strategy == 'bfs':
                    to_visit = new_states + to_visit
                elif strategy == 'mhd':  # EightPuzzle
                    to_visit += new_states
                    to_visit = sorted(to_visit, key=lambda x:-1*x.manhatten_distance())  # lower mhd is better
                elif strategy == 'eval':
                    to_visit += new_states
                    to_visit = sorted(to_visit, key=lambda x:x.evaluation())  # higher evaluation is better
                elif strategy == 'best':
                    to_visit = to_visit + new_states
                    to_visit = sorted(to_visit)  # should implement __lt__
                count += 1
        return count



if __name__ == '__main__':
    
    EASIEST, HARDEST, TRIALS, MAX_STATES = (1, 10, 10, 1000)
    
    games = {
             BoxWorld: ['dfs', 'bfs'],
             EightPuzzle: ['dfs', 'bfs', 'eval', 'mhd'],
             JealousAgents: ['dfs']
            }
    
    for puzzle, strategies in games.items():

        solver = Game(puzzle)
        results = solver.compare(strategies)
        
        if solver.game.__name__ == 'JealousAgents':
            solver.game.main()
            
        solver.plot_compare(results)



