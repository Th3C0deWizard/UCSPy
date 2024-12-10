import random
from csp import CSP
from cspsolver import CSPSolver


class LocalSearch(CSPSolver):

    def __init__(self, csp: CSP):
        super().__init__(csp)
        self.max_iterations = 100000

    def solve(self):
        self.assign_all_random()

        print("Initial state")
        self.csp.print_solution()

        i = 0
        while i < self.max_iterations:
            does_not_improve = True
            constraints, solved = self.csp.is_solved()
            if solved:
                break
            variable = None
            new_variable, new_num_ctr = None, None
            for variable, num_ctr in constraints:
                if num_ctr == 0:
                    does_not_improve = False
                    break
                print(
                    "Session with most constraints:\n",
                    variable.course.name,
                    ": ",
                    variable,
                    "\n Number of constraints: ",
                    num_ctr,
                    "\n",
                )
                new_variable, new_num_ctr = (
                    self.csp.select_value_with_fewest_constraints(variable)
                )
                if new_num_ctr <= num_ctr:
                    does_not_improve = False
                    break

                # if no improvement then assign random values to half of the variables, the ones with fewest constraints.
            if does_not_improve:
                random.shuffle(constraints)
                for v, c in constraints[len(constraints) // 2 :]:
                    self.csp.assign_random_value(v)
            else:
                self.csp.equals_variable(variable, new_variable)
            i += 1

        if i == self.max_iterations:
            print("Solution not found")

        print("--------------------------------------------------")
        print("\nFinal State")
        print("Number of iterations: ", i, "\n")
        for v, c in constraints:
            print(v.course.name, ": ", v, "\n Number of constraints: ", c, "\n")
        self.csp.print_solution()

    def assign_all_random(self):
        for variable in self.csp.variables:
            self.csp.assign_random_value(variable)
