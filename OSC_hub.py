
def hub():
    while True:
        data = (yield)
        print "sink: ", data
