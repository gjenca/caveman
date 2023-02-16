
from caveman import *
m4=Path4()

print('max cliques in p4')
for v_set in m4.max_cliques(m4.vertices()):
    print(v_set)

