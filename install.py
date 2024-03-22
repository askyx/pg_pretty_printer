import os
import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python install.py PG_INSTALL_DIR")

    source = os.path.dirname(os.path.abspath(__file__)) + '/postgres-gdb.py'
    target = args[1] + '/postgres-gdb.py'

    try:
        if not os.path.exists(args[1]):
            raise Exception("pg install directory does not exist")
        
        if not os.access(args[1], os.W_OK):
            raise Exception("pg install directory is not writable")

        if os.path.exists(target):
            raise Exception("File 'postgres-gdb.py' already exists in the pg install directory")

        postgres = args[1] + '/postgres'
        if os.path.isfile(postgres) and os.access(postgres, os.X_OK):
            os.symlink(source, target)
        else:
            raise Exception("File 'postgres' not exists in the target directory, make sure you spcified a correct directory")


        gdbinit_file = os.path.expanduser('~/.gdbinit')
        if os.path.exists(gdbinit_file):
            with open(gdbinit_file, 'a') as f:
                f.write('add-auto-load-safe-path '+ args[1] + '\n')
        else:
            with open(gdbinit_file, 'w') as f:
                f.write('add-auto-load-safe-path '+ args[1] + '\n')

    except Exception as e:
        print("An error occurred:", e)
