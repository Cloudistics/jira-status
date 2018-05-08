"""
Filepath-related utility functions.
"""
import imp
import os
import sys


def is_valid_file(parser, arg):
    """
    Determine if the file passed as an argument is a valid file.

    Args:
      parser (ArgumentParser): argparse argument parser.
      arg (file): the file passed to the argument parser.
    """
    filepath = arg.strip()
    if not os.path.exists(filepath):
        return parser.error('The file %s does not exist.' % arg)

    # Return an open file handle.
    return open(filepath, 'rb')


def main_is_frozen():
    """
    Determine if the main script is frozen.
    """
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers")  # old py2exe
            or imp.is_frozen("__main__"))  # tools/freeze


def get_main_dir():
    """
    Get the directory path of the __main__ file.
    """
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])
