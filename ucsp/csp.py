from typing import List, Tuple, Any

"""
    represents an interface to describe constraint satisfaction problems
"""


class CSP:

    def __init__(self, variables: List):
        self.variables = variables

    def is_solved(self) -> Tuple[dict[Any, int], bool]:
        pass

    def check_constraints(self, variable):
        pass

    def select_value_with_fewest_constraints(self, variable):
        pass

    def assign_random_value(self, variable):
        pass

    def equals_variable(self, variable, new_variable):
        pass

    def print_solution(self):
        pass
