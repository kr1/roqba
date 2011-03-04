"""this module privides constant note-length (rhythm) groupings
pauses should be implemented as a gate on the trigger and
are not implemented in the groupings

reconsider specifying pauses with negative values(to-do:
check implcations on other modules)
"""

DEFAULT_METER_LENGTH = 8

groupings = {8:
{"first": [
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
      [[7, 1]] * 2,
      [[1, 7]] * 2,
      # 1: 1x8
      [[8]] * 1
      ],

"second": [
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
      ],

"terns": [
      # second smallest units:
      #  2x3 & 2x1
      [[3, 3, 1, 1]] * 8,
      [[3, 1, 1, 3]] * 3,
      [[1, 1, 3, 3]] * 8,
      #  2x3 & 2x1
      [[2, 3, 3]] * 8,
      [[3, 2, 3]] * 3,
      [[3, 3, 2]] * 8,
      # 2 x (2, 1) & 2x1
      [[2, 2, 1, 2, 1]] * 8,
      [[2, 1, 2, 2, 1]] * 5,
      [[2, 1, 2, 1, 2]] * 8,
      ],

"heavy": [
      # 5 3x2 & 2x1
      [[2, 1, 1, 2, 2]] * 3,
      [[2, 2, 1, 1, 2]] * 3,
      [[2, 2, 2, 1, 1]] * 3,

      # 6 2x2 & 4x1
      [[2, 1, 1, 2, 1, 1]] * 3,
      [[1, 1, 2, 1, 1, 2]] * 3,
      # 4: 4x2
      [[2, 2, 2, 2]] * 5,
      # 3: 1x4 & 2x2
      [[4, 2, 2]] * 8,
      [[2, 4, 2]] * 8,
      [[2, 2, 4]] * 8,
      # 5 1x4 & 1x2 & 2x1
      [[4, 2, 1, 1]] * 3,
      [[2, 1, 1, 4]] * 3,
      [[1, 1, 4, 2]] * 3,
      [[4, 1, 1, 2]] * 3,
      [[1, 1, 2, 4]] * 3,
      [[4, 1, 1, 2]] * 3,
      # 2 1x6 & 1x2
      [[6, 2]] * 6,
      [[2, 6]] * 6,
      ]
  },
  (5, (2, 3)):
  {"heavy": [
      [[5]] * 7,
      [[2, 3]] * 20,
      [[2, 2, 1]] * 5,

      [[1, 1, 3]] * 5,
      [[1, 1, 2, 1]] * 5,
      [[1, 1, 1, 1, 1]] * 5,
      [[2, 1, 1, 1]] * 5
    ]
  },
  (5, (3, 2)):
  {"heavy": [
      [[5]] * 7,
      [[3, 2]] * 20,
      [[2, 1, 2]] * 5,

      [[1, 1, 1, 2]] * 5,
      [[1, 1, 1, 1, 1]] * 5,
      [[2, 1, 1, 1]] * 5
    ]
  },
  6:
  {"heavy": [
  [[6]] * 3,
  [[3, 3]] * 15,
  [[3, 2, 1]] * 3,
  [[2, 1, 2, 1]] * 6,
  [[3, 1, 1, 1]] * 3,
  [[1, 1, 1, 3]] * 3,
  [[2, 2, 2]] * 4,
  ]
  },
  (7, (3, 2, 2)):
  {"heavy": [
      [[5, 2]] * 7,
      [[3, 2, 2]] * 20,
      [[2, 1, 2, 2]] * 7,

      [[1, 1, 1, 2, 2]] * 5,
      [[1, 1, 1, 1, 1, 1, 1]] * 5,
      [[2, 1, 1, 1, 1, 1]] * 7,
      [[1, 1, 1, 1, 1, 2]] * 5,
      [[2, 1, 2, 1, 1]] * 7
    ]
  },
  (9, (3, 3, 3)):
  {"heavy": [
      [[6, 3]] * 7,
      [[3, 6]] * 7,
      [[3, 3, 3]] * 30,
      [[2, 1, 2, 1, 2, 1]] * 7,

      [[1, 1, 1, 1, 1, 1, 1, 1, 1]] * 5,
      [[2, 1, 1, 1, 1, 1, 1, 1]] * 5,
      [[2, 1, 2, 1, 1, 1, 1]] * 7,
      [[3, 3, 1, 1, 1]] * 5,
      [[3, 2, 1, 1, 2]] * 7
    ]
  }
}


