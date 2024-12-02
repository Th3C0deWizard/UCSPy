from csp import CSP
from cspsolver import CSPSolver


class LocalSearch(CSPSolver):

    def __init__(self, csp: CSP):
        super().__init__(csp)

    def solve(self):
        self.assign_all_random()

        print("Initial state")
        for var in self.csp.variables:
            print(var)
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            )

        i = 0
        while True:
            num_constraints, solved = self.csp.is_solved()
            if solved:
                break
            variable = max(num_constraints, key=num_constraints.get)
            print(
                "Variable with most constraints: ",
                variable,
                " with ",
                num_constraints[variable],
                " constraints",
            )
            new_variable = self.csp.select_value_with_fewest_constraints(variable)
            self.csp.equals_variable(variable, new_variable)
            i += 1

        print("\nFinal State")
        print("Number of iterations: ", i)
        for var in self.csp.variables:
            print(var)
            print(
                "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
            )

    def assign_all_random(self):
        for variable in self.csp.variables:
            self.csp.assign_random_value(variable)
