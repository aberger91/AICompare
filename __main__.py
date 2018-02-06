#!/usr/bin/python3.6
#%matplotlib inline

import matplotlib as mpl
mpl.style.use('ggplot')
        
        


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



