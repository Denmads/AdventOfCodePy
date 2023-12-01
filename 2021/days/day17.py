from DailyAssignment import DailyAssignment

class ProbeTrajectory(DailyAssignment):
    def __init__(self):
        super().__init__(17)

    def run_part_a(self, input: str):
        min_coords, max_coords = parse_target_area(input)
        max_y_vel = abs(min_coords[1])-1
        max_height = (max_y_vel * (max_y_vel+1)) / 2
        print(max_height)

    def run_part_b(self, input: str):
        min_coords, max_coords = parse_target_area(input)
        max_y_vel = abs(min_coords[1])-1
        max_x_vel = max_coords[0]

        #check x values
        x_vels = []
        for vel in range(1, max_x_vel+1):
            x_vel = vel
            x_pos = 0
            while x_pos <= max_coords[0]:
                x_pos += x_vel
                if within_target_zone(min_coords, max_coords, (x_pos, min_coords[1])):
                    x_vels.append(vel)
                    break
                x_vel -= 1
                if x_vel == 0:
                    break
        
        #check y values
        y_vels = []
        for vel in range(min_coords[1], max_y_vel+1):
            y_vel = vel
            y_pos = 0
            while y_pos >= min_coords[1]:
                y_pos += y_vel
                if within_target_zone(min_coords, max_coords, (min_coords[0], y_pos)):
                    y_vels.append(vel)
                    break
                y_vel -= 1

        #find pairs
        pairs = []
        for y_vel in y_vels:
            for x_vel in x_vels:
                x_temp = x_vel
                y_temp = y_vel
                x_pos = 0
                y_pos = 0
                while x_pos <= max_coords[0] and y_pos >= min_coords[1]:
                    x_pos += x_temp
                    y_pos += y_temp
                    if within_target_zone(min_coords, max_coords, (x_pos, y_pos)):
                        pairs.append((x_vel, y_vel))
                        break
                    x_temp -= 1 if x_temp > 0 else 0
                    y_temp -= 1
        
        print(len(pairs))

def within_target_zone(minp, maxp, coord):
    return minp[0] <= coord[0] <= maxp[0] and minp[1] <= coord[1] <= maxp[1]

def parse_target_area(input):
    parts = input.split(" ")
    x_range = parts[2][2:-1].split("..")
    y_range = parts[3][2:].split("..")
    x = tuple(map(int, x_range))
    y = tuple(map(int, y_range))
    return ((x[0], y[0]), (x[1], y[1]))