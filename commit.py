import os

def load(cls, name, path):
	try:
		with open(path, 'rb') as commit:
			commit_dict = pickle.load(commit.read())
		return commit_dict
	except FileNotFoundError:
		print("Could not find commit-tree here:\n`%s`" % path)
		sys.exit(1)

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