import unittest
import os
from contextlib import redirect_stdout
import filecmp
from countfiles.utils.word_counter import show_2columns, show_result_for_search_files
from countfiles.utils.file_handlers import count_files_by_extension, search_files


class TestWordCounter(unittest.TestCase):
    """Testing word_counter.py functions"""

    def get_locations(self, *args):
        print('LOCATION: ', os.path.normpath(os.path.join(os.path.dirname(__file__), *args)))
        return os.path.normpath(os.path.join(os.path.dirname(__file__), *args))

    def test_show_2columns(self):
        test1 = self.get_locations('compare_tables', 'test_2columns_sorted.txt')
        test2 = self.get_locations('compare_tables', 'test_2columns_most_common.txt')
        data = count_files_by_extension(dirpath=self.get_locations('data_for_tests'), no_feedback=True,
                                        include_hidden=False, recursive=True)
        with open(test1, 'w') as f:
            with redirect_stdout(f):
                show_2columns(sorted(data.items()))
        with open(test2, 'w') as f:
            with redirect_stdout(f):
                show_2columns(data.most_common())
        self.assertEqual(filecmp.cmp(test1, self.get_locations('compare_tables', '2columns_sorted.txt'),
                                     shallow=False), True)
        self.assertEqual(filecmp.cmp(test2, self.get_locations('compare_tables', '2columns_most_common.txt'),
                                     shallow=False), True)

    # TODO:  test show_result_for_search_files(files=data, no_list=False) for different OS
    def test_show_result_for_search_files(self):
        """Testing def show_result_for_search_files. Search by extension.
        Comparison of the file with the results of the function with the specified file.

        Expected behavior:
        no_list=True
        Found ... file(s).
        Total combined size: ... KiB.
        Average file size: ... KiB (max: ... KiB, min: ... B).
        no_list=False default
        full/path/to/file1.extension (... KiB)
        full/path/to/file2.extension (... KiB)
        ...
        Found ... file(s).
        Total combined size: ... KiB.
        Average file size: ... KiB (max: ... KiB, min: ... B).
        :return:
        """
        data = search_files(dirpath=self.get_locations('data_for_tests'), extension='.', include_hidden=False, recursive=True)
        test1 = self.get_locations('compare_tables', 'test_show_result_no_list.txt')
        with open(test1, 'w') as f:
            with redirect_stdout(f):
                show_result_for_search_files(files=data, no_list=True, no_feedback=True)
        self.assertEqual(filecmp.cmp(test1, self.get_locations('compare_tables', 'show_result_no_list.txt'),
                                     shallow=False), True)

# from root directory:
# run all tests in test_word_counter.py
# python -m unittest tests/test_word_counter.py
# run all tests for class TestWordCounter
# python -m unittest tests.test_word_counter.TestWordCounter
# run test for def test_get_files_by_extension in class TestWordCounter
# python -m unittest tests.test_word_counter.TestWordCounter.test_get_files_by_extension

# or run file in PyCharm


if __name__ == '__main__':
    unittest.main()
