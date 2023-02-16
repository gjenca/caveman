
import sys
import functools
import itertools
import networkx as nx

class Node(frozenset):

    def __repr__(self):
        
        return "".join(str(v) for v in self)

def complement(g,node_set):

        ret=set(g.nodes())
        for node in node_set:
            ret=ret & set(nx.neighbors(g,node))
        return ret

def closure(g,node_set):
    
    return complement(g,complement(g,node_set))

def powset(s):

    for n in range(len(s)+1):
        for c in itertools.combinations(s,n):
            yield set(c)

def closed_sets(g):

    for s in powset(g.nodes()):
        yield frozenset(complement(g,s))

n=5

mg=nx.Graph()

for c in itertools.combinations(range(n),2):
    mg.add_node(Node(c))

for node in list(mg.nodes()):
    for i in range(n):
        if i not in node:
            for end in node:
                mg.add_edge(node,Node((i,end)))




for cs in closed_sets(mg):
    subgraph=nx.induced_subgraph(mg,cs)
    for clique in nx.find_cliques(subgraph):
        if set(cs)!=set(closure(mg,clique)):
            print('closure of',set(clique),'is not',set(cs))
            sys.exit(0)
print('Dacey!!!')




