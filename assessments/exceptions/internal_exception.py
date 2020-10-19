__author__ = "Niloufar MP"


class InternalException(Exception):
    def __init__(self) -> None:
        default_message = 'Something went wrong! Please try again :)'
        super().__init__(default_message)
