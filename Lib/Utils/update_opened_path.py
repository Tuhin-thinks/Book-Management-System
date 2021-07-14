from global_imports import *

base = os.path.dirname(__file__)
data_path = os.path.join(base, "open_path")  # open_path is the file (TEXT)


def check_dir_location(filename):
    if os.path.exists(data_path):
        path_data = json.load(open(data_path, 'r'))
        if os.path.exists(path_data['open_path']) and os.path.realpath(path_data['open_path']) == os.path.realpath(
                filename):
            return True  # same
    # if load data doesn't exists or name doesn't match create with the new one
    with open(data_path, 'w') as f:
        json.dump({"open_path": os.path.dirname(filename)}, f, indent=3)
    return False  # different files (or False means, data file updated)
