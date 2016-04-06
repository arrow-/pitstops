import repo, sys, os, argparse

if __name__ == '__main__':
	R = repo.Repository.load_repo('poop/.ps/repo_ggyf_data.pkl')
	# R = repo.Repository('ggyf', 'uyytf', 'bar@doo.com', 'itf', 'poop')
	# print(R)
	# R.save_repo()
	print(R.CONFIG)
