import Easytest
import time

class Tester(Easytest.TestSuite):
    def passTest(self):
        time.sleep(1)
        1/1

    def failTest(self):
        time.sleep(1)
        1/0

    def passExpectationTest(self):
        self.expect("Epic string").toEqual("Epic string")

    def failExpectationTest(self):
        self.expect("Epic string").Not.toEqual("Epic string")

    def pass2Test(self):pass


if __name__ == "__main__":
    tester=Tester()
    tester.run()