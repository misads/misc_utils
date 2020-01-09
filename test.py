import misc_utils as utils
import time
import argparse

from misc_utils import *
from misc_utils.decorators import get_timer

logger = utils.get_logger()


def parse_args():
    # 创建一个parser对象
    parser = argparse.ArgumentParser(description='parser demo')
    parser.add_argument('--tag', default='cache')
    parser.add_argument('--epochs', type=int, default=500)
    opt = parser.parse_args()

    return opt


@get_timer(logger)
def test(a, **kwargs):
    for i in range(a):
        progress_bar(i, a)
        time.sleep(.1)


if __name__ == '__main__':

    d = {'a': 1, 'b': 2}

    tests = [
        get_time_stamp(),
        get_time_str(),
        get_time_stamp_by_format_str('2020/01/01 15:30:00'),  # 1577863800
        safe_key(d, 'c', 0),
        try_make_dir('cache'),
        get_file_name('test/1.png'),
        get_dir_name('test/1.png'),
        get_file_paths_by_pattern(folder='misc_utils'),
        format_time(543210),
        format_num(9876543210),
        is_file_image('1.png'),
    ]

    utils.p(tests)

    opt = parse_args()
    print_args(opt)

    test(50, b=2, c=3)


