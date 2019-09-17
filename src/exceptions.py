class StrepError(Exception):
    pass


class UnknownCommandError(StrepError):

    def __init__(self, cmd):
        self.message = f"Unknown command {cmd}"

    def __str__(self):
        return self.message

class FailedCommandError(StrepError):

    def __init__(self, cmd):
        self.message = f"Failed to {cmd}"

    def __str__(self):
        return self.message
