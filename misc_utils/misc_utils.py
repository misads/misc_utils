# encoding=utf-8
"""Misc system & data process utils

Usage:
    >>> import misc_utils as utils
    >>> utils.func_name()  # to call functions in this file
"""
import datetime
import glob
import os
import pdb
import string
import random
import sys
import time

import numpy as np
import logging
import pickle
import json


#############################
#    System utils
#############################

def to_string(obj, last_comma=False):
    """Convert to string in one line.

    Args:
        obj(list, tuple or dict): a list, tuple or dict to convert.
        last_comma(bool): add a comma at last.

    Returns:
        (str) string.

    Example:
        >>> to_string([1, 2, 3, 4], last_comma=True)
        >>> # 1, 2, 3, 4,
        >>> to_string({'a': 2,'b': 4})
        >>> # a=2, b=4

    """
    s = ''
    if type(obj) == list or type(obj) == tuple:
        for i, data in enumerate(obj):
            s += str(data)
            if last_comma or i != len(obj)-1:
                s += ', '

    elif type(obj) == dict:
        for i, data in enumerate(obj.items()):
            k, v = data
            s += '%s=%s' % (str(k), str(v))
            if last_comma or i != len(obj)-1:
                s += ', '
    else:
        s = str(obj)

    return s


def p(obj):
    """Recursively print list, tuple or dict items

    Args:
        obj(list, tuple or dict): a list, tuple or dict to print.

    """
    if type(obj) == list or type(obj) == tuple:
        for i in obj:
            print(i)
    elif type(obj) == dict:
        for k in obj:
            print('%s: %s' % (k, obj[k]))
    else:
        print(obj)


def color_print(text='', color=0, end='\n'):
    """Print colored text.

    Args:
        text(str): text to print.
        color(int):
            * 0       black
            * 1       red
            * 2       green
            * 3       yellow
            * 4       blue
            * 5       cyan (like light red)
            * 6       magenta (like light blue)
            * 7       white
        end(str): end string after colored text.

    Example
        >>> color_print('yellow', 3)

    """
    print('\033[1;3%dm' % color, end='')
    print(text, end='')
    print('\033[0m', end=end)


def print_args(args):
    """Print args parsed by argparse.

    Args:
        args: args parsed by argparse.

    Example
        >>> parser = argparse.ArgumentParser()
        >>> args = parser.parse_args()
        >>> print_args(args)

    """
    print('===========Options===========')
    for k, obj in args._get_kwargs():
        print(' \033[1;32m', str(k).lstrip(), "\033[0m=\033[1;33m", obj, '\033[0m')
    print('=============================')


def get_logger(f='log.txt', mode='w', level='info', print_stream=True):
    """Get a logger.

    Args:

        f(str): log file path.
        mode(str): 'w' or 'a'.
        level(str): 'debug' or 'info'.
        print_stream(bool): if print to terminal or not.

    Returns:
        A logger.

    Example
        >>> logger = get_logger(level='debug')
        >>> logger.info("test")

    """
    logger = logging.getLogger(__name__)
    if level.lower() == 'debug':
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(pathname)s, line %(lineno)d, in %(funcName)s(): '%(message)s'",
            datefmt='%Y-%m-%d %H:%M:%S')
    elif level.lower() == 'info':
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S')

    fh = logging.FileHandler(f, mode=mode)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    if print_stream:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.CRITICAL)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def cmd(shell):
    """Run a shell and return results.

    Args:

    """
    lines = os.popen(shell).readlines()
    return [line.rstrip('\n') for line in lines]


#############################
#        math utils
#############################

def hash(length=8):
    """Return a random hash-like string such as `a6b3c47f`.
    Args:
        length(int): length of hash

    Returns:
        (bool): (randomly) a hash-like string.

    """
    a = '0123456789abcdef'
    res = ''
    for _ in range(length):
        res += a[random.randint(0, 15)]

    return res


def gambling(prob, total=1.0):
    """Return True in a given probability
    Args:
        prob(float): chance to return True.
        total(float): total, default 1.0.

    Returns:
        (bool): (randomly) True or False.

    """
    prob = prob / total
    if random.random() <= prob:
        return True
    else:
        return False


def mean(data: list, prec=3):
    """Calc mean value of a list.

    Args:
        data(list): a list.
        prec(int): round precision.

    Returns:
        (float) mean value.

    Example:
        >>> mean([1, 2, 3, 4])
        >>> # 2.5

    """
    return round(sum(data) / len(data), prec)


#############################
#        safe loads
#############################

def safe_key(dic: dict, key, default=None):
    """Return dict[key] if dict has the key, in case of KeyError.

    Args:
        dic(dict): a dictionary.
        key(usually str or int): key.
        default: default return value.

    Returns:
        dic[key] if key in dic else default.

    """
    if key in dic:
        return dic[key]
    else:
        return default


#############################
#        file system
#############################

def try_make_dir(folder):
    """Make a directory when ignoring FileExistsError.

    Args:
        folder(str): directory path.

    """
    os.makedirs(folder, exist_ok=True)


