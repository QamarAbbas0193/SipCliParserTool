from sip_requestline import sipRequestline
from sip_header import headerLine
from sip_bodyline import BodyLine
import pdb

MANDATORY_HEADERS = ("to", "from", "cseq", "call-id", "max-forwards", "via")


class sipMessage():
    def __init__(self):
        self.msg_content = ''
        self.msg_lines = []
        self.headerslst = []
        self.bodylist = []
        self.requestline = sipRequestline()

    def __str__(self) -> str:
        return self.msg_content

    def setContent(self, filepath) -> None:
        file = open(filepath, "r")
        filecontent = file.read()
        file.seek(0)
        msglines = file.readlines()
        file.close()
        self.msg_content = filecontent
        self.msg_lines = msglines

    def setRequestLine(self):
        self.requestline.parseRequestLine(self.msg_lines[0])

    def setHeaderLines(self):
        for idx in range(len(self.msg_lines)):
            if self.msg_lines[idx] == '\n':
                break
            if idx > 0:
                hdr = headerLine()
                hdr.parseHeaderLine(self.msg_lines[idx])
                self.headerslst.append(hdr)

    def setBodyLines(self):
        for idx in range(len(self.msg_lines)):
            if self.msg_lines[idx] == '\n':
                break

        for bline in self.msg_lines[idx+1:]:
            bl = BodyLine()
            bl.setBodyLine(bline)
            self.bodylist.append(bl)

    def validateRequestLine(self):
        to_hdr = [hdr for hdr in self.headerslst if hdr.headername == "to"][0]
        msg = self.requestline.verifyRequestLine(to_hdr)
        return msg

    def validateFromHeader(self):
        from_hdr = [
            hdr for hdr in self.headerslst if hdr.headername == "from"][0]
        msg = from_hdr.verifyFromHeader()
        return msg

    def validateToHeader(self):
        to_hdr = [hdr for hdr in self.headerslst if hdr.headername == "to"][0]
        msg = to_hdr.verifyToHeader()
        return msg

    def validateMandatoryHeaders(self):
        msg_mandatory_hdr = []
        msg_mandatory_hdr = [hdr.headername for hdr in self.headerslst
                            if hdr.headername in MANDATORY_HEADERS]
        msg_mandatory_hdr_set = set(msg_mandatory_hdr)
        mandatory_hdr_set = set(MANDATORY_HEADERS)
        diff_hdr_set = mandatory_hdr_set.difference(msg_mandatory_hdr_set)

        hdrnames = ", ".join(diff_hdr_set)
        msg = ''
        if (diff_hdr_set):
            msg = f"""
            The verification of the request failed due to the following reason(s):
            Error: The "{hdrnames}" header is missing, as required by "RFC3261 Section 8.1.1"
            """
        return msg

    def isHeaderExists(self, hdr_name):
        hdrtoverify = [
            hdr for hdr in self.headerslst if hdr.headername == hdr_name]
        msg = ''
        if hdrtoverify:
            msg = msg + f"""
            The given SIP message has a {hdr_name} header:"""
            msg = msg + hdrtoverify[0].getHeader()
            msg = msg + """
            """
        else:
            msg = msg + f"""
            Info: The given SIP message has no {hdr_name} header:
            """
        return msg

    def getFormattedMsg(self):
        msg = self.requestline.getRequestline()
        msg = msg + """
        header:"""
        for hdr in self.headerslst:
            msg = msg + hdr.getHeader()

        msg = msg + """
        and body:"""
        # pdb.set_trace()
        for line in self.bodylist:
            msg = msg + line.getBodyLine()

        return msg
