from DailyAssignment import DailyAssignment
from dataclasses import dataclass
from enum import IntEnum

@dataclass
class TimeStamp:
    year: int
    month: int
    day: int
    hour: int
    minute: int

class GuardAction(IntEnum):
    WAKES_UP = 0
    FALLS_ASLEEP = 1

@dataclass
class Event:
    timestamp: TimeStamp
    guard_id: str
    action: GuardAction

class Guard:
    def __init__(self, id):
        self.id = id
        self.sleep_times = []

    def add_sleep_time(self, start, end):
        self.sleep_times.append((start, end))

    def total_time_Slept(self):
        time = 0
        for sleep in self.sleep_times:
            time += sleep[1].timestamp.minute - sleep[0].timestamp.minute
        return time
    
    def count_times_slept_at_minute(self, minute):
        times_slept = 0
        for sleep in self.sleep_times:
            if sleep[0].timestamp.minute <= minute and sleep[1].timestamp.minute > minute:
                times_slept += 1
        return times_slept


class SleepyGuards(DailyAssignment):
    def __init__(self):
        super().__init__(4)

    def run_part_a(self, input: str):
        events = parse_events(input)
        guards = create_guards(events)
        
        times = [(guard.total_time_Slept(), guard) for guard in guards.values()]
        guard = max(times, key=lambda item: item[0])[1]

        sleep_minutes = [(min, guard.count_times_slept_at_minute(min)) for min in range(0, 60)]
        max_minute = max(sleep_minutes, key=lambda item: item[1])

        print(f"ID: {guard.id}")
        print(f"Minute: {max_minute[0]}")
        print(f"Result '{int(guard.id) * max_minute[0]}'")

    def run_part_b(self, input: str):
        events = parse_events(input)
        guards = create_guards(events)

        all_combs = []
        for guard in guards.values():
            for min in range(0, 60):
                all_combs.append((
                    guard.id,
                    min,
                    guard.count_times_slept_at_minute(min)
                ))

        max_frequency = max(all_combs, key=lambda x: x[2])
        
        print(f"ID: {max_frequency[0]}")
        print(f"Minute: {max_frequency[1]}")
        print(f"Result '{int(max_frequency[0]) * max_frequency[1]}'")
        
def create_guards(events):
    guards = {}
    index = 0
    while index < len(events):
        event = events[index]
        if event.guard_id not in guards:
            guards[event.guard_id] = Guard(event.guard_id)
        guards[event.guard_id].add_sleep_time(event, events[index+1])
        index += 2
    return guards

def parse_timestamp(input):
    tokens = input[1:].split(" ")
    date = list(map(lambda x: int(x), tokens[0].split("-")))
    time = list(map(lambda x: int(x), tokens[1].split(":")))
    return TimeStamp(date[0], date[1], date[2], time[0], time[1])

def parse_events(input):
    lines = list(map(lambda x: x.split("] "), input.split("\n")))
    lines.sort(key=lambda x: x[0])
    last_guard_id = None
    events = []
    for line in lines:
        timestamp = parse_timestamp(line[0])
        action = line[1]
        if action.startswith("G"):
            last_guard_id = action.split(" ")[1][1:]
        elif action.startswith("w"):
            events.append(Event(timestamp, last_guard_id, GuardAction.WAKES_UP))
        elif action.startswith("f"):
            events.append(Event(timestamp, last_guard_id, GuardAction.FALLS_ASLEEP))
    return events
            

