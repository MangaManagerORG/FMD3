import unittest
import sys

sys.path.append('src')

if __name__ == '__main__':
    tests_module = f"./.github/workflows/workflow_helpers_tests/tests/"
    tests = unittest.defaultTestLoader.discover(tests_module)
    result = unittest.TextTestRunner().run(tests)
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)

    m