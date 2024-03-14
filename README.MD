## PostgreSQL Pretty Printer Generator for GDB

This GDB pretty printer provides a more informative representation of PostgreSQL pointer objects, making it easier to debug PostgreSQL programs.




### How to use


1. clone this repo to your machine, and checkout to the target branch which you want to use. each branch corresponds to a specific PostgreSQL version or a database distributed by PostgreSQL.

    ```shell 
    git clone https://github.com/AntDB-postgresql/pretty_printer.git -b [target]
    ```

2. add the following line to your .gdbinit file:

    ```shell
    source {/path/to/pretty_printer}/pretty_printer.py
    ```

I strongly recommend you to add following line to your.gdbinit file too, to make the output more readable:

```shell
set print pretty on
set pagination off
```

now if you use gdb, you will see the pretty printer for PostgreSQL objects. just like this:

```shell
(gdb) p * parse
$2 = Query {commandType: CMD_SELECT, querySource: QSRC_ORIGINAL, queryId: 0, canSetTag: true, resultRelation: 0, hasAggs: false, hasWindowFuncs: false, hasTargetSRFs: false, hasSubLinks: false, hasDistinctOn: false, hasRecursive: false, hasModifyingCTE: false, hasForUpdate: false, hasRowSecurity: false, isReturn: false, mergeUseOuterJoin: false, override: OVERRIDING_NOT_SET, groupDistinct: false, limitOption: LIMIT_OPTION_COUNT, stmt_location: 0, stmt_len: 27} = {
  rtable = List with 1 elements = {
    0 = RangeTblEntry {rtekind: RTE_RELATION, relid: 197623, relkind: 114 'r', rellockmode: 1, perminfoindex: 1, security_barrier: false, jointype: JOIN_INNER, joinmergedcols: 0, funcordinality: false, ctename: 0x0, ctelevelsup: 0, self_reference: false, enrname: 0x0, enrtuples: 0, lateral: false, inh: true, inFromCl: true} = {
      eref = Alias aliasname: 'datatype_tbl2' = {
        colnames = List with 2 elements = {
          0 = String [ 'id' ],
          1 = String [ 'sal' ]
        }
      }
    }
  },
  rteperminfos = List with 1 elements = {
    0 = RTEPermissionInfo {relid: 197623, inh: true, requiredPerms: 2, checkAsUser: 0, selectedCols: (b 8 9), insertedCols: 0x0, updatedCols: 0x0}
  },
  jointree = FromExpr  = {
    fromlist = List with 1 elements = {
      0 = RangeTblRef rtindex: 1
    }
  },
  targetList = List with 2 elements = {
    0 = TargetEntry {resno: 1, resname: 'id', ressortgroupref: 0, resorigtbl: 197623, resorigcol: 1, resjunk: false} = {
      expr = Var {varno: 1, varattno: 1, vartype: 23, vartypmod: -1, varcollid: 0, varnullingrels: 0x0, varlevelsup: 0, varnosyn: 1, varattnosyn: 1, location: 7}
    },
    1 = TargetEntry {resno: 2, resname: 'sal', ressortgroupref: 0, resorigtbl: 197623, resorigcol: 2, resjunk: false} = {
      expr = Var {varno: 1, varattno: 2, vartype: 1700, vartypmod: 2490409, varcollid: 0, varnullingrels: 0x0, varlevelsup: 0, varnosyn: 1, varattnosyn: 2, location: 7}
    }
  }
}
```

### Features

* easy to add new printer for new PostgreSQL types
* support all PostgreSQL types, including composite types, arrays, and range types
* different print level
  * off  
      close 
  * origin
  * trace


### Print Level (TODO)

* off
* oringin
  like pprint
  * can not call in core file, need call func
* trace
  like pprint， buf in python
  * work anywhere
* info
  * call some func to eval pointer

### Add your pretty printer

To add your own pretty printer, you need to implement a new class that inherits from the `PrettyPrinter` class in the `pretty_printer.py` file. The `PrettyPrinter` class provides a set of methods that you can override to provide a custom pretty printer for a specific type of object.


### License

This project is licensed under the MIT License.
