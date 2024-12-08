from csp import CSP
from cspsolver import CSPSolver


class LocalSearch(CSPSolver):

    def __init__(self, csp: CSP):
        super().__init__(csp)

    def solve(self):
        self.assign_all_random()

        print("Initial state")
        self.csp.print_solution()

        i = 0
        while True:
            num_constraints, solved = self.csp.is_solved()
            if solved:
                break
            variable = max(num_constraints, key=num_constraints.get)
            print(
                "Session with most constraints:\n",
                variable.course.name,
                ": ",
                variable,
                "\n Number of constraints: ",
                num_constraints[variable],
                "\n",
            )
            new_variable = self.csp.select_value_with_fewest_constraints(variable)
            self.csp.equals_variable(variable, new_variable)
            i += 1

        print("--------------------------------------------------")
        print("\nFinal State")
        print("Number of iterations: ", i, "\n")
        self.csp.print_solution()

    def assign_all_random(self):
        for variable in self.csp.variables:
            self.csp.assign_random_value(variable)
