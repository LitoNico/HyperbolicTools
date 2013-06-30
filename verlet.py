#python

'''
HyperTools.py by Lito Nicolai

For questions or bug reports, please contact lito.nicolai@gmail.com
'''


###### Classes and Constants ######

from math import sqrt

class Vector3(tuple): #Vector3 class for tuples
	def __init__(self, v):
		x, y, z = v #unpacking
		self.x = x
		self.y = y
		self.z = z
		#self.repack = v
		
	def __mul__(self, other):
		if other.__class__.__name__ == 'Vector3':
			return Vector3(tuple(m * n for (m, n) in zip(self, other)) ) # dot product
		else:
			return Vector3(tuple(other * n for n in self)) #scalar multiplication, no other types defined	
			#works only in the form Vector3 * Scalar, Scalar * Vector3 returns n copies of the vector
	def __add__(self, other):
		return Vector3(tuple(m + n for (m, n) in zip(self, other)) ) 
		
	def __sub__(self, other):
		return Vector3(tuple(m - n for (m, n) in zip(self, other)) )
		
	def pSum(self): #piecewise sum
		return self.x + self.y +self.z
	
	def cross(self, other)
		return Vector3( self.y * other.z - self.z * other.y, 
						self.z * other.x - self.z * other.z, 
						self.x * other.y - self.y * other.x)
	def magnitude(self):
		return sqrt( self.x**self.x + self.y*self.y + self.z*self.z )
		
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
		
class Constraint:
	def __init__(self, edgeTuple, restlength):
		v1, v2 = edgeTuple
		self.particleA = v1
		self.particleB = v2
	
null = 0,0,0 

###### Import vert position data from modo ######

vertList = lx.evalN("query layerservice verts ? all") # returns a list [v1, v2, ..., vn] of vertices in the current layer. Each vert is identified by an index.


vertPositions = list( lx.evalN("query layerservice vert.wpos ? " + str(index) ) for index in vertList ) #makes a list of vert positions. Positions returned are tuples.


num_particles = len(vertList) 

del vertList #don't need this anymore, vertices are always referred to in order from now on

m_particles = []

if eval(lx.eval(user.value Hypertools.previous_positions ? )) is None:
	rebuild_poslist = True

for index in range(0, num_particles): #converts vertPositions into a usable list of Particle classes.
	temp = Particle( 
						Vector3(
									vertPositions[index]#current_position
								), #end Vector3
						Vector3( 				
								
									
										vertPositions[index] # create a new base state where nothing's moving
								), #end Vector3
						Vector3( 
									null 				#forces (begin null)
								), #end Vector3
		
									index 				#index
									
									) #end Particle
	m_particles.append(temp)
	
del vertPositions #cleanup


###### Import edge data from modo ######

#fixedRestLength = m_particles[1].m_x.x 

fixedRestLength = 0.9

edgeListTemp = list( lx.evalN("query layerservice edges ? all") ) # returns a list of edges (used as constraints) as tuples of form (v1, v2). !!! this might only work on the first layer!

edgeList = [eval(x) for x in edgeListTemp] #annoying but necessary, evaluates the contents of the strings into the tuples they really are.

del edgeListTemp


num_constraints = len(edgeList)

m_constraints = []

for index in range(num_constraints): #same as above, converts edgeList to a list of Constraint classes
	temp = Constraint(edgeList[index], fixedRestLength)
	m_constraints.append(temp)
					 
del edgeList

###### Pre-build list of Verts for bending stiffness ######



###### The Verlet model ######

const = 0.5 # a lower number makes edges converge more slowly to avoid self-collision

num_iterations = 1

#global fTimeStep 
fTimeStep = 0.5


lengthlist = []

def averagedist():
	for i in range (num_constraints):
		c = m_constraints[i]
		x1 = c.particleA
		x2 = c.particleB
		lengthlist.append (distance(m_particles[x1].m_x, m_particles[x2].m_x))
	return sum(lengthlist)/len(lengthlist)
	
	
	
restlength = averagedist()				# for this case, but not for verlet in general.
restlength2 = restlength * restlength   # Can use m_constraints.restlength if normal behavior is required

def AccumulateForces():
	pass #implement if gravity is ever needed

def SatisfyConstraints():
	for i in range(0, num_iterations):
		for j in range(0, num_constraints):
			c = m_constraints[j]
			x1 = m_particles[c.particleA].m_x #getting the position of the first vertex in a constraint
			x2 = m_particles[c.particleB].m_x
			delta = x2 - x1 # a Vector3
			delta *= restlength2/ (Vector3.pSum(delta*delta) + restlength2) - 0.5 #first-order taylor expansion of sqrt operator (for speed)
			#need to push the values back into the particle
			m_particles[c.particleA].m_x -= delta * const
			m_particles[c.particleB].m_x += delta * const



def TimeStep():
	#AccumulateForces()
	SatisfyConstraints()
	
	

num_steps = 30
for n in range(num_steps):
	TimeStep()
	



###### Export vert positions back to modo ######

def pushParticles():
	lx.eval('select.drop vertex')
	for index in range(num_particles): #loop over list of particles to push their new positions back to modo
		lx.command("vert.move", vertIndex = index, posX = m_particles[index].m_x.x, posY = m_particles[index].m_x.y , posZ = m_particles[index].m_x.z)
		
pushParticles()
