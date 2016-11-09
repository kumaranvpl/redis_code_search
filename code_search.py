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
            #for directory in directories:
            #    print os.path.join(root, directory)
            for filename in filenames:
                files_list.append(os.path.join(root, filename))
        return files_list

    def redis_search(self, search_word):
        files_list = self._get_all_files_on_path(self.redis_path)

        for files in files_list:
            """if search_word in open(files).read():
                print files"""
            with open(files, "r") as f:
                searchlines = f.readlines()
            for i, line in enumerate(searchlines):
                if search_word in line:
                    print "Keyword '%s' found in file '%s' on line number %s" % (search_word, files, i+1)
                    for l in searchlines[i:i + 3]: print l,
                    print


if __name__ == "__main__":
    #print "hello"
    search_word = str(sys.argv[1])
    redis_search = CodeSearch()
    start_time = time.time()
    redis_search.redis_search(search_word)
    print "Search took %s seconds" % (time.time() - start_time)
