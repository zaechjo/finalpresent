from enum import Enum

class State(Enum):
    START = 1
    QUESTION = 2
    AFTER_QUESTION = 3
    INFO_PAGE = 4
    OUTPUT = 5