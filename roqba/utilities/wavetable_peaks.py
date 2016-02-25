import itertools


def detect_local_extrema(array):
    extrema = {}

    pre = array[0]
    num = array[1]
    for idx in range(1, len(array)):
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
        if extrema[start] == extrema[end]:
            continue
        elif extrema[start] > extrema[end]:
            target = downwards
        else:
            target = upwards
        target.append({
            'start': (start, extrema[start]),
            'end': (end, extrema[end])})
    passages = {
        'upwards': upwards,
        'downwards': downwards,
    }
    return passages
