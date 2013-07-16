#python

'''
hyperbolictools.py by Lito Nicolai

Implements 
"Advanced Character Physics," T. Jakobsen, 2003
and
"Simple Linear Bending Stiffness in Particle Systems," Volino and Magnenat-Thalmann, 2006

For questions or bug reports, please contact lito.nicolai@gmail.com
'''

lx.eval("poly.triple")

###### Classes and Constants ######

from math import sqrt

class Vector3(tuple): #Vector3 class for tuples
	def __init__(self, v):
		x, y, z = v #unpacking
		self.x = x
		self.y = y
		self.z = z
		
	def __mul__(self, other):
		if other.__class__.__name__ == 'Vector3':
			return Vector3(tuple(m * n for (m, n) in zip(self, other)) ) # dot product
		else:
			return Vector3(tuple(other * n for n in self)) #scalar multiplication	
			#works only in the form Vector3 * Scalar, Scalar * Vector3 returns n copies of the vector
	def __add__(self, other):
		return Vector3(tuple(m + n for (m, n) in zip(self, other)) ) 
		
	def __sub__(self, other):
		return Vector3(tuple(m - n for (m, n) in zip(self, other)) )
		
	def pSum(self): #piecewise sum
		return self.x + self.y + self.z
	
	def cross(self, other):
		return Vector3( 
							(
						self.y * other.z - self.z * other.y, 
						self.z * other.x - self.z * other.z, 
						self.x * other.y - self.y * other.x
							 )
					   )
					   
	def magnitude(self):
		return sqrt( self.x*self.x + self.y*self.y + self.z*self.z )
		
	def normalize(self):
		return self * 1.0 / magnitude

