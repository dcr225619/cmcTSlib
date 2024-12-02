import unittest

# import test modules
import test_processor
import test_statssummaries
import test_visualization

# initialize test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite

suite.addTest(loader.loadTestsFromModule(test_processor))
suite.addTest(loader.loadTestsFromModule(test_statssummaries))
suite.addTest(loader.loadTestsFromModule(test_visualization))

# initialize a test runner and run the test suite

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)