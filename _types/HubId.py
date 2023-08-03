from _consts import ROOM_ID_PATTERN


class HubId:
    id: str

    def __init__(self, attempt_id: str):
        if ROOM_ID_PATTERN.fullmatch(attempt_id) is None:
            raise Exception("Doesn't match pattern (5 letters)")
        self.id = attempt_id

    def __str__(self):
        return self.id
