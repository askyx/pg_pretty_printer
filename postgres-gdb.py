import sys
import gdb
import os
import os.path

if gdb.current_objfile () is not None:
    path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, path)
  
from printer import register_postgres_printers
register_postgres_printers(gdb.current_objfile())