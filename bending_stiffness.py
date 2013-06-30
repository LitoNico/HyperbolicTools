bendList = []
bending_stiffness = 2


for i in m_constraints:
	c = m_constraints[i]
	v1 = c.particle_A
	v2 = c.particle_B
	edge_verts = v1,v2
	vert1_connected = lx.eval('query layerservice vert.vertList ? ' + str(v1) )
	vert2_connected = lx.eval('query layerservice vert.vertList ? ' + str(v2) )
	addl_two = tuple([item for item in vert1_connected if item in vert2_connected])
	bendList.append( [edge_verts, addl_two] )


normalList = [] #wrong wrong wrong
for index in num_verts:
	normalList.append = eval(lx.eval('query layerservice vert.normal ? ' + str(index) ))
	
def precompute_stiffness
	for i in enumerate(bendList):
		try:
			a, b = bendList[i][1] 
			c,d = bendList[i][0]
		except:
			lx.out("Error in list access")
		#shortnames
		h_a = normalList[a]
		h_b = normalList[b]
		h_c = normalList[c]
		h_d = normalList[d]
		# build coefficients
		alpha_a = h_b / (h_a + h_b)
		alpha_b = h_a / (h_a + h_b)
		alpha_c = h_d / (h_c + h_d)
		alpha_d = h_c / (h_c + h_d)
		
		cd_edge_length = distance(c,d) #this will raise an error
		
		stiffness_lambda = (2.0/3.0) * ( (h_a + h_b) / (h_a*h_b)**2 ) * bending_stiffness * cd_edge_length
	


def runtime_stiffness
	r = 