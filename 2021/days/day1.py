from DailyAssignment import DailyAssignment

class SeaFloorDepth(DailyAssignment):
    def __init__(self):
        super().__init__(1)

    def run_part_a(self, input: str):
        depths = list(map(lambda x: int(x), input.split("\n")))
        increases = 0
        for i in range(1, len(depths)):
            if depths[i-1] < depths[i]:
                increases += 1
            
        print(f"{increases} increases counted!")

    def run_part_b(self, input: str):
        depths = list(map(lambda x: int(x), input.split("\n")))
        increases = 0
        for i in range(0, len(depths)):
            window_a = sum(depths[i:i+3])
            window_b = sum(depths[i+1:i+4])
            if window_a < window_b:
                increases += 1
            
        print(f"{increases} increases counted!")

