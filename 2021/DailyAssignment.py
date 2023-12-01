import abc

class DailyAssignment(abc.ABC):
    def __init__(self, day_index: int):
        self.day_index = day_index

    @abc.abstractmethod    
    def run_part_a(self, input: str):
        ...

    @abc.abstractmethod
    def run_part_b(self, input: str):
        ...