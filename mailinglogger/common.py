# Copyright (c) 2007-2012 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import re

from cgi import escape
from logging import Formatter
from socket import gethostname


def getErrorInfo(record):
    if "Traceback (" in record.message:
       return record.message.split('\n')[-1]

    msg = record.message.split('\n')[0]
    if len(msg) > 100:
        msg = " ".join(msg.split(' ')[0:10])
    return msg


class SubjectFormatter(Formatter):

    def format(self,record):
        record.message = record.getMessage()
        if self._fmt.find('%(line)') >= 0:
            record.line = record.message.split('\n')[0]
        if self._fmt.find("%(asctime)") >= 0:
            record.asctime = self.formatTime(record, self.datefmt)
        if self._fmt.find("%(hostname)") >= 0:
            record.hostname = gethostname()
        if self._fmt.find("%(short_error_info)") >= 0:
            record.short_error_info = getErrorInfo(record)

        return self._fmt % record.__dict__

class HTMLFilter(object):

    def filter(self, record):
        record.msg = escape(record.getMessage())
        record.args = ()
        return True 

class RegexConversion:

    def __init__(self, regex):
        self._rx = re.compile(regex)

    def __call__(self, value):
        return bool(self._rx.search(value))

def process_ignore(ignore):
    if isinstance(ignore,basestring):
        ignore = [ignore]
    result = []
    for i in ignore:
        if not isinstance(i,RegexConversion):
            i = RegexConversion(i)
        result.append(i)
    return result
