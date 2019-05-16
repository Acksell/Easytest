
from MessageHandler import _MessageHandler
from exceptions import ExpectationFailure
import helpers

class Expect:
    """
    When you're writing tests, you often need to check that values meet
    certain conditions. Expect gives access to a number of "matchers"
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
    
    def _handleExpectation(self, passes, phrase, expected, received=None):
        if not passes: # throw ExpectationFailurs
            self._fail(expected, self.obj if received is None else received, phrase) 
        return passes

    def toEqual(self, expected):
        """
        Expects any object.
        Passes if the object equals expected object.
        """
        # bitwise XOR creates correct truth table
        passes = (self.obj == expected) ^ self._negated 
        phrase="object to {}equal".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected)


    def toBe(self, expected):
        """
        Expects any object.
        Passes if the object is (strictly the same) the expected object.
        """
        # bitwise XOR creates correct truth table
        passes = (self.obj is expected) ^ self._negated 
        phrase="object to {}be strictly equal to".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected)

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
        Passes if object is a subset of expected object.
        
        You can pass classes if you don't want to be specific 
        about the value that is allowed.
            Example: expect({"a":4}).dictContains({"a":int}) would pass.
        """
        passes = helpers.issubset(self.obj, expectedObj) ^ self._negated
        phrase="object to {}be a *superset* of".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expectedObj)

    def toBeInstanceOf(self, expectedClass):
        """
        Expects any object.
        Passes if object is instance of the expected class.
        """
        passes = (isinstance(self.obj, expectedClass)) ^ self._negated 
        phrase="object to {}be an instance of".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expectedClass)

    def toBeGreaterThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is greater than numerical.
        """
        passes = (self.obj > numerical) ^ self._negated 
        phrase="number to {}be greater than".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, numerical)

    def toBeLessThan(self, numerical):
        """
        Expects a numerical.
        Passes if object is less than numerical.
        """
        passes = (self.obj < numerical) ^ self._negated 
        phrase="number to {}be less than".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, numerical)
    
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
        return self._handleExpectation(passes, phrase, None)

    def toBeTruthy(self):
        """
        Expects anything.
        Passes if the object is truthy.
        """
        passes = self.obj if not self._negated else not self.obj
        phrase="object to {}be interpreted as".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected=True)

    def toBeFalsy(self):
        """
        Expects anything.
        Passes if the object is falsy.
        """
        passes = self.obj if self._negated else not self.obj
        phrase="object to {}be interpreted as".format("not " if self._negated else "")
        return self._handleExpectation(passes, phrase, expected=False)        

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

    def toThrow(self, exception=Exception):
        """
        Expects a function taking zero arguments.
        Passes if the function call throws the expected Exception.
        If no specific exception provided, any exception is expected. 
        """
        pass

    def toThrowWith(self, *args, **kwargs):
        """
        Expects a function.
        Passes if the function throws an error with the provided arguments to .toThrowWith.
        """
        pass
