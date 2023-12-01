from dataclasses import dataclass, field
from functools import reduce
from typing import Callable, Union


@dataclass
class MonkeyItem:
    value: int
    next: 'MonkeyItem' = field(default=None)

class Monkey:
    @staticmethod
    def parse(data: str) -> 'Monkey':
        lines = data.split("\n")
        
        id = int(lines[0][7:-1])
        items = list(map(lambda i: int(i), lines[1].strip()[16:].split(", ")))
        worry_op = lines[2].strip()[17:].split()
        test_arg = int(lines[3].strip()[19:])
        true_index = int(lines[4].strip()[25:])
        false_index = int(lines[5].strip()[26:])

        def worry_transform(x: int) -> int:
            left = x if worry_op[0] == "old" else int(worry_op[0])
            right = x if worry_op[2] == "old" else int(worry_op[2])

            if worry_op[1] == "+": return left + right
            elif worry_op[1] == "*": return left * right

        def test_func(x: int) -> bool:
            return x % test_arg == 0

        return Monkey(id, items, worry_transform, test_arg, test_func, true_index, false_index)

    def __init__(self, id: int, items: list[int], worry_transform: Callable[[int], int], test_arg: int, test_function: Callable[[int], bool], true_monkey_index: int, false_monkey_index: int):
        self.id = id
        self.worry_transform = worry_transform
        self.test_function = test_function

        self._create_initial_items(items)

        self.test_arg = test_arg

        self.true_monkey_index = true_monkey_index
        self.false_monkey_index = false_monkey_index
        
        self.true_monkey = None
        self.false_monkey = None
        self.inspect_count = 0

        def manage(n: int) -> int:
            return n // 3

        self.manage_func = manage

    def _create_initial_items(self, items: list[int]):
        monkey_items = [MonkeyItem(i) for i in items]

        for i in range(len(monkey_items)):
            item = monkey_items[i]

            if i-1 >= 0:
                item.prev = monkey_items[i-1]

            if i+1 < len(monkey_items):
                item.next = monkey_items[i+1]

        self.items_head = monkey_items[0]
        self.items_tail = monkey_items[-1]


    def resolve_monkeys(self, monkeys: list['Monkey']):
        self.true_monkey = monkeys[self.true_monkey_index]
        self.false_monkey = monkeys[self.false_monkey_index]

    def do_turn(self):
        item = self._next_item()
        while item is not None:
            self.inspect_count += 1
            item.value = self.manage_func(self.worry_transform(item.value))
            
            if self.test_function(item.value):
                self.true_monkey.give(item)
            else:
                self.false_monkey.give(item)

            item = self._next_item()
                

    def _next_item(self) -> Union[MonkeyItem, None]:
        if self.items_head is None: return None

        item = self.items_head
        self.items_head = item.next

        if item.next is None:
            self.items_tail = None

        item.next = None
        return item


    def give(self, item: MonkeyItem):

        if self.items_head is None:
            self.items_head = item
            self.items_tail = item
        else:
            self.items_tail.next = item
            self.items_tail = item


# //////////////////// PARSING /////////////////////////

def parse_input(data: str) -> list[Monkey]:
    sections = data.split("\n\n")
    monkeys = list(map(lambda s: Monkey.parse(s), sections))
    for monkey in monkeys:
        monkey.resolve_monkeys(monkeys)
    return monkeys


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Monkey]):
    NUM_ROUNDS = 20

    for i in range(NUM_ROUNDS):
        print(f"Round {i}")
        for monkey in data:
            print(f"Monkey {monkey.id}")
            monkey.do_turn()
    
    inspect_counts = sorted(map(lambda m: m.inspect_count, data), reverse=True)

    print(f"Sum of two largest: {inspect_counts[0] * inspect_counts[1]}")


def run_b(data: list[Monkey]):
    NUM_ROUNDS = 10000

    common = reduce(lambda x, y: x * y, map(lambda m: m.test_arg, data))
    def new_manage(n: int) -> int:
        return n % common
    
    for monkey in data:
        monkey.manage_func = new_manage

    for i in range(NUM_ROUNDS):
        # print(f"Round {i}")
        for monkey in data:
            monkey.do_turn()
    
    inspect_counts = sorted(map(lambda m: m.inspect_count, data), reverse=True)

    print(f"Sum of two largest: {inspect_counts[0] * inspect_counts[1]}")