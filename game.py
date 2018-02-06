from enum import Enum
from random import shuffle, randint
import matplotlib.pyplot as plt


class Game:
    def __init__(self, game):
        self.game = game
    
    def plot_compare(self, results):
        f = plt.figure()
        plt.style.use('ggplot')
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
                    to_visit = Game.depth_first_search(to_visit, new_states)
                elif strategy == 'bfs':
                    to_visit = Game.breadth_first_search(to_visit, new_states)
                elif strategy == 'mhd':  # should implement State.manhatten_distance
                    to_visit = Game.manhatten_distance(to_visit, new_states)
                elif strategy == 'eval':  # should implement State.eval
                    to_visit = Game.evaluation(to_visit, new_states)
                elif strategy == 'best':  # should implement State.__lt__
                    to_visit = Game.best(to_visit, new_states)
                count += 1
        return count

    @staticmethod
    def depth_first_search(to_visit, new_states):
        to_visit += new_states
        return to_visit

    @staticmethod
    def breadth_first_search(to_visit, new_states):
        to_visit = new_states + to_visit
        return to_visit

    @staticmethod
    def manhatten_distance(to_visit, new_states):
        to_visit += new_states
        to_visit = sorted(to_visit, key=lambda x:-1*x.manhatten_distance())  # lower mhd is better
        return to_visit

    @staticmethod
    def evaluation(to_visit, new_states):
        to_visit += new_states
        to_visit = sorted(to_visit, key=lambda x:x.evaluation())  # higher evaluation is better
        return to_visit

    @staticmethod
    def best(to_visit, new_states):
        to_visit = to_visit + new_states
        to_visit = sorted(to_visit)  # should implement __lt__
        return to_visit
