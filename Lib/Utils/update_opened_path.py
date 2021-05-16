from global_imports import *

data_path = "Utils/open_path"
if not os.path.exists(data_path):
    os.mkdir(data_path)


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
