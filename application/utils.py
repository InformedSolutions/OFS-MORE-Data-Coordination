import sys
import traceback
import logging


log = logging.getLogger(__name__)


class CronErrorContext:
    """
    Context manager to swallow all exceptions and log them in a concise format instead, for more robust
    and easily-diagnosable cron tasks. Wrap around sections of job that can fail independently, e.g:

        with CronErrorContext():
            data = load_some _data
            for each datum in data:
                with CronErrorContext(logging.WARNING):
                    do_thing_with(datum)
    """
    def __init__(self, log_level=logging.ERROR):
        self.log_level = log_level

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is not None:
            # log brief summary
            log.log(self.log_level, error_short_summary((exc_type, exc_val, exc_tb)))

        # indicate that exceptions should not be propagated
        return True


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
