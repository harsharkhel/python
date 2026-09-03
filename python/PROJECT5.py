import numpy as np

length = 20      # road has 20 cells
v_max = 3        # fastest a car can go
p_slow = 0.3     # 30% chance a car randomly slows down

# -1 means empty cell. A number 0-3 means a car going that speed.
road = np.full(length, -1)
road[[2, 5, 6, 12, 15]] = [2, 0, 1, 3, 2]   # place 5 cars with starting speeds

def step(road):
    positions = np.flatnonzero(road >= 0)      # where the cars are
    speeds = road[positions]                    # how fast each one goes

    # gap = how many empty cells until the next car (wraps around the road)
    order = np.argsort(positions)
    sorted_pos = positions[order]
    gaps = np.empty_like(sorted_pos)
    gaps[:-1] = sorted_pos[1:] - sorted_pos[:-1] - 1
    gaps[-1] = (sorted_pos[0] + length) - sorted_pos[-1] - 1
    gap = np.empty_like(gaps)
    gap[order] = gaps

    speeds = np.minimum(speeds + 1, v_max)       # 1. speed up a little
    speeds = np.minimum(speeds, gap)             # 2. but not into the car ahead
    slow = np.random.random(len(speeds)) < p_slow
    speeds = np.where(slow, np.maximum(speeds - 1, 0), speeds)  # 3. random braking

    new_positions = (positions + speeds) % length  # 4. move forward
    new_road = np.full(length, -1)
    new_road[new_positions] = speeds
    return new_road

for t in range(10):
    print(road)
    road = step(road)