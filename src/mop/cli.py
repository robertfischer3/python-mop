"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mmop` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``mop.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``mop.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
from mop.framework.commands import Command

parser = argparse.ArgumentParser(description="Welcome to Mop!\nCommand descriptions.", epilog='Robert Fischer, 2020')

parser.add_argument('-p', '--policy', action='store', help='Policy command palete')
parser.add_argument('-pyp', '--python_policy', action='store', help='Python policies command palete')


def main(args=None):
    args = parser.parse_args(args=args)
    print(args.policy)
    print("launched...")
    cmd = Command(args)
    cmd.execute()
