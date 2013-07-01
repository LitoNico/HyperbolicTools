bendList = []
stiffness_constant = 0.01 #smaller is less stiff


for i in m_constraints:
	c = m_constraints[i]
	v1 = c.particle_A
	v2 = c.particle_B
	edge_verts = v1,v2
	vert1_connected = lx.eval('query layerservice vert.vertList ? ' + str(v1) )
	vert2_connected = lx.eval('query layerservice vert.vertList ? ' + str(v2) )
	addl_two = tuple([item for item in vert1_connected if item in vert2_connected])
	bendList.append( [edge_verts, addl_two] )



stiffness_vertnormals = cross( #the 

def precompute_stiffness
	for i in enumerate(bendList):
		try:
			a, b = bendList[i][1] 
			c,d = bendList[i][0]
		except:
			lx.out("Error in list access")
		#shortnames
		h_a = normalList[a]
		# build coefficients
		stiffness_alpha = h_b / (h_a + h_b)
		#Since the satisfyConstraints function will cause edges to converge to 
		#the same length, all faces will converge to equilateral triangles
		
		c-d_edgelength = avg_len #distance(c,d)
		
		stiffness_lambda = (2.0/3.0) * ( (h_a + h_b) / (h_a*h_b)**2 ) * stiffness_constant * c-d_edgelength
	


def runtime_stiffness
	r = 
	
	
	for i in enumerate(vertList):
		m_particles[i].m_x += stiffnessList[i]