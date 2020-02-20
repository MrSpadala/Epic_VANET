import networkx as nx



n	=	100		#nodes

p	=	0.3		#probability edge creation


grap = nx.fast_gnp_random_graph(n=n,p=p)

print(nx.nodes(grap))
print(nx.edges(grap))