import sys
import traceback
import logging


log = logging.getLogger(__name__)

class CronErrorContext:
    """
    Context manager to log exceptions in a concise format and recover
    from exceptions from sub-sections, for more robust and
    easily-diagnosable cron tasks.

    Wrap job with new instance and use the 'sub' method to define sections
    of the job that can fail independently. e.g:

        # errors at this level are logged as ERROR by default and re-raised
        with CronErrorContext() as error_context:
            data = load_some_data()
            for each datum in data:
                # errors at this level will be logged at the specified
                # level and collected util leaving the top level context
                with error_context.sub(logging.WARNING):
                    do_thing_with(datum)
    """

    class ErrorsEncounteredException(Exception):
        pass

    def __init__(self, log_level=logging.ERROR):
        self.log_level = log_level
        self._root = self
        self._suberrors = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if any((exc_type, exc_val, exc_tb)):
            # log brief summary
            log.log(self.log_level, error_short_summary((exc_type, exc_val, exc_tb)))
            # noinspection PyProtectedMember
            self._root._suberrors += 1

        if self._root is self and self._suberrors > 0:
            try:
                raise self.ErrorsEncounteredException(
                    '{} errors encountered during this cron task. See log for details'.format(self._suberrors))
            except:
                log.log(self.log_level, error_short_summary())
                raise

        # Indicate that we've handled the exception ourselves
        return True

    def sub(self, log_level=logging.ERROR):
        subcontext = CronErrorContext(log_level)
        subcontext._root = self._root
        return subcontext


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

