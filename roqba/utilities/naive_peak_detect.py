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
