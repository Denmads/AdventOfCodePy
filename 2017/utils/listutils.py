def subgroup_list(items: list, group_size: int, fill_value):
    copy = items.copy()
    while len(items) % group_size != 0:
        copy.append(fill_value)
    
    return [copy[i:i+group_size] for i in range(0, len(copy), group_size)]