def get_grouping(meter, mode, check=True):
    '''returns the groupings for a given meter and mode

    well_foredness is checked by default, "default"-mode
    will combine first, second and terns-modes
    '''
    mode = None if mode == "default" else mode
    meter_length = meter if type(meter) == int else meter[0]
    res = assemble(meter, mode, meter_length=meter_length)
    if check:
        if badly_formeD(meter_length, res):
            raise RuntimeError("badly formed rhythm grouping.")
    return res


def assemble(id, which=None, fallback=True, meter_length=DEFAULT_METER_LENGTH):
    if id not in groupings.keys():
        raise RuntimeError("KeyError: specified meter not found.")
    target = groupings[id]
    
    if which:
        if which not in target.keys():
            if fallback:
                res = groupings[DEFAULT_METER_LENGTH][which]
                return cut_grouping_to_size(sum(res,[]), meter_length)
            else:
                raise RuntimeError("non-existing meter mode")
        else:
            return sum(target[which], [])
    else:
        return assemble(id, "first", fallback, meter_length) +\
               assemble(id, "second", fallback, meter_length) +\
               assemble(id, "terns", fallback, meter_length)
        return sum(target["first"] +
                   target["second"] +
                   target["terns"], [])

def cut_grouping_to_size(grouping, size):
    res = []
    for group in grouping:
        new = []
        for i in group:
            new.append(i)
            sum_ = sum(new)
            if sum_ >= size:
                new.pop()
                diff = size -sum(new)
                if diff != 0:
                    new.append(abs(diff))
                break
        if sum_ < size:
            new.append(size - sum_)
        res.append(new)
    return res

DEFAULT_NOTE_LENGTH_GROUPINGS = assemble(DEFAULT_METER_LENGTH)
DEFAULT_FAST_GROUPINGS = assemble(DEFAULT_METER_LENGTH, "first")
DEFAULT_TERNARY_GROUPINGS = assemble(DEFAULT_METER_LENGTH, "terns")
DEFAULT_SLOWER_GROUPINGS = assemble(DEFAULT_METER_LENGTH, "heavy")


def analyze_grouping(g):
    """transform the grouping into a nibary pattern for every beat, i.e.:

    >>> analyze_grouping([1,2,1,3])
    [1, 1, 0, 1, 1, 0, 0]
    """
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


def badly_formeD(meter_length, to_check):
    odd = filter(lambda x: sum(x) != meter_length, to_check)
    return odd

if badly_formeD(8, DEFAULT_NOTE_LENGTH_GROUPINGS):
    raise RuntimeError('''not all note length groupings are well-formed:
            \n{0}\n\nin:{1}'''.format(badly_formeD(8,
                                          DEFAULT_NOTE_LENGTH_GROUPINGS),
                                      DEFAULT_NOTE_LENGTH_GROUPINGS))

if __name__ == "__main__":
    import pprint as pp
    pp.pprint(DEFAULT_NOTE_LENGTH_GROUPINGS)

    ## TEST analyze_grouping
    res = analyze_grouping([1, 2, 1, 3])
    assert res == [1, 1, 0, 1, 1, 0, 0]
    print res
    assert get_grouping((5, (2, 3)), "heavy") ==\
            sum(groupings[(5, (2, 3))]["heavy"], [])
    assert get_grouping(8, "heavy") == sum(groupings[8]["heavy"], [])
    print get_grouping((5, (2, 3)), "terns")
    print get_grouping((9, (3, 3, 3)), "terns")
    print get_grouping((7, (3, 2, 2)), "terns")
    import doctest
    doctest.testmod()
