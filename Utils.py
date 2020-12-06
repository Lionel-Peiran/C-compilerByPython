from enum import Enum

#   Action Table Enum
class ActionState(Enum):
    Reduce = 1
    Shift = 2
    Accept = 3
Empty_Symbol = "ε"