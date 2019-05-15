

def issubset(received, expected):
    # The expected is just a class,
    # so check if instance of class.
    if isinstance(expected, type):
        return isinstance(received, expected)
    elif isinstance(received, dict): # check subset for dict
        passed = True
        for key in received:
            if key in expected:
                # traverse deeper.
                passed = issubset(received[key], expected[key]) and passed
            else: 
                return False
        return passed # all keys returned true
    elif isinstance(received, list): # check subset for list
        if expected:
            if isinstance(expected[0], type): # is a list of class. e.g. [int]
                #check that all items are instances of that class.
                return all(map(lambda item: isinstance(item, expected[0]), received))
            else:
                if len(received) > expected: return false
                passed = True
                for i,item in enumerate(received):
                    passed = issubset(item, expected[i]) and passed
                    if not passed: break
                return passed
        else:
            return len(received) == 0
    else: 
         # not instance of class, so it's a leaf, just check equality.
        return received == expected
