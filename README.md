# Coursera Dump

This program scrapes coursera courses. To scrape coursera you could pass additional parameters -o (ouput path) and -n (number of courses). If you stuck with program abilities you can run it with -h argument.

# How to run

Example of running a script on a Linux with a Python3 interpreter.

```bash
$python3 coursera.py -o /home/zap/git/misc/1.xlsx
Output path exists. The file will be overriden
The file has been created:/home/zap/git/misc/1.xlsx
```

Example of running a script with -h argument passed in.

```bash
$python3 coursera.py -h
usage: coursera.py [-h] [-o OUTPUT] [-n NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path
  -n NUMBER, --number NUMBER
                        number of courses
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
