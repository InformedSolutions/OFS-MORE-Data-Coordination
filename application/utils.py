import sys
import traceback
import logging


log = logging.getLogger(__name__)


def format_person_name(first, middles, last):
    return first + ((' '+middles) if middles else '') + ' ' + last


def error_short_summary(ex_tuple=None):
    try:
        if ex_tuple is None:
            ex_tuple = sys.exc_info()
        extype, exval, tb = ex_tuple
        frame = traceback.extract_tb(tb)[-1]
        return '{exname}: "{exval}" in "{filename}", "{name}" at line {lineno}'.format(
            exname=extype.__name__, exval=exval, filename=frame.filename, name=frame.name, lineno=frame.lineno)
    except:
        return 'FAILED TO SUMMARISE ERROR'