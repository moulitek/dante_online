SEGFAULT = 1
BADOUTPUT = 2
RETVALUE = 3
TIMEOUT = 4
NEVER_RUN = 5

moulitek_all_categories = []

class Category:
    def __init__(self, name, desc=None, info = False):
        """Init a category

        `name` The name of the category

        `desc` (optional) A description of the category
        """
        self.name = name
        self.desc = desc
        self.info = info
        self.sequences = []
        moulitek_all_categories.append(self)

    def add_sequence(self, name, desc=None):
        """Add sequence to category

        `name` The name of the sequence

        `desc` (optional) A description of the sequence
        """
        sequence = Sequence(self, name, desc)
        self.sequences.append(sequence)
        return sequence


class Sequence:
    def __init__(self, category: Category, name: str, desc : str = None):
        self.name = name
        self.desc = desc
        self.category = category
        self.tests = []

    def test_exist(self, name: str):
        """Check if test exists

        `name` The name of the test
        """
        for i, test in enumerate(self.tests):
            if test["name"] == name:
                return i
        return -1

    def add_test(self, name: str, desc: str = None):
        """Add a test to the Sequence

        `name` The name of the test

        `desc` (optional) A description of the test
        """
        if self.test_exist(name) != -1:
            return False
        test = {"name": name, "desc": desc, "passed": False,
                "reason": NEVER_RUN, "expected": None, "got": None}
        self.tests.append(test)
        return True

    def set_status(self, name, passed: bool = True, reason: int = 0, expected: str = None, got: str = None):
        """Set status of a test

        `name` The name of the test

        `passed` Test status

        - If passed is False :

            `reason` SEGFAULT | BADOUTPUT | RETVALUE | TIMEOUT

            `expected`: Expected result

            `got`: Expected result
        """
        existing_test = self.test_exist(name)
        if existing_test == -1:
            return False
        if not passed and (reason == 0 or expected == None or got == None):
            return False
        self.tests[existing_test]["passed"] = passed
        self.tests[existing_test]["reason"] = reason
        self.tests[existing_test]["expected"] = expected
        self.tests[existing_test]["got"] = got
        return True
