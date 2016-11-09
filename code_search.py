import os
import sys
import time


class CodeSearch:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.redis_path = self.dir_path + "/redis-unstable"

    def _get_all_files_on_path(self, path):
        files_list = []
        for root, directories, filenames in os.walk(path):
            # for directory in directories:
            #    print os.path.join(root, directory)
            for filename in filenames:
                files_list.append(os.path.join(root, filename))
        return files_list

    def _search_word_in_file(self, filename, word):
        """if search_word in open(files).read():
                        print files"""
        with open(filename, "r") as f:
            searchlines = f.readlines()
        for i, line in enumerate(searchlines):
            if word in line:
                print "Keyword '%s' found in file '%s' on line number %s" % (word, filename, i + 1)
                for l in searchlines[i:i + 3]: print l,
                print

    def redis_search(self, search_word, part_of=None):
        files_list = self._get_all_files_on_path(self.redis_path)

        if part_of in ["func", "function"]:
            search_word = " " + search_word + "("

        for files in files_list:
            self._search_word_in_file(filename=files, word=search_word)


def do_search(word, part_of=None):
    if part_of:
        if part_of not in ["func", "function", "param", "parameter", "var", "variable"]:
            print "part_of has unsupported value - '%s'. converting it to None" % part_of
            print "Supported values are func/function, param/parameter, var/variable"
            part_of = None
    redis_search = CodeSearch()
    start_time = time.time()
    redis_search.redis_search(word, part_of)
    print "Search took %s seconds" % (time.time() - start_time)


if __name__ == "__main__":
    #print "hello"
    s_word = str(sys.argv[1])
    if sys.argv[2]:
        prt_of = str(sys.argv[2])
        do_search(s_word, part_of=prt_of)
    else:
        do_search(s_word)

