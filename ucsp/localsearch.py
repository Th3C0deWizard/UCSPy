from csp import CSP
from cspsolver import CSPSolver


class LocalSearch(CSPSolver):

    def __init__(self, csp: CSP):
        super().__init__(csp)

    def solve(self):
        return super().solve()

    def assign_all_random(self):
        return super().assign_all_random()

    def select_variable(self):
        return super().select_variable()

    def assign_value(self, variable):
        return super().assign_value(variable)
