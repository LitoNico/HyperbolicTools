
###### Creation of user values and flags ######

#put this in the config
#user.defNew HyperTools.restart_flag integer
#user.defNew HyperTools.previous_positions string

if restart_flag() == 1:
	lx.eval(user.value HyperTools.previous_positions None)
	
lx.eval(user.value HyperTools.previous_positions
