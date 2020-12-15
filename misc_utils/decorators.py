"""Decoration Utilities."""
import time
from .misc_utils import format_time, to_string, get_time_str, color_print
import warnings


def timer(show_args=True, logger=None):
    """Decorate a function to log how log the function took to execute.

    Args:
        logger: logger to write to, print if None.

    Example:
        >>> from misc_utils import timer
        >>>
        >>> @get_timer(logger)
        >>> def test(a, **kwargs):
        >>>     for i in range(a):
        >>>         time.sleep(1)
        >>>
        >>> test(3, b=2, c=3)
        >>> # [INFO] 2020-01-01 15:30:00 Call ttt(3, b=2, c=3), time: 3s.

    """

    def decorator(fn):
        def measure_time(*args, **kwargs):

            start = time.time()
            result = fn(*args, **kwargs)
            elapsed_time = time.time() - start

            if show_args:
                args_str = to_string(args, last_comma=True) if len(args) and len(kwargs) else to_string(args)
            else:
                args_str = ''

            info = 'Called %s(%s%s), elapsed time: %.5f(s).' % (fn.__name__, args_str, to_string(kwargs), elapsed_time)
            if logger is not None:
                logger.info(info)
            else:
                print('[INFO] %s ' % get_time_str() + info)

            return result

        return measure_time

    return decorator


def deprecated(info=''):
    """Decorate a deprecated function.

    Args:
        info: info to show.

    Example:
        >>> from misc_utils import deprecated
        >>>
        >>> @deprecated('old_func() is deprecated now, use new_func() instead.')
        >>> def old_func():
        >>>     pass
        >>>
        >>> old_func()
        >>> # DeprecationWarning: old_func() is deprecated now, use new_func() instead.

    """
    def decorator(fn):
        def deprecation_info(*args, **kwargs):
            warnings.warn(info, DeprecationWarning)
            color_print('DeprecationWarning: ' + info, 1)
            result = fn(*args, **kwargs)
            return result

        return deprecation_info
    return decorator
