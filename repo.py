import json, pickle, os, traceback, sys
import fsystem

DEFAULT_CONFIG = {
    "last_mod" : "?",
    "last_access" : "?",
}

class Developer:
    def __init__(self, name, email, usrname):
        self.name = name
        self.email = email
        self.username = usrname
        self.uid = hash(name+email)

    def __repr__(self):
        return "<%s aka @%s, %s>" % (self.name, self.username, self.email)

class Repository:
    def __init__(self, name, owner_name, owner_usrname, owner_email, loc=None):
        self.name = name
        self.owner = Developer(owner_name, owner_usrname, owner_email)
        if loc == None:
            loc = name
        self.base_dir = os.path.abspath(os.path.join(os.getcwd(), loc))
        psdir = os.path.join(self.base_dir, '.ps')
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        if not (os.path.exists(psdir)):
            os.mkdir(psdir)
        self.config_updated = False

        self.cfile = ".ps/config.json"
        self.read_config()

    def save_repo(self):
        self.save_config()
        repo_dfile = os.path.join(self.base_dir, '.ps/repo_data.pkl')
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
    
    #####################################  ^^^^ WONT CHANGE ^^^^  ################################3
    
    @classmethod
    def init(cls, cmd_line_args):
        print("Just give us a few details...")
        if cmd_line_args.verbosity > 0:
            print("/i\ Leave fields blank to use the value suggested.")
            print("/i\ You can leave several fields blank and configure them later.\n")
        _name = input("1. What would you call this project? ")
        _owner = input("2. Who owns this (full name)? ")
        _username = input("3. User handle of '%s' on pitstops-hub? " % _owner)
        while True:
            _email = input("4. Associated email-id? ")
            if '@' in _email and '.com' in _email and _email.find('@') < _email.find('.com'):
                _email_left, _email_right = _email.split('@')
                _email_mid, _email_right = _email_right.split('.com')
                if (len(_email_mid) > 0 and len(_email_left) > 0 and len(_email_right) == 0):
                    # email is valid
                    break
                elif cmd_line_args.verbosity > 0:
                    print("/*\ The email-id provided seems to be invalid, please review it.")
            elif cmd_line_args.verbosity > 0:
                print("/*\ The email-id provided seems to be invalid, please review it.")
        _loc = input("Where would you want to locate the project directory? [./%s]\n" % _name)
        if _loc == '':
            _loc = None
        R = cls(_name, _owner, _username, _email, _loc)
        print(R)
        R.save_repo()