"""Decoration Utilities."""
import time
from .misc_utils import to_string, get_time_str, color_print, preview
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
                args_str += to_string(kwargs)

                if '\n' in args_str or len(args_str) > 20:
                    # 参数过长
                    args_str = 'args too long'
                    info = 'Called %s(%s), elapsed time: %.5f(s).' % (fn.__name__, args_str , elapsed_time)
                    if logger is not None:
                        logger.info(info)
                    else:
                        print('[INFO] %s ' % get_time_str() + f'Called {fn.__name__}(')
                        color_print('args:', 2)
                        preview(args, 1)
                        color_print('keyword args:', 2)
                        preview(kwargs, 1)
                        print(f') elapsed time: {elapsed_time:.5f}(s).')       

                    return result

            else:
                args_str = ''

            info = 'Called %s(%s), elapsed time: %.5f(s).' % (fn.__name__, args_str , elapsed_time)
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
