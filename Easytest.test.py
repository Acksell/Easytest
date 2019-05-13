import Easytest
import time

class Tester(Easytest.TestSuite):
    def willPassTest(self):
        time.sleep(1)
        1/1
    def willFailTest(self):
        time.sleep(1)
        1/0


if __name__ == "__main__":
    tester=Tester()
    tester.run()