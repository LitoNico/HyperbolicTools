import modoTools from HyperbolicTools

initial_edges = get_selected_edges()

for i in range(repeats):
	grow_quads(selected)
	latest_edges = get_new_edges(model)
	order_edges(latest_edges)
	edge_select( get_edge_interval(latest_edges) )
	edge_split_script()




def get_edge_interval(orderedEdges, interval)
	for i in range(len(orderedEdges), interval)
		...
		
		
def grow_quads():
	lx.eval("edge.growQuads true 0.1 89.9 false")
	
def get_new_edges(edgeList_current, edgeList_previous):
	