class HttpError(Exception):
    def __init__(self, code, message):
        self.code = 400
        self.message = message