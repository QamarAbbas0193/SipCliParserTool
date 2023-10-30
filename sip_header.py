import pdb
import re


class headerLine():  # Replace with sipheader
    def __init__(self):
        self.headername = ''
        self.value = ''

    def parseHeaderLine(self, headerline):
        self.headername = headerline.split(": ")[0].lower()
        self.value = headerline.split(": ")[1]
        self.value = self.value.replace('\n', '')

    def getHeader(self):
        msg = f"""
            {self.headername}: {self.value}"""
        return msg

    def verifyFromHeader(self):
        msg = ''
        pattern = r'([^<]*\s*)?(<?sips?:[^>]+>?)(;[^>]*)?'
        match = re.search(pattern, self.value)
        display_name = ''
        uri = ''
        parameters = ''

        if match:
            display_name = match.group(1) if match.group(1) else ""
            uri = match.group(2) if match.group(2) else self.value
            parameters = match.group(3) if match.group(3) else ""
        else:
            msg = msg + f"""
            The verification of the request failed due to the following reason(s):
            Error: The From header URI is neither has sip/sips URI as required by "RFC3261 Section 8.1.1.3""
            """

        if "tag=" not in parameters and self.headername == "from":
            msg = msg + f"""
            The verification of the request failed due to the following reason(s):
            Error: The From header should contain from tag as required by "RFC3261 Section 8.1.1.3"
            """
        return msg

    def verifyToHeader(self):
        msg = ''
        pattern = r'([^<]*\s*)?(<?sips?:[^>]+>?|<tel:[^>]+>)(;[^>]*)?'
        match = re.search(pattern, self.value)
        display_name = ''
        uri = ''
        parameters = ''

        if match:
            display_name = match.group(1) if match.group(1) else ""
            uri = match.group(2) if match.group(2) else ""
            parameters = match.group(3) if match.group(3) else ""
        else:
            msg = msg + f"""
            The verification of the request failed due to the following reason(s):
            Error: The To header URI is neither sip/sips not Tel URL 8.1.1.3"
            """

        if "tag=" in parameters:
            msg = msg + f"""
            The verification of the request failed due to the following reason(s):
            Error: The To header should not contain tag outside the dialog as required by "RFC3261 Section 8.1.1.2"
            """
        return msg
