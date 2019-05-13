
"""
A small test module inspired by the javascript test
library jest and the python test library unittest.
"""

from collections import deque

from ColorPrint import ColorPrint 
from Expect import Expect

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
        self.description = ""
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
            self.beforeEach()
            ColorPrint.warn(" RUNS ", end="", background=True)
            ColorPrint.white(" {}".format(test.__name__), end="\r")
            try:
                test()
            except Exception as error:
                ColorPrint.fail(" FAIL ",end="", background=True)
                ColorPrint.white(" {}".format(test.__name__))
                self._messageHandler.queueError(error, testname=test.__name__)
            else:
                ColorPrint.green(" PASS ",end="", background=True)
                ColorPrint.green(" {}".format(test.__name__))
                # self._messageHandler.queueMessage("PASSED: {}".format(test.__name__))
            self.afterEach()
        self._messageHandler.popMessages()

    def expect(self, obj):
        """Returns an Expectation object connected to this test suite"""
        return Expect(obj, self._messageHandler)

    def describe(self, message):
        """
        Adds a descriptive explanation to the currently running test.
        """
        pass

class _MessageHandler:
    def __init__(self):
        self.errors=deque()
        self.messages=deque()

    def queueError(self, error, traceback=None, testname=None):
        """Adds an appropriate error message to message queue."""
        # print(error.value)
        self.errors.append((type(error).__name__, error, testname))

    def queueMessage(self,message):
        """Adds a message to the message queue."""
        self.messages.append(message)

    def popMessages(self):
        """Displays all messages in queue and pops them."""
        # self.messages.popleft() can try this when looping
        for message in self.messages:
            ColorPrint.green(message)
        self.messages.clear()
        for errorType, errorMsg, testname in self.errors:
            # print error type with hard background.
            if testname: 
                ColorPrint.fail(" ERROR ",background=1,end="")
                ColorPrint.white(" In test {}:".format(testname))
            ColorPrint.fail("\t{}:".format(errorType), end="", background=0)
            # print error message with no background.
            ColorPrint.fail(" {}".format(errorMsg), background=0)
        self.errors.clear()

