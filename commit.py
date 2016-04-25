import os

# This function only READS the Commit info.
# There is no point in loading any commit in memory.
# What purpose can that serve? Nothing. (Prove this)
def load(cls, name, path):
    try:
        with open(path, 'rb') as commit_info_file:
            commit_info_dict = pickle.load(commit_info_file.read())
        return commit_info_dict
    except FileNotFoundError:
        print("Could not find commit-info here:\n`%s`" % path)
        sys.exit(1)


# This object hold only some info about a SINGLE Commit
class Commit:
    def __init__(self, parent, branch, message, repo):
        self.message = message
        self.hash = self.make_hash()
        # self.repo.dstore.get_commits_by_branch(branch)
        # make changes to tree
        # save
        # make chages to main tree?
        # exit

    def make_hash(self):
        return "yash uuid"