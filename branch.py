import os

class BranchInfo:
    def __init__(self, name, parent, repo):
        self.name = name
        # parent is a hash of the commit from which this branch was born.
        self.parent = parent
        self.repo = repo

    @classmethod
    def load(cls, name, path):
        try:
            with open(path, 'rb') as info:
                self.info = pickle.load(info.read())
        except FileNotFoundError:
            print("Could not find branch-info here:\n`%s`" % info_file)
            sys.exit(1)