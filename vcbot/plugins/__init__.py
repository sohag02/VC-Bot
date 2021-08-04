from os.path import dirname, basename, isfile, join
import glob

plugins = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in plugins if isfile(f) and not f.endswith("__init__.py")
]