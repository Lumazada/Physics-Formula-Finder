class Formula:
    def __init__(self, name, variables, expression):
        self.name = name
        self.vars = variables
        self.var_num = len(self.vars)
        self.expression = expression
        self.foundvar = None


    def dimensionize(self, dimension):
        var_names = []
        dim_vars = []
        for v in self.vars:
            var_names.append(v.name)
        for var in variables:
            if var.name in var_names:
                if var.dim == dimension or var.dim is None:
                    dim_vars.append(var)
        dim_expression = self.expression.replace("x",dimension)
        return Formula(self.name,dim_vars,dim_expression)

class Variable:
    def __init__(self, name, symbol, has_components=False):
        self.has_components = has_components
        self.name = name
        self.symbol = symbol
        self.dim = check_dim(self)


    def dimensionize(self,dimension):
        if self.symbol.count("x") > 0:
            return Variable(self.name, self.symbol.replace("x",dimension))
        else:
            return Variable(self.name, self.symbol+dimension)

def check_dim(var):
    if var.symbol.count("x") > 0:
        return "x"
    if var.symbol.count("y") > 0:
        return "y"
    if var.symbol.count("z") > 0:
        return "z"
    return None


# Kinematics
velocity = Variable("velocity","v", True)
initial_velocity = Variable("initial_velocity","v0", True)
average_velocity = Variable("average_velocity","va", True)
velocity_change = Variable("velocity_change","dv", True)
acceleration = Variable("acceleration","a", True)
initial_position = Variable("initial_position","x0")
position_change = Variable("position_change","dx")
position = Variable("position","x")
time = Variable("time","t")
angle = Variable("angle","A")
# Dynamics
mass = Variable("mass","m")
all_masses = Variable("all_masses","all_mx")
all_positions = Variable("all_positions","all_x")
center_of_mass = Variable("center_of_mass","cmx")
force_of_friction = Variable("force_of_friction","F(f)")

variables = [velocity, initial_velocity, average_velocity, velocity_change, acceleration, initial_position,
             position_change, position, time, angle, mass, all_masses, all_positions, center_of_mass]
for var in variables: ## Add other dimensions
    if var.has_component == True:
        variables.append(var.dimensionize("x"))
for var in variables:
    if var.dim == 'x':
        variables.append(var.dimensionize("y"))
        variables.append(var.dimensionize("z"))
formulas = [
    # Kinematics
    Formula("Average Velocity", [initial_velocity, velocity_component, average_velocity], "vax=(v0x+vx)/2"),
    Formula("Change in Velocity", [initial_velocity, velocity_component, velocity_change], "dvx=vx-v0x"),
    Formula("Velocity", [initial_velocity, acceleration, time, velocity_component], "vx=v0x+ax*t"),
    Formula("Distance", [average_velocity, time, initial_position, position], "x=vax*t+x0"),
    Formula("Distance", [initial_position, initial_velocity, time, acceleration, position], "x=x0+v0x*t+.5*ax*t^2"),
    Formula("Velocity Squared", [initial_velocity, acceleration, initial_position, position, velocity_component], "vx^2=v0x^2+2ax(x-x0)"),
    Formula("Vector Component", [initial_velocity,]) # make this
    # Dynamics
    Formula("Center of Mass", [all_masses, all_positions, center_of_mass], "cmx=(Σmx)/(Σm)")
]
for formula in formulas: # Add dimensions to formulas
    needs_dim = False
    for var in formula.vars:
        if var.dim == "x":
            needs_dim = True
            break
    if needs_dim:
        formulas.append(formula.dimensionize("y"))
        formulas.append(formula.dimensionize("z"))
def solve():
    known = input("Enter Known Information: ").split(",")
    output = input("What are you solving for?: ")
    for var in variables: # change list of strings to list of var objects with dimensions
        for v in known:
            if var.symbol == v:
                known.remove(v)
                known.append(var)
        if var.symbol == output:
            output = var
    solved_formulas = []
    final_formula = None
    solved = False
    failed = False
    while not solved:
        new_formula = False
        for formula in formulas:
            known_var_num = 0
            for var in formula.vars:
                if var in known:
                    known_var_num += 1
            if known_var_num == formula.var_num-1:
                new_formula = True
                solved_formulas.append(formula) #if we can find a new variable with formula, add it to list of solved forms
                for var in formula.vars:
                    if var not in known:
                        known.append(var)
                        formula.foundvar = var
                print(formula.name,formula.foundvar.symbol)
                if output in known:
                    solved = True
                    break
        if not new_formula:
            print("Cannot find Solution")
            failed = True
            break
    if failed:
        return
    for formula in solved_formulas:
        if output in formula.vars:
            final_formula = formula
    for formula in solved_formulas:
        if formula.foundvar in final_formula.vars:
            print(f'{formula.name}: {formula.expression}') # only print useful formulas
            continue
        else:
            for solved_formula in solved_formulas:
                if formula.foundvar in solved_formula.vars and solved_formula.foundvar in final_formula.vars:
                    print(f'{formula.name}: {formula.expression}')

running = True
while running:
    solve()
    if input("again? (y/n)") != "y":
        running = False