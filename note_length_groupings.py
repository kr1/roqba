"""this module privides constant note-length (rhythm) groupings
pauses should be implemented as a gate on the trigger and 
are not implemented in the groupings
"""



raw_first = [
      # smallest units
      # 8: 8x1
      [[1, 1, 1, 1, 1, 1, 1, 1]] * 3,
      # 7: 6x1 & 1x2
      [[2, 1, 1, 1, 1, 1, 1]] * 6,
      [[1, 2, 1, 1, 1, 1, 1]] * 4,
      [[1, 1, 2, 1, 1, 1, 1]] * 6,
      [[1, 1, 1, 2, 1, 1, 1]] * 4,
      [[1, 1, 1, 1, 2, 1, 1]] * 6,
      [[1, 1, 1, 1, 1, 2, 1]] * 4,
      [[1, 1, 1, 1, 1, 1, 2]] * 6,
      # 6: 5x1 & 1x3
      [[3, 1, 1, 1, 1, 1]] * 2,
      [[1, 3, 1, 1, 1, 1]] * 2,
      [[1, 1, 3, 1, 1, 1]] * 2,
      [[1, 1, 1, 3, 1, 1]] * 2,
      [[1, 1, 1, 1, 3, 1]] * 2,
      [[1, 1, 1, 1, 1, 3]] * 2,
      # 5: 1x4 & 1x4
      [[4, 1, 1, 1, 1]] * 2,
      [[1, 4, 1, 1, 1]] * 2,
      [[1, 1, 4, 1, 1]] * 2,
      [[1, 1, 1, 4, 1]] * 2,
      [[1, 1, 1, 1, 4]] * 2,
      # 4: 1x5 3x1
      [[5, 1, 1, 1]] * 2,
      [[1, 5, 1, 1]] * 2,
      [[1, 1, 5, 1]] * 2,
      [[1, 1, 1, 5]] * 2,
      # 3: 1x6 & 2x1
      [[6, 1, 1]] * 2,
      [[1, 6, 1]] * 2,
      [[1, 1, 6]] * 2,
      # 2: 1x7 & 1x1
      [[7 , 1]] * 2,
      [[1 , 7]] * 2,
      # 1: 1x8
      [[8]] * 1
      ]

raw_second = [
      # second smallest units:
      # 5 3x2 & 2x1
      [[1, 1, 2, 2, 2]] * 8,
      [[2, 1, 1, 2, 2]] * 8,
      [[2, 2, 1, 1, 2]] * 8,
      [[2, 2, 2, 1, 1]] * 8,
      # 4: 4x2
      [[2, 2, 2, 2]] * 10,
      # 3: 1x4 & 2x2
      [[4, 2, 2]] * 8,
      [[2, 4, 2]] * 8,
      [[2, 2, 4]] * 8,
      # 2 1x6 & 1x2
      [[6, 2]] * 6,
      [[2, 6]] * 6,
      ]

raw = raw_first + raw_second

DEFAULT_NOTE_LENGTH_GROUPINGS = sum(raw, [])
DEFAULT_FAST_GROUPINGS = sum(raw_first, [])
DEFAULT_SLOWER_GROUPINGS = sum(raw_second, [])

def analyze_grouping(g):
    res = []
    for item in g:
        first = True
        for n in xrange(item):
            if first:
              res.append(1)
            else:
              res.append(0)
            first = False
    return res

def badly_formeD():
    odd = filter(lambda x: sum(x) != 8, DEFAULT_NOTE_LENGTH_GROUPINGS)
    return odd

if badly_formeD():
    raise RuntimeError, "not all note length groupings are well-formed:\n{0}\n\nin:{1}".format(badly_formeD(),
                                                                                DEFAULT_NOTE_LENGTH_GROUPINGS)

if __name__ == "__main__":
    import pprint as pp
    pp.pprint(DEFAULT_NOTE_LENGTH_GROUPINGS)

    ## TEST analyze_grouping
    res = analyze_grouping([1,2,1,3])
    assert res == [1,1,0,1,1,0,0]
    print res
