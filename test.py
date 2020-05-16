import misc_utils as utils
import time
import argparse

from misc_utils import *
from misc_utils.decorators import timer

logger = utils.get_logger()


def parse_args():
    # 创建一个parser对象
    parser = argparse.ArgumentParser(description='parser demo')
    parser.add_argument('--tag', default='cache')
    parser.add_argument('--epochs', type=int, default=500)
    opt = parser.parse_args()

    return opt


@timer(logger)
def test(a, **kwargs):
    for i in range(a):
        progress_bar(i, a, msg='hello!')
        time.sleep(.1)


if __name__ == '__main__':

    d = {'a': 1, 'b': 2}

    tests = [
        get_time_stamp(),
        to_string(123),
        get_time_str(year_length=2),
        get_time_stamp_by_format_str('2020/01/01 15:30:00'),  # 1577863800
        safe_key(d, 'c', 0),
        safe_key(d, 'a'),
        try_make_dir('cache'),
        get_file_name('test/1.png'),
        get_dir_name('test/1.png'),
        get_file_paths_by_pattern(folder='misc_utils'),
        format_time(543210),
        format_time(43210),
        format_time(3210),
        format_time(10),
        format_num(9876543210),
        is_file_image('1.png'),
        is_file_image('png'),
        is_file_image('1.txt'),
        toggle_list_dict([1, 3, 5, 7, 9]),
        toggle_list_dict({1: 2, 3: 4}),
        toggle_list_dict({'a': [3, 5, 7], 'b':[1, 3, 4]}),
        toggle_list_dict([{'a': 3, 'b': 1}, {'a': 5, 'b': 2}, {'a': 7, 'b': 3}]),
        mean([1, 2, 3, 4]),
        gambling(0.5),
        hash(12),
        cmd('ls')
    ]



    p(tests)
    p(d)
    p(123)

    opt = parse_args()
    print_args(opt)

    color_print('Yellow', 3)

    test(50, b=2, c=3)



