'''
    Andrew Berger | CSC480 | Homework #3 | 2/24/2018 
                                                        '''

class Fact:
    def __init__(self, predicate, *arguments):
        self.predicate = predicate
        self.arguments = arguments

    def __eq__(self, other):
        return (isinstance(other, Fact)
                and self.predicate == other.predicate
                and self.arguments == other.arguments)

    def __hash__(self): 
        return hash(self.predicate) ^ hash(self.arguments)

    def __repr__(self):
        op = self.predicate
        arguments = [str(arg) for arg in self.arguments]
        if op.isidentifier():
            if arguments:
                return '%s(%s)' % (op, ', '.join(arguments))
            else:
                return op
        elif len(arguments) == 1:
            return op + arguments[0]
        else:
            opp = (' ' + op + ' ')
            return '(' + opp.join(arguments) + ')'


def is_variable(x):
    is_var = isinstance(x, Fact) 
    is_var = (is_var and not x.arguments)
    is_var = (is_var and not x.predicate[-1].isdigit())
    return is_var

def first(iterable):
    default = None
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def occur_check(var, x, s):
    if var == x:
        return True

    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)

    elif isinstance(x, Fact):
        return (occur_check(var, x.predicate, s) or occur_check(var, x.arguments, s))

    elif isinstance(x, (tuple, list)):
        return first(e for e in x if occur_check(var, e, s))

    else:
        return False

def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)

    elif x in s:
        return unify(var, s[x], s)

    elif occur_check(var, x, s):
        return False

    else:
        s2 = s.copy()
        s2[var] = x
        return s2

def one_is_string(x, y):
    return isinstance(x, str) or isinstance(y, str)

def are_facts(x, y):
    return isinstance(x, Fact) and isinstance(y, Fact)

def are_iterables(x, y):
    return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple))

def are_equal_lengths(x, y):
    return len(x) == len(y)


def unify(x, y, s={}):
    if s is None:
        return False

    elif x == y:
        return s

    elif is_variable(x):
        return unify_var(x, y, s)

    elif is_variable(y):
        return unify_var(y, x, s)

    elif are_facts(x, y):
        return unify(x.arguments, 
                     y.arguments, 
                     unify(x.predicate, y.predicate, s)
                     )

    elif one_is_string(x, y):
        return False

    elif are_iterables(x, y):

        if not are_equal_lengths(x, y) or not x:
            return s

        return unify(x[1:], 
                     y[1:], 
                     unify(x[0], y[0], s)
                     )

    else:
        return False



if __name__ == '__main__':

    test_cases = [
                  (Fact('human', Fact('x')), 
                   Fact('human', Fact('y'))),

                  (Fact('likes', Fact('x'), Fact('y')), 
                   Fact('likes', Fact('pat0'), Fact('chris2'))),

                  (Fact('likes', Fact('x'), Fact('x')), 
                   Fact('likes', Fact('pat0'), Fact('chris2'))),

                  (Fact('likes', Fact('x'), Fact('x')), 
                   Fact('likes', Fact('y'), Fact('pat0'))),

                  (Fact('likes', Fact('pat0'), Fact('pat0')), 
                   Fact('likes', Fact('x'), Fact('x'))),

                  (Fact('likes', Fact('pat0'), Fact('x')), 
                   Fact('likes', Fact('y'), Fact('pat0'))),

                  (Fact('likes', Fact('x'), Fact('y'), Fact('y')), 
                   Fact('likes', Fact('pat0'), Fact('chris2'))),

                  # EXTRA CREDIT

                  (Fact('likes', Fact('x'), Fact('y')),
                   Fact('likes', Fact('friend-of', Fact('pat0')), Fact('pat0'))),

                   (Fact('likes', Fact('friend-of', Fact('y')), Fact('y')),
                   Fact('likes', Fact('friend-of', Fact('x')), Fact('x'))),

                   (Fact('suburb', Fact('sk1', Fact('c')), Fact('c')),
                   Fact('suburb', Fact('x'), Fact('naperville0'))),

                   (Fact('suburb', Fact('sk1', Fact('c')), Fact('c')),
                   Fact('suburb', Fact('skcity1', Fact('c')), Fact('naperville0'))),

                ]


    print(__doc__)

    for x in range(len(test_cases)):

        expr_a = test_cases[x][0]
        expr_b = test_cases[x][1]
        
        print('%d. %s = %s' % (x+1, expr_a, expr_b))

        print(unify(expr_a, expr_b))
        print()


