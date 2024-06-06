#!/usr/bin/python3

import os
import sys
import json


DATA_FILE_PATH = "storage/data.json"


def find_all_files_by_ext(path, ext=".py"):
    res = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                res.append(os.path.join(root, file))
    return res


if __name__ == "__main__":
    path = None
    ext = None
    language = None
    context = None
    question = None
    for i, a in enumerate(sys.argv):
        if i == 1:
            path = a
        elif i == 2:
            ext = a
        elif i == 3:
            language = a
        elif i == 4:
            context = a
        elif i == 5:
            question = a

    all_files = find_all_files_by_ext(path, ext)

    os.unlink(DATA_FILE_PATH)

    data_list = []

    for file_path in all_files:
        tmp = {
            "language": language,
            "context": context,
            "question": question,
            "path": "/%s" % (file_path)
        }
        data_list.append(tmp)

    with open(DATA_FILE_PATH, "a") as outfile: 
        json.dump(data_list, outfile)

    print("data.json done. Found %s files" % (len(all_files)))
