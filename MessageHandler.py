
from collections import deque, namedtuple
from ColorPrint import ColorPrint

class _MessageHandler:
    def __init__(self):
        # self.errors = deque()
        # self.expectations = deque()
        self.context = None
        self.contexts=[]
        self.queues = dict()
        self.queues[None] = dict()
        self.queues[None]["errors"] = deque()
        self.queues[None]["expectations"] = deque()

    def setContext(self, context):
        if context not in self.queues:
            self.queues[context] = dict()
            self.queues[context]["errors"] = deque()
            self.queues[context]["expectations"] = deque()
            self.contexts.append(context) # store available contexts
        self.context = context

    def queueError(self, error, traceback=None, context=None):
        """Adds an appropriate error message to message queue."""
        # get correct queue
        queue = self.queues.get(self.context, None)
        if queue:
            queue["errors"].append((type(error).__name__, error, context))
        else:
            raise KeyError("Could not find queue with context {}".format(self.context))

    def queueExpectation(self, expected, received, phrase="",context=None):
        # get correct queue
        queue = self.queues.get(self.context, None)
        if queue:
            queue["expectations"].append((expected,received,phrase,context))            
        else:
            raise KeyError("Could not find queue with context {}".format(self.context))
        
    def popExpectations(self, context):
        queue = self.queues[context]
        while queue["expectations"]:
            expected, received, phrase, context = queue["expectations"].popleft()
            ColorPrint.white("\tExpected {}:".format(phrase))
            ColorPrint.green("\t\t{}".format(expected))
            ColorPrint.white("\tBut received:")
            ColorPrint.fail("\t\t{}".format(received))

    def popErrors(self, context):
        """Displays all error-messages in queue and pops them."""
        queue = self.queues[context]
        while queue["errors"]:
            errorType, errorMsg, context = queue["errors"].popleft()
            # print error type with hard background.
            ColorPrint.fail("\t{}:".format(errorType), end="", background=0)
            # print error message with no background.
            ColorPrint.fail(" {}".format(errorMsg), background=0)

    def popAll(self):
        for context in self.contexts:
            if self.queues[context]["expectations"] or self.queues[context]["errors"]:
                ColorPrint.white(" In test {}:".format(context))
            if self.queues[context]["expectations"]:
                ColorPrint.white("  ",end="")
                ColorPrint.fail(" EXPECTATION ",background=1)
                self.popExpectations(context)
            if self.queues[context]["errors"]:
                ColorPrint.white("  ",end="")
                ColorPrint.fail(" ERROR ",background=1)
                self.popErrors(context)
