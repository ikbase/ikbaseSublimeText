

## evn config

vim .bash_profile

```shell
#ikbase config
export IKBASE_ROOT=/Users/xxx/ikbase
export IKBASE_PY3_PACKAGES=/Users/xxx/.pyenv/versions/3.7.1/lib/python3.7/site-packages
launchctl setenv IKBASE_ROOT $IKBASE_ROOT
launchctl setenv IKBASE_PY3_PACKAGES $IKBASE_PY3_PACKAGES
```
source .bash_profile


## Require

Python 3.x

PIL
./pip3 install Pillow

python git
./pip3 install gitpython


## REF:
[ref1](https://github.com/aviaryan/SublimeNotebook)


