from re import compile

ROOM_ID_PATTERN = compile(r"^[a-zA-Z]{5}$")
NAME_PATTERN = compile(r"^\w{3,15}$")

ALLOWED_CONNECTION_DETAILS = ["connected", "disconnected"]

PROD_URL = "r-chapy-server"

JWT_LIVE_TIME = 3
