def loop_int(num: int, min: int, max) -> int:
    if num < min: return num + (max - min + 1)
    elif num > max: return num - (max - min + 1)
    else: return num