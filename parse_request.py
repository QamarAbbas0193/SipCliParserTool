import sys
import os
import argparse
import pdb
from sip_message import sipMessage

DIRPATH = os.path.split(__file__)[0]


class clirequestParser():
    def __init__(self):
        self.filepath = ''
        self.msg = ''

    def parseArguments(self):
        parser = argparse.ArgumentParser(description="CLI to parse a \
        SIP Message from a Text file")
        parser.add_argument('-v', "--validate", nargs=1, metavar='\b',
                            help="the request should be checked for \
                            compliance with the RFC3261 Sections \
                                8.1.1, 8.1.1.1, 8.1.1.2 and 8.1.1.3")
        parser.add_argument('-p', "--print", nargs=1, metavar='\b', help="the\
                             sip message is parsed from file and printed in a\
                             format")
        parser.add_argument('-e', "--exists", nargs=2, metavar='\b', help="\
                            the sip header is checked in a file")
        args = parser.parse_args()

        if args.validate is None and args.print is None and args.exists is None:
            parser.error('One of option is mandatory, Use --help option  ..')

        fpath = ''
        if args.validate:
            fpath = args.validate[0]
        if args.print:
            fpath = args.print[0]
        if args.exists:
            fpath = args.exists[-1]

        # pdb.set_trace()
        self.filepath = os.path.join(str(DIRPATH), fpath)
        self.args = args

    def performAction(self):
        sipmsg = sipMessage()
        sipmsg.setContent(self.filepath)
        sipmsg.setRequestLine()
        sipmsg.setHeaderLines()
        sipmsg.setBodyLines()

        if self.args.print:
            fmsg = sipmsg.getFormattedMsg()
            self.msg = fmsg
        elif self.args.exists:
            hdr_name = self.args.exists[0].lower()
            self.msg = sipmsg.isHeaderExists(hdr_name)
        elif self.args.validate:
            rline_out = sipmsg.validateRequestLine()
            from_hdr_out = sipmsg.validateFromHeader()
            to_hdr_out= sipmsg.validateToHeader()
            mandatoryhdr_out = sipmsg.validateMandatoryHeaders()
            self.msg = \
            f"{rline_out}{from_hdr_out}{to_hdr_out}{mandatoryhdr_out}"

            if (self.msg == ''):
                self.msg = """
                The request has been verified and no issues were found.
                """

    def displayResults(self):
        print(self.msg)


if __name__ == "__main__":
    cmd = clirequestParser()
    cmd.parseArguments()
    cmd.performAction()
    cmd.displayResults()
