
import re

from MessageHandler import _MessageHandler
from exceptions import ExpectationFailure
import helpers

class Expect:
    """
    When you're writing tests, you often need to check that values meet
    certain conditions. Expect gives access to a number of methods
    that let you validate different things.

    Each public method represents different expectations of the 
    object's content. If an expectation fails, a neat error message is 
    assured.
    """
    def __init__(self, obj, _messageHandler=None, _negated=False, context=None):
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
        self.context=context
        if context is None:
            self.context = "__main__"
        self.obj = obj
        self._negated = _negated
        self._messageHandler = _messageHandler
        if _messageHandler is None:
            self._messageHandler = _MessageHandler()
        
    @property
    def Not(self):
        """
        A getter for not, returns an identical Expect object but with 
        methods that test for the opposite of normal
        """
        return Expect(self.obj, self._messageHandler, _negated=not self._negated)

    def _fail(self, expected, received, phrase):
        self._messageHandler.queueExpectation(expected, received, phrase)
        # the string passed here is just if calling Expect independently of in a testsuite.
        raise ExpectationFailure("\nExpected {}\n\t{}\nbut received\n\t{}".format(phrase, expected, received))
    
    def _handleExpectation(self, passes, phrase, expected, received):
        if not passes: # throw ExpectationFailurs
            self._fail(expected, received, phrase) 
        return passes

    def toEqual(self, expected):
        """
        Expects any object.
        Passes if the object equals expected object.
        """
        # bitwise XOR creates correct truth table
        passes = (self.obj == expected) ^ self._negated 
        phrase="object to {}equal".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected, self.obj)

    def toBe(self, expected):
        """
        Expects any object.
        Passes if the object is (strictly the same) the expected object.
        """
        # bitwise XOR creates correct truth table
        passes = (self.obj is expected) ^ self._negated 
        phrase="object to {}be strictly equal to".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected, self.obj)

    def toHaveLength(self, length):
        """
        Expects an object implementing __len__.
        Passes if object's length is equal to expected length.
        """
        # bitwise XOR creates correct truth table
        passes = (len(self.obj) == length) ^ self._negated 
        phrase="object to {}have length".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, length, received=len(self.obj))

    def toBeSubset(self, expectedObj):
        """
        Expects an object.
        Passes if `obj` is a subset of the `expected` object.
        Note that lists are sensitive to order, so `[1,2,3]` is
        not a subset of `[2,3,1]`.

        You can pass classes if you don't want to be specific 
        about the value that is allowed. Example: 
          `Expect({"a":4}).toBeSubset({"a":int})` would pass.

        When faced with a list such as `[class]`, a list is a subset
        if all items are an instance of the class. For example, this passes:
          `Expect([1,2,3,4,5]).toBeSubset([int])`
        """
        passes = helpers.issubset(self.obj, expectedObj) ^ self._negated
        phrase="object to {}be a *superset* of".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expectedObj, self.obj)

    def toBeInstanceOf(self, expectedClass):
        """
        Expects any object.
        Passes if object is instance of the expected class.
        """
        passes = (isinstance(self.obj, expectedClass)) ^ self._negated 
        phrase="object to {}be an instance of".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expectedClass, self.obj)

    def toBeGreaterThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than numerical.
        """
        passes = (self.obj > numerical) ^ self._negated 
        phrase="number to {}be greater than".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, numerical, self.obj)

    def toBeLessThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is less than numerical.
        """
        passes = (self.obj < numerical) ^ self._negated 
        phrase="number to {}be less than".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, numerical, self.obj)
    
    def toBeGreaterThanOrEqual(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than or equal to numerical.
        """
        return self.Not.toBeLessThan(numerical)

    def toBeLessThanOrEqual(self, numerical):
        """
        Expects a numerical.
        Passes if object is less than or equal to numerical.
        """
        return self.Not.toBeGreaterThan(numerical)
        
    def toBeNone(self):
        """
        Expects anything.
        Passes if the object is None.
        """
        passes = (self.obj is None) ^ self._negated 
        phrase="object to {}be".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, None, self.obj)

    def toBeTruthy(self):
        """
        Expects anything.
        Passes if the object is truthy.
        """
        passes = (not not self.obj) ^ self._negated
        phrase="object to {}be interpreted as".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected=True, received=self.obj)

    def toBeFalsy(self):
        """
        Expects anything.
        Passes if the object is falsy.
        """
        passes = (not self.obj) ^ self._negated
        phrase="object to {}be interpreted as".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected=False, received=self.obj)        

    def toBeCloseTo(self, number, numDigits=2):
        """
        Expects a numeric type.
        Passes if object is sufficiently close to 
        number when accounting for floating point errors.
        """
        passes = (abs(self.obj - number) < 10**(-numDigits)/2) ^ self._negated
        phrase = "number to {}be accurate up to {} decimals of".format("not " if self._negated else "", numDigits)
        return self._handleExpectation(passes, phrase, number, self.obj)

    def toMatch(self, regex, flags=0):
        """
        Expects a string.
        Passes if the string matches (re.search) the regular expression.
        """
        passes = (not not re.search(regex, self.obj, flags=flags)) ^ self._negated
        phrase="string to {}be matched by the regex".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, regex, self.obj)

    def toBeWithinRange(self, low, high):
        """
        Expects an object compatible with <= and < comparisons.
        Passes if object in interval [low,high).
        """
        passes = (low <= self.obj < high) ^ self._negated
        phrase="string to {}be in the interval".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, 
                    expected="[{}, {})".format(low,high), received=self.obj)

    def toThrow(self, exception=Exception):
        """
        Expects a function taking zero arguments.
        Passes if the function call throws the expected Exception.
        If no specific exception provided, any exception is expected. 
        """
        result=None
        try:
            result = self.obj()
        except Exception as err:
            result=err
            passes = isinstance(err, exception)
        else:
            passes=False
        passes ^= self._negated
        phrase="function {} to {}throw the exception".format(self.obj.__name__, "not " if self._negated else "")
        return self._handleExpectation(passes, phrase, exception, received=result)


    def toThrowWith(self, *args, **kwargs):
        """
        Expects a function.
        Passes if the function throws an Exception with the provided arguments.
        """
        result=None
        try:
            result=self.obj(*args, **kwargs)
        except Exception as err:
            result=err
            passes = True
        else:
            passes=False
        passes ^= self._negated
        phrase="function {} to {}throw an exception".format(self.obj, "not " if self._negated else "")
        return self._handleExpectation(passes, phrase, Exception, received=result)
