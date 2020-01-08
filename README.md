# misc_utils

<p>
    <a href='https://torch-template.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/torch-template/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
</p>

Misc system & data process utils for Python. 


### Installation

**For pip**  

```bash
pip install misc-utils
```

**For source**

Clone the repo, cd into it and run `pip install .` command.

```bash
git clone https://github.com/misads/misc_utils.git
cd misc_utils
pip install .
```

**For conda**

```bash
source ~/anaconda3/bin/activate
conda activate <env>
python setup.py install
```

A configure file `misc_utils.egg-info` will be generated in the repo directory. Copy `misc_utils` and `misc_utils.egg-info` to your `site-packages` folder.


### Usage

```python
import misc_utils as utils
utils.color_print('Yellow Text', 3)
```

### Documentation

The documentation webpage can be found here <https://misc-utils.readthedocs.io/en/latest/utils.html>.