def distance(vec1, vec2):
		return sqrt( (vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2 + (vec1.z - vec2.z)**2 )
		
class Particle: #pretty much identical to T.Jakobsen's class
	def __init__(self, current_position, previous_position, forces, index): #where everything except index is a vector
		self.m_x = current_position
		self.old_x = previous_position
		self.m_a = forces
		self.index = index
		
class Constraint: #restlength unused, but can be implemented for better 'cloth' simulation
	def __init__(self, edgeTuple, restlength):
		v1, v2 = edgeTuple
		self.particleA = v1
		self.particleB = v2
	
null = 0,0,0 

###### Import vert position data from modo ######

vertList = lx.evalN("query layerservice verts ? all") # returns a list [v1, v2, ..., vn] of vertices in the current layer. Each vert is identified by an index.
vertPositions = list( lx.evalN("query layerservice vert.wpos ? " + str(index) ) for index in vertList ) #makes a list of vert positions. Positions returned are tuples.
num_particles = len(vertList) 
del vertList #vertices are always referred to in order from now on


m_particles = []

for index in range(0, num_particles): #converts vertPositions into a usable list of Particle classes.
	temp = Particle( 
						Vector3(
									vertPositions[index]#current_position
								), #end Vector3
						Vector3( 						
										vertPositions[index] # create a new base state where nothing's moving.
										#more to be implemented
								), #end Vector3
						Vector3( 
									null 				#forces (begin null)
								), #end Vector3
									index 		
									) #end Particle
	m_particles.append(temp)
	
del vertPositions 

###### Import edge data from modo ######

lengthlist = []

def averagedist(): #get average edge length
	for i in range (num_constraints):
		c = m_constraints[i]
		x1 = c.particleA
		x2 = c.particleB
		lengthlist.append (distance(m_particles[x1].m_x, m_particles[x2].m_x))
	return sum(lengthlist)/len(lengthlist)
	
	
	
restlength = averagedist()				# for this case, but not for verlet in general.
restlength2 = restlength * restlength   # Can use m_constraints.restlength if normal behavior is required


edgeListTemp = list( lx.evalN("query layerservice edges ? all") ) # returns a list of edges (used as constraints) as tuples of form (v1, v2). !!! this might only work on the first layer!

edgeList = [eval(x) for x in edgeListTemp] #annoying but necessary, evaluates the contents of the strings into the tuples they really are.

del edgeListTemp


num_constraints = len(edgeList)

m_constraints = []

for index in range(num_constraints): #same as above, converts edgeList to a list of Constraint classes
	temp = Constraint(edgeList[index], restlength)
	m_constraints.append(temp)
					 
del edgeList

###### Solving constraints ######

const = 0.5 #constant between 1 and 0 
            #a lower number makes edges converge more slowly to avoid self-collision

num_iterations = 1

#fTimeStep = 0.5 implement if using real verlet

def AccumulateForces():
	pass #implement if gravity is ever needed

def SatisfyConstraints():
	for i in range(num_iterations):
		for j in range(num_constraints):
			c = m_constraints[j]
			x1 = m_particles[c.particleA].m_x #getting the position of the first vertex in a constraint
			x2 = m_particles[c.particleB].m_x
			delta = x2 - x1 # a Vector3
			delta *= restlength2/ (Vector3.pSum(delta*delta) + restlength2) - 0.5 #first-order taylor expansion of sqrt operator (for speed)
			#need to push the values back into the particle
			m_particles[c.particleA].m_x -= delta * const
			m_particles[c.particleB].m_x += delta * const



#def TimeStep(): implement for verlet sim
#	AccumulateForces()
#	Verlet()
#	SatisfyConstraints()

constraints_steps = 10
for n in range(constraints_steps): #pre-solve constraints so calculating stiffness constants can be generalized
	SatisfyConstraints()
	

###### Bending Stiffness ######

stiffness_constant = 0.001 #Value for scale-based stiffness- smaller is less stiff
#epsilon = 0.0001

bendList = []
for i in range(num_constraints): #a list of triangle-pairs used to calculate bending angles
	c = m_constraints[i]
	v1 = c.particleA
	v2 = c.particleB
	edge_verts = v1,v2
	vert1_connected = lx.eval('query layerservice vert.vertList ? ' + str(v1) )
	vert2_connected = lx.eval('query layerservice vert.vertList ? ' + str(v2) )
	addl_two = tuple([item for item in vert1_connected if item in vert2_connected])
	bendList.append( [addl_two, edge_verts] )

#Since the satisfyConstraints function will cause edges to converge to 
#the same length, all faces will converge to equilateral triangles. So, the stiffness alpha
#constants can be generalized and only need be calculated for one set of two tris.

Pa, Pb = bendList[0][0] # Point a, point b...
Pc, Pd = bendList[0][1]

Pa = m_particles[Pa].m_x
Pb = m_particles[Pb].m_x
Pc = m_particles[Pc].m_x
Pd = m_particles[Pd].m_x

vertnormal_a = Vector3.cross((Pa-Pc),(Pa-Pd)) #approximate normals of the verts
vertnormal_b = Vector3.cross((Pb-Pd),(Pb-Pc))
vertnormal_c = Vector3.cross((Pc-Pb),(Pc-Pd))
vertnormal_d = Vector3.cross((Pd-Pa),(Pd-Pb))
	

stiffness_alpha_a = Vector3.magnitude(vertnormal_b)/(Vector3.magnitude(vertnormal_a) + Vector3.magnitude(vertnormal_b) )
stiffness_alpha_b = Vector3.magnitude(vertnormal_a)/(Vector3.magnitude(vertnormal_a) + Vector3.magnitude(vertnormal_b) )
stiffness_alpha_c = -1.0*(Vector3.magnitude(vertnormal_d)/(Vector3.magnitude(vertnormal_c) + Vector3.magnitude(vertnormal_d) ) )
stiffness_alpha_d = -1.0*(Vector3.magnitude(vertnormal_c)/(Vector3.magnitude(vertnormal_c) + Vector3.magnitude(vertnormal_d) ) )
	
alphasum = stiffness_alpha_a + stiffness_alpha_b + stiffness_alpha_c + stiffness_alpha_d

lx.out("alphasum = " + str(alphasum)) #must be 0
#assert 0 - alphasum < 0 - epsilon or 0 - alphasum < 0 + epsilon

#use this defn. of stiffness_lambda if more realistic, scale-based stiffness is desired.
#stiffness_lambda = -1.0 * (2.0/3.0) * ( 
#										Vector3.magnitude(vertnormal_a)+ Vector3.magnitude(vertnormal_b) 
#									  ) / ( 
#									  ( Vector3.magnitude(vertnormal_a) * Vector3.magnitude(vertnormal_b) ) **2 
#									       ) * stiffness_constant * restlength 

#lx.out("lambda = " + str(stiffness_lambda) )

del Pa
del Pb
del Pc
del Pd

stiffness_lambda = -0.2 #same stiffness, regardless of scale


def RuntimeStiffness():
	for i in range(len(bendList)):
		try:
			Pa, Pb = bendList[i][0] 
			Pc, Pd = bendList[i][1]
		except:
			pass #for verts on the outer edge of the surface
		bendingvector_R = m_particles[Pa].m_x * stiffness_alpha_a + m_particles[Pb].m_x * stiffness_alpha_b + m_particles[Pc].m_x * stiffness_alpha_c + m_particles[Pd].m_x * stiffness_alpha_d 
		stiffnessforce_a = bendingvector_R * stiffness_lambda * stiffness_alpha_a
		stiffnessforce_b = bendingvector_R * stiffness_lambda * stiffness_alpha_b
		stiffnessforce_c = bendingvector_R * stiffness_lambda * stiffness_alpha_c
		stiffnessforce_d = bendingvector_R * stiffness_lambda * stiffness_alpha_d
		
		m_particles[Pa].m_x += stiffnessforce_a * const #to converge slower
		m_particles[Pb].m_x += stiffnessforce_b * const
		m_particles[Pc].m_x += stiffnessforce_c * const
		m_particles[Pd].m_x += stiffnessforce_d * const


num_steps = 10
for n in range(num_steps):
	SatisfyConstraints()
	RuntimeStiffness()

###### Export vert positions back to modo ######

def pushParticles():
	lx.eval('select.drop vertex')
	for index in range(num_particles): #loop over list of particles to push their new positions back to modo
		lx.command("vert.move", vertIndex = index, posX = m_particles[index].m_x.x, posY = m_particles[index].m_x.y , posZ = m_particles[index].m_x.z)
		
pushParticles()
