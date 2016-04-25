import os, sys, pickle, commit, branch

class DataStore:
    def __init__(self, base):
        # base == absolute path to project dir
        self.base_dir = os.path.join(base, '.ps')
        self.project_dir = base
        self.branches_dir = os.path.join(self.base_dir, 'branches')
        self.commit_tree = {}
        self.commit_updated = False

        self.load_branches()

    def get_commits_by_branch(self, branch):
        ct_file_path = os.path.join(self.branches_dir, '%s-cm.pkl'%branch)
        return commit.load(ct_file_path)

    def load_commits_in_all(self):
        # this is the master commit tree for the repo. No other tree is "stored".
        for branch in self.branches:
            self.commit_tree.update(self.get_commits_by_branch(branch))
        else:
            raise RuntimeError("First load all branches, use `Repository.load_branches()`")

    def load_branches(self):
        branch_names = os.listdir(self.branches_dir)
        self.branches = {}
        for branch in branch_names:
            info_path = os.path.join(self.branches_dir, os.path.join(branch, '%s-info.pkl'%branch))
            self.branches[branch] = branch.BranchInfo.load(info_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def check_and_save_diff(diff_dest, oldf, newf):
        # diff_dest is <path> join <name-of-this-diff>
        # oldf and newf also have same format
        if os.system('diff -q %s %s' % (oldf, newf)) == 0:
            return False
        else:
            os.system('diff -N %s %s > %s' % (oldf, newf, diff_dest))
            return True