
"""
A small test module inspired by the javascript test
library jest and the python test library unittest.
"""

from collections import deque
import sys, traceback

from ColorPrint import ColorPrint 
from Expect import Expect
from MessageHandler import _MessageHandler

from exceptions import ExpectationFailure

class TestSuite:
    """
    Class for running test suites with setup and teardown.
    Test methods should end with "Test".
    """
    def __init__(self):
        # get test methods to run (modified from StackOverflow)
        # https://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class
        testnames = [func for func in dir(self) if callable(getattr(self, func)) and func.endswith("Test")]
        self._tests = [getattr(self, test) for test in testnames]
        self._messageHandler = _MessageHandler()
        self._status = dict()  # in case anyone wants this.
        self._currently_running=None

    def beforeEach(self):
        """This function runs before each testcase. Feel free to override."""
        pass

    def afterEach(self):
        """This function runs after each testcase. Feel free to override."""
        pass

    def run(self):
        """
        Runs all tests, that is, all class methods whose names ends with "Test".
        If any test fails, continue to run other tests. Displays helpful information
        while running the tests and reports whether a test failed or succeeded.
        If a test fails, a helpful error message is displayed.
        """
        # can try: except: here to catch errors and display more verbose error messages.

        for test in self._tests:
            self._currently_running = test.__name__
            self._messageHandler.setContext(self._currently_running)

            ColorPrint.warn(" RUNS ", end="", background=True)
            ColorPrint.white(" {}".format(self._currently_running), end="\r")
            
            self.beforeEach()
            try:
                test()
            except Exception as error:
                # ExpectationFailure is raised because Expect doesn't know if
                # it is running in a testsuite.
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tracebackFormatted = traceback.format_tb(exc_traceback)
                if not isinstance(error, ExpectationFailure):
                    self._messageHandler.queueError(error, tracebackFormatted)

                ColorPrint.fail(" FAIL ",end="", background=True)
                ColorPrint.white(" {}".format(self._currently_running))
                self._status[test.__name__] = "failed"
            else:
                ColorPrint.green(" PASS ",end="", background=True)
                ColorPrint.green(" {}".format(self._currently_running))
                self._status[test.__name__] = "passed"
            self.afterEach()
        self._messageHandler.popAll()

    def expect(self, obj):
        """Returns an Expectation object connected to this test suite"""
        return Expect(obj, self._messageHandler, context=self._currently_running)

    def it(self, message):
        """
        Adds a descriptive explanation to the currently running test.
        Example: self.it("should return False for empty case")
        """
        capitalizedMessage="{}{}".format(message[0].upper(), message[1:])
        self._messageHandler.setDescription(capitalizedMessage)
