

from voice import Voice
from composer import Composer
from OSC_hub import hub


def startup():
    s = hub()
    s.next() # get the coroutine to the yield
    c = Composer()
    v1 = Voice(1, s, c)
    v2 = Voice(2, s, c)
    v3 = Voice(3, s, c)
    return c

def main(c):
    c.send_state({"possible":[2,6,9],
                  "composer":c})
    c.report()

if __name__ == "__main__":
    composer = startup()
    main(composer)
