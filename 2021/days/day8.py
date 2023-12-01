from DailyAssignment import DailyAssignment

class SevenSegmentAnalysis:

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.segments = {}

        self.numbers = {
            "abcefg": 0,
            "cf": 1,
            "acdeg": 2,
            "acdfg": 3,
            "bcdf": 4,
            "abdfg": 5,
            "abdefg": 6,
            "acf": 7,
            "abcdefg": 8,
            "abcdfg": 9
        }

    def get_input_with_length(self, length):
        res = []
        for inp in self.inputs:
            if len(inp) == length: res.append(inp)
        return res

    def configure(self):
        sig_1 = self.get_input_with_length(2)[0]
        sig_4 = self.get_input_with_length(4)[0]
        sig_7 = self.get_input_with_length(3)[0]
        sig_8 = self.get_input_with_length(7)[0]

        # HOR EDGES
        # 1 - 7: find top edge
        top_edge = list(set(sig_7) - set(sig_1))[0]
        self.segments[top_edge] = "a"

        # 3 x 5 segs - find 3 horizontal edges contained in all three
        five_segs = self.get_input_with_length(5)
        hor_edges = []
        for ch in five_segs[0]:
            if ch in five_segs[1] and ch in five_segs[2]:
                hor_edges.append(ch)

        # 4 - find middle edge using prev result
        middle_edge = None
        for ch in sig_4:
            if ch in hor_edges:
                middle_edge = ch
                break
        self.segments[middle_edge] = "d"

        # find lower edge from remainder in three set
        lower_edge = list(set(hor_edges) - set([top_edge, middle_edge]))[0]
        self.segments[lower_edge] = "g"
        
        #VER EDGES
        #lower left - diff between 4 and 8
        four_min_hor = list(set(sig_4) - set(hor_edges))
        vert_edges = list(set(sig_8) - set(hor_edges))
        lower_left_edge = list(set(vert_edges) - set(four_min_hor))[0]
        self.segments[lower_left_edge] = "e"

        #upper right - test: remove all hor edges and lower left ver edge, when one remains it is the upper right
        upper_right_edge = None
        for signal in self.inputs:
            remains = list(set(signal) - set(hor_edges) - set(lower_left_edge))
            if len(remains) == 1:
                upper_right_edge = remains[0]
                break
        self.segments[upper_right_edge] = "c"

        #lower right - test: 7 - top edge - upper right edge
        lower_right_edge = list(set(sig_7) - set([top_edge, upper_right_edge]))[0]
        self.segments[lower_right_edge] = "f"

        #upper left - test: find 8 and remove all hor edges and three ver edges found so far, the one remaining is the upper left
        upper_left_edge = list(set(sig_8) - set(hor_edges) - set(upper_right_edge) - set(lower_right_edge) - set(lower_left_edge))[0]
        self.segments[upper_left_edge] = "b"

    def get_digit(self, op):
        res = []
        for ch in op:
            res.append(self.segments[ch])
        res.sort()
        res = "".join(res)
        return self.numbers[res]


    def get_output(self):
        res = ""
        for op in self.outputs:
            res += str(self.get_digit(op))
        return int(res)

class WireMess(DailyAssignment):
    def __init__(self):
        super().__init__(8)

    def run_part_a(self, input: str):
        entries = parse_inputs_and_outputs(input)
        count_outs = 0
        for entry in entries:
            for out in entry["outputs"]:
                if len(out) in [2, 3, 4, 7]:
                    count_outs += 1
        print(count_outs)

    def run_part_b(self, input: str):
        entries = parse_inputs_and_outputs(input)
        analysis = list(map(lambda x: SevenSegmentAnalysis(x["inputs"], x["outputs"]), entries))
        for a in analysis:
            a.configure()
        total = 0
        for a in analysis:
            total += a.get_output()
        print(total)

def parse_inputs_and_outputs(input):
    lines = input.split('\n')
    entries = []
    for line in lines:
        parts = line.split(" | ")
        entries.append({
            "inputs": parts[0].split(" "),
            "outputs": parts[1].split(" "),
        })
    return entries