def get_file_name(path):
    """Get filename by path (without extension).

    Args
        path(str): file's abs path.

    Returns
        filename (without extension).

    Example
        >>> get_file_name('train/0001.jpg')  # 0001

    """
    name, _ = os.path.splitext(os.path.basename(path))
    return name


def get_dir_name(path):
    """Get parent directory name.

    Args
        path(str): file's abs path.

    Returns
        dirname.

    Example
        >>> get_dir_name('root/train/0001.jpg')  # mode/train
        >>> get_dir_name(get_dir_name('root/train/0001.jpg'))  # root

    """
    return os.path.dirname(path)


def get_file_paths_by_pattern(pattern='*', folder=None):
    """Get a file path list matched given pattern.

    Args:
        pattern(str): a pattern to match files.
        folder(str): searching folder.

    Returns
        (list of str): a list of matching paths.

    Examples
        >>> get_file_paths_by_pattern('*.png')  # get all *.png files in folder
        >>> get_file_paths_by_pattern('*rotate*')  # get all files with 'rotate' in name

    """
    if folder is None:
        return glob.glob(pattern)
    else:
        return glob.glob(os.path.join(folder, pattern))


def file_lines(filename, prefix='', offset=0, max_num=0):
    """Load a text file and parse the content as a list of strings.

    Args:
        filename (str): Filename.
        prefix (str): The prefix to be inserted to the begining of each item.
        offset (int): The offset of lines.
        max_num (int): The maximum number of lines to be read,
            zeros and negatives mean no limitation.

    Returns:
        list[str]: A list of strings.
    """
    cnt = 0
    item_list = []
    with open(filename, 'r') as f:
        for _ in range(offset):
            f.readline()
        for line in f:
            if cnt >= max_num > 0:
                break
            item_list.append(prefix + line.rstrip('\n'))
            cnt += 1
    return item_list


