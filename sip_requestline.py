import pdb
import re


class sipRequestline():
    def __init__(self):
        self.ruri = ''
        self.method = ''
        self.sipversion = ''

    def parseRequestLine(self, requestline):
        # As per RFC 3261  7.1
        self.method = requestline.split()[0]
        self.ruri = requestline.split()[1]
        self.sip_version = requestline.split()[2]

    def getRequestline(self):
        msg = f"""
        The given SIP message is a request with:
        request-uri: {self.ruri}
        method: {self.method}"""
        return msg

    def verifyRequestLine(self, to_hdr):
        msg = ''
        # To header can contain tel/sip/sips uri
        uri = to_hdr.value
        pattern = r'(<sip[s]?:[^>]+>|<tel:[^>]+>)'
        match = re.search(pattern, to_hdr.value)
        if match:
            uri = match.group(0)
        else:
            print("Invalid 'To' header format.")

        if self.ruri in uri and self.method != 'REGISTER':
            pass
        else:
            msg = f"""
            The verification of the request failed due to the following reason(s):
            Error: The Request-URI does not contain URI in the To field, as required by "RFC3261 Section 8.1.1.1"
            """
        return msg
