import imp
import os
import sys


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
    # print 'Running from path', os.path.dirname(sys.executable)
    return os.path.dirname(sys.executable)
  return os.path.dirname(sys.argv[0])
