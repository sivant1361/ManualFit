eqn = input("enter the equation: ")
constants = input("enter the constants separated with comma: ")
variables = input("enter the variables separated with comma: ")

const_dict = {}
var_dict = {}

for i in constants.split(","):
        const_dict[i] = 0
        
for i in variables.split(","):
        var_dict[i] = 0

for i in const_dict.keys():
    const_dict[i] = float(input("Enter the value of "+str(i)+": "))

for i in var_dict.keys():
    var_dict[i] = float(input("Enter the value of "+str(i)+": "))

for i in const_dict.keys():
    exec("%s = %f"%(i,const_dict[i]))

for i in var_dict.keys():
    exec("%s = %f"%(i,var_dict[i]))

print(eval(eqn))