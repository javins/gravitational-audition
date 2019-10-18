from unittest import TestLoader, TextTestRunner
import grav.test


def main():
    """
    The primary entrypoint for this project, and one that can be used in the
    `console_scripts` directive in setup.py.
    """
    tests = TestLoader().loadTestsFromModule(grav.test)
    # verbosity 2 is enough to show all tests, per:
    # https://github.com/python/cpython/blob/ecb035cd14c11521276343397151929a94018a22/Lib/unittest/runner.py#L40
    # more doesn't seem to do anything -- wdella 2019-10
    result = TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit(1)


if __name__ == "__main__":
    main()
