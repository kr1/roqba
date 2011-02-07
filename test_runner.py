"""this script orchestrates the tests contained in the tests folder"""
import sys
import unittest2 as unittest
import tests.unit_test_composer as u_t_composer

if __name__ == "__main__":
    uniT, functionaL = False, False
    print "script called with %r arguments" % sys.argv
    la = len(sys.argv)
    if  la == 1:
        uniT, functionaL = True, True
    elif la > 1:
        what = sys.argv[1]
        if what == "unit":
            uniT = True
        elif what == "integration":
            functionaL = True
        else:
            print "Usage:\ncall the script with 'unit' XOR 'integration' \
                     arguments to run only the specified test-suite."
            print "calling it without arguments will result in running \
                     all tests."
    if functionaL:
        print "starting functional tests...\n-----------------------------"
        #unittest.TextTestRunner(verbosity=2).run(f_t_voice.suite())
    if uniT:
        print "starting unit tests...\n---------------------------"
        unittest.TextTestRunner(verbosity=2).run(u_t_composer.suite())
