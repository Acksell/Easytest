
"""
A small test module inspired by the javascript test
library jest and the python test library unittest.
"""

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
        self.messageHandler = _MessageHandler()

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

    def expect(self, obj):
        """Returns an Expectation object connected to this test suite"""
        return Expect(obj, self.messageHandler)

class Expect:
    """
    When you're writing tests, you often need to check that values meet
    certain conditions. Expect gives access to a number of "matchers"
    that let you validate different things.

    Each public method represents different expectations of the 
    object's content. If an expectation fails, a neat error message is 
    assured.
    """
    def __init__(self, obj, messageHandler=None, _negated=False):
        """Params:
            - object: the object to be inspected.
            - messageHandler: the MessageHandler to use.
            - _negated: if True, all methods test for the opposite of normal.
        Attributes:
            obj: the object to be inspected.
            messageHandler: the MessageHandler to use.
            not: an identical Expect object but with 
                 methods that test for the opposite of normal
            _negated: if True, all methods test for the opposite of normal.
        """
        pass

    @property
    def not(self):
        """
        A getter for not, returns an identical Expect object but with 
        methods that test for the opposite of normal
        """
        return Expect(self.obj, self.messageHandler, _negated=True)
    
    def toEqual(self, expected):
        """
        Expects any object.
        Passes if the object equals expected object.
        """
        pass

    def toBe(self, expected):
        """
        Expects any object.
        Passes if the object is (strictly the same) the expected object.
        """

    def toHaveLength(self, length):
        """
        Expects an object implementing __len__.
        Passes if object's length is equal to expected length.
        """
        pass

    def dictContains(self, expectedDict):
        """
        Expects a dictionary.
        Passes if dictionary is a subset of expected dictionary.
        
        You can pass classes if you don't want to be specific 
        about the value that is allowed.
            Example: expect({"a":4}).dictContains({"a":int}) would pass.
        """
        pass

    def iterContains(self, expectedIter)
        """
        Expects an iterable.
        Passes if iterable is a subset of the expected iterable.

        You can pass classes if you don't want to be specific 
        about the value that is allowed.
            Example: expect(["This is","a list"]).iterContains([str,str,str]) would pass.
        """
        pass

    def toBeInstanceOf(self, expectedClass):
        """
        Expects any object.
        Passes if object is instance of the expected class.
        """
        pass

    def toBeGreaterThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than numerical.
        """
        pass

    def toBeGreaterThanOrEqual(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than or equal to numerical.
        """
        pass

    def toBeLessThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is less than numerical.
        """
        pass

    def toBeLessThanOrEqual(self, numerical):
        """
        Expects a numerical.
        Passes if object is less than or equal to numerical.
        """
        pass

    def toBe(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than numerical.
        """
        pass

    def toBeNone(self, anyobject):
        """
        Expects anything.
        Passes if the object is not None.
        """
        pass

    def toBeTruthy(self, obj):
        """
        Expects anything.
        Passes if the object is truthy.
        """
        pass

    def toBeFalsy(self, obj):
        """
        Expects anything.
        Passes if the object is falsy.
        """
        pass
        

    def toBeCloseTo(self, number):
        """
        Expects a numeric type.
        Passes if object is sufficiently close to 
        number when accounting for floating point errors.
        """
        pass

    def toMatch(self, regex):
        """
        Expects a string.
        Passes if the string matches the regular expression.
        """
        pass

    def toBeWithinRange(self, low, high):
        """
        Expects an object compatible with < and <= comparisons.
        Passes if object between low and high.
        """
        pass

class _MessageHandler:
    def __init__(self):
        self.errors=[]
        self.messages=[]

    def queueError(message,traceback):
        """Adds an appropriate error message to message queue."""
        pass

    def queueMessage(message):
        """Adds a message to the message queue."""
        pass

    def popMessages(self):
        """Displays all messages in queue and pops them."""
        pass

