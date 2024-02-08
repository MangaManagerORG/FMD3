import unittest
import sys

sys.path.append('src')


tests_module = f"."
tests = unittest.defaultTestLoader.discover(tests_module)
result = unittest.TextTestRunner().run(tests)
if result.wasSuccessful():
    exit(0)
else:
    exit(1)
