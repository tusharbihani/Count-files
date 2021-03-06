"""https://docs.python.org/3.6/library/timeit.html

Timer(stmt='pass', setup='pass', timer=<timer function>, globals=None)
Timer.repeat(repeat=3, number=1000000)
"""
import timeit
import sys
import os
from countfiles.utils.file_handlers import search_files, count_file_extensions1, count_files_by_extension
from countfiles.__main__ import main_flow


def get_locations(*args):
    return os.path.normpath(os.path.join(os.path.expanduser('~/'), *args))


main_no_feedback_no_table = """
main_flow([location, '-a', '-nf', '-nt'])
"""

main_feedback_table = """
main_flow([location, '-a'])
"""

search_files_feedback = """
data = search_files(dirpath=location, extension='', recursive=True, include_hidden=True)
counter = count_file_extensions1(file_paths=data, no_feedback=False)
"""

count_files_feedback = """
data = count_files_by_extension(dirpath=location, no_feedback=False, recursive=True, include_hidden=True)
"""


if __name__ == "__main__":

    if sys.platform.startswith('win'):
        location = get_locations('Desktop')
    elif sys.platform.startswith('darwin'):
        # specify folder
        pass
    elif sys.platform.startswith('linux'):
        # specify folder
        pass

    stmts = [search_files_feedback, count_files_feedback]
    for s in stmts:
        t = timeit.Timer(stmt=s, globals=globals())
        print(s, t.repeat(repeat=3, number=1))
