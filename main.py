import repo, sys, os, argparse

def locate_ps(dirname):
    # try to look for a .ps folder in an ancestor of CWD
    while dirname != '/':
        if os.path.exists('.ps'):
            return os.path.join(dirname)
        dirname = os.path.split(dirname)[0]
    return None

parser = argparse.ArgumentParser(add_help = True)
parser.add_argument('command', choices = ('init', 'status', 'fork', 'merge', 'add'), type=str)
parser.add_argument('--verbosity', '-v', help="Can be used to make output more verbose.", action='count', default = 0)

if __name__ == '__main__':
    # Parse arguments first
    _args = parser.parse_args()
    if _args.command == None:
        # Show usage and exit
        parser.print_usage()
        sys.exit(1)
    # command has been specified
    # try to guess context only is command is NOT init
    _base_dir = locate_ps(os.getcwd())
    if not _base_dir:
        if _args.command == 'init':
            R = repo.Repository.init(_args)
        else:
            print("No pitstops repo detected here.")
            sys.exit(1)

    # Found a repo, now process "_args.command" (init already handled).
    # if _args.command == 'add'
    # elif
    # elif
    # .
    # .
    # .
    # else