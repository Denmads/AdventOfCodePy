from typing import List
from DailyAssignment import DailyAssignment
from dataclasses import dataclass, field

@dataclass
class Step:

    def __init__(self, letter):
        self.letter = letter
        self.required_steps = []
        self.next_steps = []
        self.done = False
    
    def add_required_step(self, step):
        self.required_steps.append(step)

    def add_next_step(self, step):
        self.next_steps.append(step)

    def __eq__(self, other):
        return self.letter == other.letter

    def __repr__(self) -> str:
        return f"(letter={self.letter}, required_steps=[{', '.join(map(lambda x: x.letter, self.required_steps))}], next_steps=[{', '.join(map(lambda x: x.letter, self.next_steps))}], done={self.done})"

@dataclass
class StepList:
    steps: List[Step] = field(default_factory=list)

    def add(self, step):
        self.steps.append(step)

    def get_next(self):
        return self.steps.pop(0)

    def sort(self):
        self.steps.sort(key=lambda x: x.letter)

    def __len__(self):
        return len(self.steps)

    def __contains__(self, step):
        return step in self.steps

@dataclass
class Worker:
    id: int
    base_task_time: int
    available_steps: StepList
    steps_done: StepList
    wait_time: int = 0
    current_step: Step = None

    def is_free(self):
        return self.wait_time == 0

    def do_step(self, step):
        self.current_step = step
        self.wait_time = self.base_task_time + (ord(step.letter) - 64)

    def decrease_time(self):
        if self.wait_time > 0:
            self.wait_time -= 1
            if self.wait_time == 0 and self.current_step is not None:
                self.current_step.done = True
                self.steps_done.add(self.current_step)
                next_valid_steps = find_valid_next_steps(self.current_step)
                for next_step in next_valid_steps:
                    if next_step not in self.available_steps:
                        self.available_steps.add(next_step)
                        self.available_steps.sort()
                self.current_step = None


class SomeAssemblyRequired(DailyAssignment):
    def __init__(self):
        super().__init__(7)

    def run_part_a(self, input: str):
        steps = parse_steps(input)
        available_steps = find_first_steps(steps)
        steps_done = []

        while len(available_steps) > 0:
            available_steps.sort(key=lambda x: x.letter)
            step = available_steps.pop(0)
            step.done = True
            steps_done.append(step)
            next_valid_steps = find_valid_next_steps(step)
            for next_step in next_valid_steps:
                if next_step not in available_steps:
                    available_steps.append(next_step)
            
        step_order = "".join(map(lambda x: x.letter, steps_done))
        print(f"The steps should be done in the following order '{step_order}'")

    def run_part_b(self, input: str):
        steps = parse_steps(input)
        available_steps = StepList()
        [available_steps.add(step) for step in find_first_steps(steps)]
        available_steps.sort()
        steps_done = StepList()
        workers = [Worker(id, 60, available_steps, steps_done) for id in range(5)]

        time_step = 0

        while len(available_steps) > 0 or not all_workers_free(workers):
            for worker in workers:
                if worker.is_free() and len(available_steps) > 0:
                    step = available_steps.get_next()
                    worker.do_step(step)
                
            for worker in workers:
                worker.decrease_time()

            time_step += 1

        print(f"It takes {time_step} seconds, to complete all the steps.")

def all_workers_free(workers):
    all_free = True
    for worker in workers:
        all_free = all_free and worker.is_free()
    return all_free

def find_valid_next_steps(step):
    valid_steps = []
    for next_step in step.next_steps:
            if next_step.done:
                continue

            all_done = True
            for req_step in next_step.required_steps:
                all_done = all_done and req_step.done
            if all_done and next_step:
                valid_steps.append(next_step)
    return valid_steps

def find_first_steps(steps):
    first = []
    for step in steps.values():
        if len(step.required_steps) == 0:
            first.append(step)
    return first

def parse_steps(input):
    lines = input.split("\n")

    all_steps = {}
    for line in lines:
        tokens = line.split(" ")
        prev_step_let = tokens[1]
        step_let = tokens[7]

        if step_let not in all_steps:
            step = Step(step_let)
            all_steps[step_let] = step
        else:
            step = all_steps[step_let]

        if prev_step_let not in all_steps:
            prev_step = Step(prev_step_let)
            all_steps[prev_step_let] = prev_step
        else:
            prev_step = all_steps[prev_step_let]

        step.add_required_step(prev_step)
        prev_step.add_next_step(step)
    return all_steps
