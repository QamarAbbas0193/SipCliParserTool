class BodyLine():
    def __init__(self):
        self.line = ''

    def setBodyLine(self, line):
        self.line = line.replace('\n', '')

    def getBodyLine(self):
        msg = f"""
            {self.line}"""
        return msg
