import sys

collect_ignore = []
if sys.version_info.major < 3:
    collect_ignore.append("tests/test_py3_annotation.py")
