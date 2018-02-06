from enum import Enum
from random import shuffle, randint
import matplotlib.pyplot as plt


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

