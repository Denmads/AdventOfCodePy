from DailyAssignment import DailyAssignment

def have_same_char(id, count):
    chars = set(id)
    for char in chars:
        if id.count(char) == count:
            return True
    return False

def compare_ids(id1, id2):
    for i in range(len(id1)):
        mod_1 = id1[:i] + id1[i+1:]
        mod_2 = id2[:i] + id2[i+1:]
        if mod_1 == mod_2:
            return mod_1
    return None

class BoxIDs(DailyAssignment):
    def __init__(self):
        super().__init__(2)

    def run_part_a(self, input: str):
        ids = input.split("\n")
        two_count = 0
        three_count = 0
        for id in ids:
            two_count += 1 if have_same_char(id, 2) else 0
            three_count += 1 if have_same_char(id, 3) else 0

        print(f"The checksum is '{two_count * three_count}'")

    def run_part_b(self, input: str):
        ids = input.split("\n")
        for i in range(len(ids)-1):
            for j in range(i+1, len(ids)):
                res = compare_ids(ids[i], ids[j])
                if res is not None:
                    print(f"Common letters '{res}'")
                    return
        print("No almost identical ids!")