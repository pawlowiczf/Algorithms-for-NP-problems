from pulp import *

model = LpProblem(name = 'test', sense = LpMinimize)

x = LpVariable('x', cat=LpInteger)
y = LpVariable('y', cat=LpInteger)

model += x + y 

model += y >= x - 1 
model += y >= -4 * x + 4 
model += y <= -0.5 * x + 3 

print(model)

model.solve() 

print( LpStatus[model.status] ) 

for var in model.variables():
    print( var.name, "=", var.varValue )

print( value(model.objective) )