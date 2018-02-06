from abstract import IGame
from random import shuffle, randint

        
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
