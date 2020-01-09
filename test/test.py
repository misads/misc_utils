import misc_utils as utils
import time

from misc_utils import *
from misc_utils.decorators import get_timer

logger = utils.get_logger()


@get_timer(logger)
def test(a, **kwargs):
    for i in range(a):
        time.sleep(1)


if __name__ == '__main__':

    tests = [
        get_time_stamp(),
        get_time_str(),
        get_time_stamp_by_format_str('2020/01/01 15:30:00'),  # 1577863800

    ]

    utils.p(tests)

    test(3, b=2, c=3)


