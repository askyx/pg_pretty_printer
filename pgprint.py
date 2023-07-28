import gdb
import string


class PgPrintCommand(gdb.Command):

    def __init__(self):
        super(PgPrintCommand, self).__init__("pgprint", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, False)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)
        if len(arg_list) != 1:
            raise gdb.GdbError ("Usage: pgprint var")

        l = gdb.parse_and_eval(arg_list[0])


        print(l)


PgPrintCommand()

