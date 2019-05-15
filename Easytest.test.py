import Easytest
import time

class Tester(Easytest.TestSuite):
    def passTest(self):
        time.sleep(1)
        1/1

    def failTest(self):
        time.sleep(1)
        1/0

    def passEmptyTest(self):pass

    def passToEqualTest(self):
        self.expect("Epic string").toEqual("Epic string")

    def failNotToEqualTest(self):
        self.expect("Epic string").Not.toEqual("Epic string")

    def passLengthTest(self):
        self.expect([1,2,3,"4"]).toHaveLength(4)

    def failLengthTest(self):
        self.expect([1,2,3,"4"]).toHaveLength(3)

    def failNotLengthTest(self):
        self.expect([1,2,3,"4"]).Not.toHaveLength(4)

if __name__ == "__main__":
    tester=Tester()
    tester.run()
    
    assert tester._status["passTest"] == "passed"
    assert tester._status["passEmptyTest"] == "passed"
    assert tester._status["failTest"] == "failed"
    assert tester._status["passToEqualTest"] == "passed"
    assert tester._status["failNotToEqualTest"] == "failed"
    assert tester._status["passLengthTest"] == "passed"
    assert tester._status["failNotLengthTest"] == "failed"
    # assert tester._status["passTest"] == pass
    # assert tester._status["passTest"] == pass
    # assert tester._status["passTest"] == pass
    # assert tester._status["passTest"] == pass
    
    