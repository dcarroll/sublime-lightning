import os
from os import path


def walk_up(bottom):
    """
    mimic os.walk, but walk 'up'
    instead of down the directory tree
    """
    bottom = path.realpath(bottom)

    # get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception as e:
        print(e)
        return

    dirs, nondirs = [], []
    for name in names:
        if path.isdir(path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = path.realpath(path.join(bottom, '..'))

    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x

if __name__ == '__main__':
    # tests/demos

    # print all files and directories
    # directly above the current one
    for i in walk_up(os.curdir):
        print(i)

    # look for a TAGS file above the
    # current directory
    for c, d, f in walk_up(os.curdir):
        if 'TAGS' in f:
            print(c)
            break
