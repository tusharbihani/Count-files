from collections import OrderedDict
from pathlib import Path
import datetime
import os
from utils.file_handlers import human_mem_size


class WordCounter:
    def __init__(self):
        self.counters = dict()

    def count_word(self, word: str):
        if word in self.counters.keys():
            self.counters[word] += 1
        else:
            self.counters[word] = 1

    def sort_by_frequency(self):
        sorted_counters = [(word, self.counters[word])
                           for word in sorted(self.counters,
                                              key=self.counters.get,
                                              reverse=True)]
        return sorted_counters

    def sort_by_word(self):
        ordered = OrderedDict(sorted(self.counters.items()))
        sorted_counters = ordered.items()
        return sorted_counters

    @staticmethod
    def show_2columns(data):
        if len(data) == 0:
            print("Oops! We have no data to show...\n")
            return

        max_word_width = 9  # default value, the minimum EXTENSION col. width
        total_occurences = 0
        for word, freq in data:
            total_occurences += freq
            max_word_width = max(len(word), max_word_width)

        total_occurences_width = len(str(total_occurences))
        if total_occurences_width < 5:
            total_occurences_width = 5

        header = f" {'EXTENSION'.ljust(max_word_width)} | {'FREQ.'.ljust(total_occurences_width)} "
        sep_left = (max_word_width + 2) * '-'
        sep_center = "+"
        sep_right = (total_occurences_width + 2) * '-'
        sep = sep_left + sep_center + sep_right
        print(header)
        print(sep)

        for word, freq in data:
            line = f" {word.ljust(max_word_width)} | {str(freq).rjust(total_occurences_width)} "
            print(line)
        print(sep)
        line = f" {'TOTAL:'.ljust(max_word_width)} | {str(total_occurences).rjust(total_occurences_width)} "
        print(line)
        print(sep + "\n")

    def show_total(self) -> int:
        total = 0
        for _, freq in self.counters.items():
            total += freq
        print(f"Total number of files in selected directory: {total}.\n")
        return total

    @staticmethod
    def get_files_by_extension(location: str, extension: str, preview=False, preview_size=395) -> int:
        """ Search recursively (in the folder indicated by ``location`) for files
        that have the given extension in their filename and optionally display
        a preview of the file.
        Special thanks to Natalia Bondarenko (github.com/NataliaBondarenko),
        who suggested this feature and submited an initial implementation.
        """
        files = sorted(Path(os.path.expanduser(location)).rglob(f"*.{extension}"))

        print(f'\nRecursively searching for .{extension} files in{location}.\n')

        if files:
            sizes = []
            for f in files:
                sizes.append(f.stat().st_size)

                print(f'{f} ({human_mem_size(f.stat().st_size)})')
                if preview:
                    print('–––––––––––––––––––––––––––––––––––')
                    print(f.read_text(errors="replace")[0:preview_size].replace('\n', ' '))
                    print("–––––––––––––––––––––––––––––––––––\n")

            total_size = sum(sizes)
            h_total_size = human_mem_size(total_size)
            avg_size = human_mem_size(int(total_size / len(files)))

            h_max = human_mem_size(max(sizes))
            h_min = human_mem_size(min(sizes))

            print(f"\n   Found {len(files)} .{extension} files.")
            print(f"   Total combined size: {h_total_size}.")
            print(f"   Average file size: {avg_size} (max: {h_max}, min: {h_min}).\n")
            return len(files)

        else:
            print(f"No files with the extension '{extension}' were found in the specified directory.\n")
            # len([]) == 0
            return len(files)