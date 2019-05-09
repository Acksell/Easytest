# Easytest
A small test module inspired by the javascript test
library jest and the python test library unittest.

Easytest provides a lightweight testing API with helpful error 
messages and debugging tools.

It's easiest to show how it works by example:

```Python
from easytest import TestSuite

class TreapTest(TestSuite):
    def beforeEach(self):
        self.treap = Treap()
        self.treap.insert("D")
        self.treap.insert("F")
        self.treap.insert("A")
        self.treap.insert("E")
        self.treap.insert("G")

    def afterEach(self):
        self.treap.healthy()

    def insertTest(self):
        self.treap.insert("B")
        self.expect(self.treap.size()).toEqual(1)
        self.treap.insert("B")
        # does not increment size when not inserting new
        self.expect(self.treap.size()).not.toEqual(2) 
        self.treap.insert("C")
        self.expect(self.treap.size()).toEqual(2)


if __name__ == "__main__":
    TreapTest().run()
```

It's that easy.

You can also easily perform typechecks of complex datastructures:

```Python
from easytest import Expect
# The below passes if object is a *subset* of expected. Useful
# for testing if data is unknown or unimportant. So these pass:
Expect(["A","B",{}]).iterContains([str,str,dict])
Expect([{"a":["B","C"]}]).dictContains([{"a":[str,str,int,list,dict]}])
```

For more documentation, see [Easytest.py](https://gits-15.sys.kth.se/grudat19/axelen-ovn7/blob/master/Easytest.py).
