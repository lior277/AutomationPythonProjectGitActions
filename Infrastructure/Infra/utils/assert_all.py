class AssertAll:
    def __init__(self, assertions: list):
        self.assertions = assertions
        self.assertion_errors = []

    def run(self):
        for assertion in self.assertions:
            try:
                assertion()
            except AssertionError as e:
                self.assertion_errors.append(str(e))

        if self.assertion_errors:
            raise AssertionError("\n".join(self.assertion_errors))
