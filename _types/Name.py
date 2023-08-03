from _consts import NAME_PATTERN


class Name:
    name: str

    def __init__(self, attempt: str):
        if NAME_PATTERN.fullmatch(attempt) is None:
            raise Exception("Doesn't match pattern (3-15 word characters)")
        self.name = attempt

    def __str__(self):
        return self.name
