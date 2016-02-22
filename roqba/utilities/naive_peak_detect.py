def detect_local_extrema(array):
    minima = {}
    maxima = {}
    pre = array[0]
    num = array[1]
    for idx in range(1, len(array)):
        post = array[idx]
        if pre < num > post:
            maxima[idx - 1] = num
        if pre > num < post:
            minima[idx - 1] = num
        pre = num
        num = post
    return minima, maxima
