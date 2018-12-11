import itertools


def detect_local_extrema(array):
    extrema = {}
    pre = array[0]
    num = array[1]
    for idx in range(2, len(array)):
        post = array[idx]
        if pre < num > post or pre > num < post:
            extrema[idx - 1] = num
        pre = num
        num = post
    return extrema


def extract_peak_passages(array):
    upwards = []
    downwards = []
    extrema = detect_local_extrema(array)
    all_ = itertools.permutations(extrema.keys(), 2)
    for start, end in all_:
        startval = extrema[start]
        endval = extrema[end]
        if startval == endval:
            continue
        elif startval > endval:
            target = downwards
        else:
            target = upwards

        in_between = [(key, value) for key, value in extrema.items()
                      if start < key < end or end < key < start]
        if not in_between:
            deviation = 1
        else:
            min_ = min([val for key, val in in_between])
            max_ = max([val for key, val in in_between])
            full_range = sorted([min_, max_, startval, endval])
            full_range = abs(full_range[0] - full_range[-1])
            deviation = full_range / abs(startval - endval)
        target.append({
            'start': (start, startval),
            'end': (end, endval),
            'deviation': deviation,
            'in_between': in_between})
    passages = {
        'upwards': upwards,
        'downwards': downwards,
    }
    return passages
