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

    def passNotTest(self):
        self.expect("test").Not.Not.toEqual("test")
        self.expect("test").Not.Not.Not.toEqual("lol")

    def passLengthTest(self):
        self.expect([1,2,3,"4"]).toHaveLength(4)

    def failLengthTest(self):
        self.expect([1,2,3,"4"]).toHaveLength(3)

    def passSubsetTest(self):
        self.expect(["test"]).toBeSubset([str])
        self.expect({"test":3}).toBeSubset({"test":int})
        self.expect({"test":[4,5,1,2,2]}).toBeSubset({"test":[int]})
        self.expect({"test":[1,2,3,4,5]}).toBeSubset({"test":[1,2,3,4,5,6,7,8]})
        self.expect([{}]).toBeSubset([dict])
        result = self.expect({
            "a": {
                "b": {"c":[3,2,1]},
                "d": "string"
                }
        })
        result.toBeSubset({
            "a": {
                "b": dict,
                "d":str,
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

    def failSubset4Test(self):
        self.expect([2,3,4,5]).toBeSubset([2,3,4])

    def failSubset5Test(self):
        # order matters
        self.expect([1,2,3,4,5]).toBeSubset([2,3,4,1,5])

    def passInstanceOfTest(self):
        self.expect(2).toBeInstanceOf(int)
        self.expect("2").toBeInstanceOf(str)
        self.expect(dict).Not.toBeInstanceOf(dict)
        self.expect(set()).toBeInstanceOf(set)

    def failInstanceOfTest(self):
        self.expect(dict).toBeInstanceOf(dict)

    def passGreaterThanTest(self):
        self.expect(3).toBeGreaterThan(2)
        self.expect(3.0).Not.toBeGreaterThan(3.0)
    
    def passGreaterThanOrEqualTest(self):
        self.expect(3).toBeGreaterThanOrEqual(2)
        self.expect(3.0).toBeGreaterThanOrEqual(3.0)
    
    def passLessThanTest(self):
        self.expect(2).toBeLessThan(3)
        self.expect(3.0).Not.toBeLessThan(3.0)
    
    def passLessThanOrEqualTest(self):
        self.expect(2).toBeLessThanOrEqual(3)
        self.expect(3.0).toBeLessThanOrEqual(3.0)
    
    def passNoneTest(self):
        self.expect(None).toBeNone()
        self.expect("not none").Not.toBeNone()

    def failNoneTest(self):
        self.expect(False).toBeNone()
    
    def passTruthyTest(self):
        self.expect("notempty").toBeTruthy()
        self.expect([0]).toBeTruthy()
    
    def failTruthyTest(self):
        self.expect("").toBeTruthy()

    def passFalsyTest(self):
        self.expect("").toBeFalsy()
        self.expect([]).toBeFalsy()
    
    def failFalsyTest(self):
        self.expect("notempty").toBeFalsy()

    def passRegexTest(self):
        inner='.*'.join("progp")
        regex=r'^(.*{}.*)$'.format(inner)
        self.expect("programmeringsparadigm").toMatch(regex)
        self.expect("ducksgoquack").Not.toMatch(regex)

if __name__ == "__main__":
    tester=Tester()
    tester.run()
    
    assert tester._status["passTest"] == "passed"
    assert tester._status["passEmptyTest"] == "passed"
    assert tester._status["failTest"] == "failed"
    assert tester._status["passToEqualTest"] == "passed"
    assert tester._status["failNotToEqualTest"] == "failed"
    assert tester._status["passNotTest"] == "passed"
    assert tester._status["passLengthTest"] == "passed"
    assert tester._status["passSubsetTest"] == "passed"
    assert tester._status["failSubset1Test"] == "failed"
    assert tester._status["failSubset2Test"] == "failed"
    assert tester._status["failSubset3Test"] == "failed"
    assert tester._status["failSubset4Test"] == "failed"
    assert tester._status["failSubset5Test"] == "failed"
    assert tester._status["passInstanceOfTest"] == "passed"
    assert tester._status["failInstanceOfTest"] == "failed"
    assert tester._status["passGreaterThanTest"] == "passed"
    assert tester._status["passGreaterThanOrEqualTest"] == "passed"
    assert tester._status["passLessThanTest"] == "passed"
    assert tester._status["passLessThanOrEqualTest"] == "passed"
    assert tester._status["passNoneTest"] == "passed"
    assert tester._status["failNoneTest"] == "failed"
    assert tester._status["passTruthyTest"] == "passed"
    assert tester._status["failTruthyTest"] == "failed"
    assert tester._status["failFalsyTest"] == "failed"
    assert tester._status["passRegexTest"] == "passed"
    # assert tester._status["passInstanceOf"] == "passed"
    
    