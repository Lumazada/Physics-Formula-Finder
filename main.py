class Formula:
    def __init__(self, name, variables, expression):
        self.name = name
        self.vars = variables
        self.var_num = len(self.vars)
        self.expression = expression
        self.foundvar = None


# Kinematics
velocity, initial_velocity, average_velocity, velocity_change, acceleration, gravity = "v", "v0", "va", "dv", "a", "g"
initial_position, position_change, position, time = "x0", "dx", "x", "t"

formulas = [
    # Kinematics
    Formula("Average Velocity", [initial_velocity, velocity, average_velocity], "va=(v0+v)/2"),
    Formula("Change in Velocity", [initial_velocity, velocity, velocity_change], "dv=v-v0"),
    Formula("Velocity", [initial_velocity, acceleration, time, velocity], "v=v0+a*t"),
    Formula("Distance (no acceleration)", [average_velocity, time, initial_position, position], "x=va*t+x0"),
    Formula("Distance (with acceleration)", [initial_position, initial_velocity, time, acceleration, position], "x=x0+v0*t+.5*a*t^2"),
    Formula("Velocity Squared", [initial_velocity, acceleration, initial_position, position, velocity], "v^2=v0^2+2a(x-x0)")
]
print(formulas)
known = input("Enter Known Information: ").split(",")
found = []
output = input("What are you solving for?: ")
solved_formulas = []
final_formula = None
solved = False
while not solved:
    for formula in formulas:
        known_var_num = 0
        for var in formula.vars:
            if var in known:
                known_var_num += 1
        if known_var_num == formula.var_num-1:
            solved_formulas.append(formula)
        if formula in solved_formulas:
            for var in formula.vars:
                if var not in known:
                    known.append(var)
                    found.append(var)
                    formula.foundvar = var
            if output in known:
                solved = True
                break
for formula in solved_formulas:
    if output in formula.vars:
        final_formula = formula
for formula in solved_formulas:
    if formula.foundvar in final_formula.vars:
        print(f'{formula.name}: {formula.expression}')
        continue
    else:
        for solved_formula in solved_formulas:
            if formula.foundvar in solved_formula.vars and solved_formula.foundvar in final_formula.vars:
                print(f'{formula.name}: {formula.expression}')
