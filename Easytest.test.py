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

    def passSubsetTest(self):
        self.expect(["test"]).toBeSubset([str])
        self.expect({"test":3}).toBeSubset({"test":int})
        self.expect({"test":[4,5,1,2,2]}).toBeSubset({"test":[int]})
        self.expect({"test":[1,2,3,4,5]}).toBeSubset({"test":[1,2,3,4,5,6,7,8]})
        result = self.expect({
            "a": {
                "b": {"c":[3,2,1]},
                "d": "string"
                }
        })
        result.toBeSubset({
            "a": {
                "b": dict,
                "d":"string",
                "not in received": 42
            }
        })
        result.toBeSubset({
            "a": {
                "b": {"c": list},
                "d":"string",
                "not in received": 42
            }
        })


    def failSubset1Test(self):
        self.expect({"test":3}).toBeSubset({"test":4})

    def failSubset2Test(self):
        self.expect({"test":[4,5,1,2,2,"9"]}).toBeSubset({"test":[int]})

    def failSubset3Test(self):
        self.expect(["not empty"]).toBeSubset([])

if __name__ == "__main__":
    tester=Tester()
    tester.run()
    
    assert tester._status["passTest"] == "passed"
    assert tester._status["passEmptyTest"] == "passed"
    assert tester._status["failTest"] == "failed"
    assert tester._status["passToEqualTest"] == "passed"
    assert tester._status["failNotToEqualTest"] == "failed"
    assert tester._status["passLengthTest"] == "passed"
    assert tester._status["passSubsetTest"] == "passed"
    assert tester._status["failSubset1Test"] == "failed"
    assert tester._status["failSubset2Test"] == "failed"
    assert tester._status["failSubset3Test"] == "failed"
    # assert tester._status["passTest"] == pass
    
    