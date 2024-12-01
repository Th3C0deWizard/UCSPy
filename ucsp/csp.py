from typing import List

"""
    represents an interface to describe constraint satisfaction problems
"""


class CSP:

    def __init__(self, variables: List):
        self.variables = variables

    def get_domain(self, variable):
        pass

    def check_constraints(self, variable):
        pass

    def is_solved(self) -> bool:
        pass
