import json, pickle, os, traceback, sys
import fsystem

DEFAULT_CONFIG = {
	"last_mod" : "?",
	"last_access" : "?",
}

class Developer:
	def __init__(self, name, email, uid):
		self.name = name
		self.email = email
		self.uid = uid

	def __repr__(self):
		return "<%s aka @%s, %s>" % (self.name, self.uid, self.email)

class Repository:
	def __init__(self, name, owner_name, owner_email, owner_uid, loc):
		self.name = name
		self.owner = Developer(owner_name, owner_email, owner_uid)
		self.base_dir = os.path.abspath(os.path.join(os.getcwd(), loc))
		if not (os.path.exists(os.path.join(self.base_dir, '.ps'))):
			os.mkdir(os.path.join(self.base_dir, '.ps'))
		self.config_updated = False

		self.cfile = ".ps/config.json"
		self.read_config()

	def save_repo(self):
		self.save_config()
		repo_dfile = os.path.join(self.base_dir, '.ps/repo_%s_data.pkl'%self.name)
		pickle.dump(self, open(repo_dfile, 'wb'))

	def read_config(self):
		cfile_path = os.path.join(self.base_dir, self.cfile)
		try:
			with open(cfile_path, 'r') as cfile:
				jconf = cfile.read()
				self.CONFIG = json.loads(jconf)
		except FileNotFoundError:
			print("Config file is missing, using defaults.")
			self.CONFIG = DEFAULT_CONFIG
			self.config_updated = True

	def save_config(self):
		if (self.config_updated):
			cfile_path = os.path.join(self.base_dir, self.cfile)
			with open(cfile_path, 'w') as cfile:
				cfile.write(json.dumps(self.CONFIG, sort_keys=True))

	def setup_datastore_objects(self):
		self.dstore = fsystem.Datastore(self.base_dir)

	def __repr__(self):
		return ("The repository '%s' belongs to '%s'.\nBASE = %s" % (self.name, self.owner, self.base_dir))

	@classmethod
	def load_repo(cls, repo_dfile):
		try:
			rep = pickle.load(open(os.path.join(os.getcwd(), repo_dfile), 'rb'))
			rep.read_config()
			return rep
		except FileNotFoundError as err:
			print("Could not find any repo here:\n`%s`" % os.path.join(os.getcwd(), repo_dfile))
			sys.exit(1)
			