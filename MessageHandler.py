
from collections import deque, OrderedDict
from ColorPrint import ColorPrint

class _MessageHandler:
    def __init__(self):
        # self.errors = deque()
        # self.expectations = deque()
        self.context = None
        # ordered dict because when displaying messages the contexts 
        # should be the same order every time you run the program
        self.contexts = OrderedDict()
        # None is default global context.
        self.contexts[None] = dict()
        self.contexts[None]["errors"] = deque()
        self.contexts[None]["expectations"] = deque()

    def setContext(self, context):
        if context not in self.contexts:
            self.contexts[context] = dict()
            self.contexts[context]["errors"] = deque()
            self.contexts[context]["expectations"] = deque()
        self.context = context

    def setDescription(self, description):
        self.contexts[self.context]["description"] = description

    def queueError(self, error, traceback=None):
        """Adds an appropriate error message to message queue."""
        # get correct queue
        context = self.contexts.get(self.context, None)
        if context:
            context["errors"].append((type(error).__name__, error, traceback))
        else:
            raise KeyError("Could not find context {}".format(self.context))

    def queueExpectation(self, expected, received, phrase=""):
        # get correct queue
        context = self.contexts.get(self.context, None)
        if context:
            context["expectations"].append((expected,received,phrase))            
        else:
            raise KeyError("Could not find context {}".format(self.context))
        
    def popExpectations(self, contextName):
        context = self.contexts.get(contextName, None)
        if context:
            while context["expectations"]:
                expected, received, phrase = context["expectations"].popleft()
                ColorPrint.white("\tExpected {}:".format(phrase))
                ColorPrint.green("\t\t{}".format(repr(expected)))
                ColorPrint.white("\tBut received:")
                ColorPrint.fail("\t\t{}".format(repr(received)))
        else:
            raise KeyError("Could not find context {}".format(contextName))

    def popErrors(self, contextName):
        """Displays all error-messages in queue and pops them."""
        context = self.contexts.get(contextName, None)
        if context:
            while context["errors"]:
                errorType, errorMsg, traceback = context["errors"].popleft()
                # print error type with hard background.
                ColorPrint.fail("\t{}:".format(errorType), end="")
                # print error message with no background.
                ColorPrint.fail(" {}".format(errorMsg))
                for line in traceback:
                    ColorPrint.fail("  {}".format(line))
        else:
            raise KeyError("Could not find context {}".format(contextName))

    def popAll(self):
        for context in self.contexts.keys():
            currContext=self.contexts[context]
            if currContext["expectations"] or currContext["errors"]:
                ColorPrint.white(" In test {}:".format(context))
                if currContext.get("description"):
                    ColorPrint.info("  {}".format(currContext["description"]))
            if currContext["expectations"]:
                ColorPrint.white("  ",end="")
                ColorPrint.fail(" EXPECTATION ",background=True)
                self.popExpectations(context)
            if currContext["errors"]:
                ColorPrint.white("  ",end="")
                ColorPrint.fail(" ERROR ",background=True)
                self.popErrors(context)