def save_pickle(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(file):
    with open(file, 'rb') as f:
        data = pickle.load(f, encoding='bytes')
    return data


def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_time_stamp(add_offset=0):
    """Get time_zone+0 unix time stamp (seconds)

    Args:
        add_offset(int): bias added to time stamp

    Returns:
        (str): time stamp seconds
    """
    ti = int(time.time())
    ti = ti + add_offset
    return str(ti)


def get_time_str(time_stamp=None, fmt="%Y/%m/%d %H:%M:%S", timezone=8, year_length=4):
    """Get formatted time string.
    
    Args:
        time_stamp(str): linux time string (seconds).
        fmt(str): string format.
        timezone(int): time zone.
        year_length(int): 2 or 4.

    Returns:
        (str): formatted time string.

    Example:
        >>> get_time_str()
        >>> # 2020/01/01 13:30:00

    """
    if time_stamp is None:
        time_stamp = get_time_stamp()

    time_stamp = int(time_stamp)

    base_time = datetime.datetime.utcfromtimestamp(time_stamp)

    time_zone_time = base_time + datetime.timedelta(hours=timezone)
    format_time_str = time_zone_time.strftime(fmt)

    if year_length == 2:
        format_time_str = format_time_str[2:]
    return format_time_str


def get_time_stamp_by_format_str(time_str: str, fmt="%Y/%m/%d %H:%M:%S", timezone=8):
    """Get timestamp by formatted time string.

    Args:
        time_str(str): string in fmt format.
        fmt(str): format.
        timezone(int): time zone.

    Returns:
        (str): time stamp

    Example:
        >>> get_time_stamp_by_format_str('2020/01/01 15:30:00')
        >>> # 1577863800

    """
    time_0 = datetime.datetime.utcfromtimestamp(0)

    time_str_parse = datetime.datetime.strptime(time_str, fmt)
    time_str_parse = time_str_parse - datetime.timedelta(hours=timezone)

    days = (time_str_parse - time_0).days
    seconds = (time_str_parse - time_0).seconds
    return str(days * 3600 * 24 + seconds)


def format_time(seconds):
    """Convert seconds to formatted time string.

    Args:
        seconds(int): second number.

    Examples
        >>> format_time(10)  # 10s
        >>> format_time(100)  # 1m
        >>> format_time(10000)  # 2h 47m
        >>> format_time(1000000)  # 11d 13h 47m

    """
    eta_d = seconds // 86400
    eta_h = (seconds % 86400) // 3600
    eta_m = (seconds % 3600) // 60
    eta_s = seconds % 60
    if eta_d:
        eta = '%dd %dh %dm' % (eta_d, eta_h, eta_m)
    elif eta_h:
        eta = '%dh %dm' % (eta_h, eta_m)
    elif eta_m:
        eta = '%dm' % eta_m
    else:
        eta = '%ds' % eta_s
    return eta


def format_num(num: int) -> str:
    """Add comma in every three digits (return a string).

    Args:
        num(int): a number.

    Examples
        >>> format_num(10000)  # 10,000
        >>> format_num(123456789)  # 123,456,789

    """
    num = str(num)
    ans = ''
    for i in range(len(num)-3, -4, -3):
        if i < 0:
            ans = num[0:i+3] + ans
        else:
            ans = ',' + num[i:i+3] + ans

    return ans.lstrip(',')


def split_underline(str, end_num, start_num=0, token='_', keep_ex=True):
    """split a string by token and return a part of it.

    Args:
       str(str): string to handle with.
       end_num(int): end of kept parts.
       start_num(int): start of kept parts.
       token(str): split by which token.
       keep_ex(bool): whether to keep original extension.

    Example:
        >>> split_underline('abc_123_t134567_cam1.jpg', 2)
        >>> # abc_123.jpg

    """
    if keep_ex:
        ex = os.path.splitext(str)[-1]
    else:
        ex = ''

    str = get_file_name(str)
    return token.join(str.split(token)[start_num: end_num]) + ex


def toggle_list_dict(obj):
    """Convert list of dict to dict of list, and vice versa.

    Args:
        obj: a list or a dict.

    Returns:
        converted type of obj.

    Example:
        >>> toggle_list_dict([{'a': 3}, {'a': 5}, {'a': 7}])
        >>> # {'a': [3, 5, 7]}
        >>> toggle_list_dict({'a': [3, 5, 7]})
        >>> # [{'a': 3}, {'a': 5}, {'a': 7}]
        >>> k, v = toggle_list_dict({1: 2, 3: 4})
        >>> # k=[1, 3], v=[2, 4]

    """
    if len(obj) == 0:
        return obj

    if type(obj) == list:
        ans = {}
        if type(obj[0]) == dict:
            l = len(obj)
            keys = obj[0].keys()
            return {k: [obj[i][k] for i in range(l)] for k in keys}
        else:
            for i, data in enumerate(obj):
                ans[i] = data
            return ans

    elif type(obj) == dict:
        first_key = list(obj.keys())[0]
        first_value = obj[first_key]
        if type(first_value) == list:
            l = len(first_value)
            return [{i: obj[i][j] for i in obj.keys()} for j in range(l)]
        else:
            return list(zip(*(obj.items())))

    else:
        return obj


try:
    _, term_width = os.popen('stty size', 'r').read().split()
    term_width = int(term_width)
except:
    term_width = 80


TOTAL_BAR_LENGTH = 30
last_time = time.time()
begin_time = last_time


def progress_bar(current, total, pre_msg=None, msg=None):
    """Render a progress_bar in terminal.

    Preview
        Training...  Step: [=======>... 26/100 ...........] ETA: 0s | loss: 0.45

    Args:

        current(int): current counter, range in [0, total-1].
        total(int): total counts.
        pre_msg(str): message before the progress bar.
        msg(str): message after the progress bar.

    Example
        >>> for i in range(100):
        >>>     progress_bar(i, 100, 'Training...', 'loss:0.45')

    """
    global last_time, begin_time
    if current == 0:
        begin_time = time.time()  # Reset for new bar.


    cur_len = int(TOTAL_BAR_LENGTH*current/total)
    rest_len = int(TOTAL_BAR_LENGTH - cur_len) - 1

    if pre_msg is None:
        pre_msg = ''
    sys.stdout.write(pre_msg + ' Step:')

    sys.stdout.write(' [')
    for i in range(cur_len):
        sys.stdout.write('=')
    sys.stdout.write('>')
    for i in range(rest_len):
        sys.stdout.write('.')
    sys.stdout.write(']')

    cur_time = time.time()
    step_time = cur_time - last_time
    last_time = cur_time
    tot_time = cur_time - begin_time
    if current == 0:
        step_time = 20
    else:
        step_time = (tot_time / current)
    eta_time = int((total - current) * step_time)
    eta = format_time(eta_time)

    L = []
    L.append(' ETA: %s' % eta)
    if msg:
        L.append(' | ' + msg)

    msg = ''.join(L)
    sys.stdout.write(msg)
    for i in range(3):
        sys.stdout.write(' ')
    # for i in range(term_width-int(TOTAL_BAR_LENGTH)-len(msg)-3):
    #     sys.stdout.write(' ')

    # Go back to the center of the bar.
    # for i in range(term_width-int(TOTAL_BAR_LENGTH/2)+2):
    #     sys.stdout.write('\b')
    # sys.stdout.write(' %d/%d ' % (current+1, total))
    for i in range(len(msg) + int(TOTAL_BAR_LENGTH/2)+8):
        sys.stdout.write('\b')
    sys.stdout.write(' %d/%d ' % (current+1, total))

    if current < total-1:
        sys.stdout.write('\r')
    else:
        sys.stdout.write('\n')
    sys.stdout.flush()


def is_file_image(filename):
    """Return if a file's extension is an image's.

    Args:
        filename(str): file path.

    Returns:
        (bool): if the file is image or not.

    """
    img_ex = ['jpg', 'png', 'bmp', 'jpeg', 'tiff']
    if '.' not in filename:
        return False
    s = filename.split('.')

    if s[-1].lower() not in img_ex:
        return False

    if filename.startswith('.'):
        return False

    return True
