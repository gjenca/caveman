
import itertools
import functools

class myfrozenset(frozenset):

    def __repr__(self):
        
        return repr(set(self))

    def __str__(self):
        
        return str(set(self))


class OrthoSpace:

    def neighbourhood(self,v_set):

        return functools.reduce(lambda a,b: myfrozenset(a & b),
           (myfrozenset(self.neighbourhood_f(v)) for v in v_set),
        self.vertices())   


    def closure(self,v_set):

        return self.neighbourhood(self.neighbourhood(v_set))

    def subsets(self):

        for n in range(len(self)):
            for c in itertools.combinations(self.vertices(),n):
                yield myfrozenset(c)

    def closed_subsets(self):
        
        cs=set()
        for v_set in self.subsets():
            cs.add(self.closure(v_set))

        return cs

    def is_clique(self,v_set):

        n=len(v_set)
        for v in v_set:
            k=sum(1 for w in self.neighbourhood_f(v) if w in v_set)
            if k<n-1:
                return False
        return True
        
    def max_cliques(self,v_set):

        print('max_cliques',v_set)
        if len(v_set)==0:
            yield myfrozenset()
        else:
            v=next(iter(v_set))
            rest=myfrozenset(v_set-{v})
            for clique_smaller in self.max_cliques(rest):
                try_bigger=myfrozenset({v}|clique_smaller)
                if self.is_clique(try_bigger):
                    yield try_bigger
                else:
                    for w in clique_smaller:
                        try_smaller=myfrozenset({v}|(clique_smaller-{w}))
                        if self.is_clique(try_smaller):
                            yield(try_smaller)

class Path4(OrthoSpace):

    n_d={
        1:{2},
        2:{1,3},
        3:{2,4},
        4:{3},
    }

    def __len__(self):

        return 4

    def vertices(self):

        return myfrozenset({1,2,3,4})

    @property
    def neighbourhood_f(self):

        def ret_f(v):
            
            return myfrozenset(self.n_d[v])
    
        return ret_f

class NumberEdge(frozenset):

    def __repr__(self):

        return "".join(str(x) for x in self)

class MatchingGraph(OrthoSpace):

    def __init__(self,n):

        self.n=n

    def __len__(self):

        return self.n*(self.n-1)//2

    def vertices(self):

        return myfrozenset(NumberEdge(pair) for pair in itertools.combinations(range(self.n),2))

    @property
    def neighbourhood_f(self):
        
        @functools.cache
        def ret_f(v):
        
            for i in range(self.n):
                if i not in v:
                    for end in v:
                        yield NumberEdge((i,end))

        return ret_f
        

        

    
