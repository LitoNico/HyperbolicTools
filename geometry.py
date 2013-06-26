#python

#edges are selected
lx.eval("select.editSet cache1 add")
lx.eval("edge.growQuads false 0.1 89.9 false")
lx.eval("edge.collapse")
lx.eval("select.useSet cache1 select")
lx.eval("edge.remove true")
lx.eval("select.editSet cache1 remove")
#lx.eval("poly.triple")

#edge lengths are equalized