import sys
import gdb
import os
import os.path

if gdb.current_objfile () is not None:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
  
from printer import register_postgres_printers
register_postgres_printers(gdb.current_objfile())