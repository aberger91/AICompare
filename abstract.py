
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
    

