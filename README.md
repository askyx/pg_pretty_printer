<p align="center">
  <br> English | <a href="README-CN.md">中文</a>
  <br>A generator for quickly generating GDB pretty printers for PostgreSQL.<br>
</p>

## PostgreSQL Pretty Printer Generator for GDB

This GDB pretty printer provides a more informative representation of PostgreSQL pointer objects, making it easier to debug PostgreSQL programs.


### How to use


1. clone this repo to your machine, and checkout to the target branch which you want to use. each branch corresponds to a specific PostgreSQL version or a database distributed by PostgreSQL.

    ```shell 
    git clone https://github.com/askyx/pretty_printer.git -b [target]
    ```

2. make sure you can execute `pg_config`, do flowing command to install the pretty printer to your GDB.

    ```shell
    cd pretty_printer
    cmake -Bbuild
    cmake --build build  --target install
    ```

3. or else, you can install by following command:

    ```shell    
    cd pretty_printer
    ln -s `pwd`/postgres-gdb.py `pg_config --bindir`/postgres-gdb.py
    echo "add-auto-load-safe-path `pg_config --bindir`" >> ~/.gdbinit
    ```


I strongly recommend you to add following line to your.gdbinit file too, to make the output more readable:

```shell
set print pretty on
set pagination off
```

now if you use gdb to debug ``select 1;``, you will see the pretty printer for PostgreSQL objects. just like this:

```shell
(gdb) p * parse
$2 = Query {commandType: CMD_SELECT, querySource: QSRC_ORIGINAL, queryId: 0, canSetTag: true, resultRelation: 0, hasAggs: false, hasWindowFuncs: false, hasTargetSRFs: false, hasSubLinks: false, hasDistinctOn: false, hasRecursive: false, hasModifyingCTE: false, hasForUpdate: false, hasRowSecurity: false, isReturn: false, mergeUseOuterJoin: false, override: OVERRIDING_NOT_SET, groupDistinct: false, limitOption: LIMIT_OPTION_COUNT, stmt_location: 0, stmt_len: 8} = {
  jointree = FromExpr ,
  targetList = List with 1 elements = {
    0 = TargetEntry {resno: 1, resname: '?column?', ressortgroupref: 0, resorigtbl: 0, resorigcol: 0, resjunk: false} = {
      expr = Const {consttype: 23, consttypmod: -1, constcollid: 0, constlen: 4, constvalue: 1, constisnull: false, constbyval: true, location: 7}
    }
  }
}
```

more examples can be found in the [test](./test) directory.

### Add your pretty printer

1. add you node strucutre to [`printer/node_struct.py`](./printer/node_struct.py) file.

2. and do nothing, most of the work is done by the [`printer/printer.py`](./printer/printer.py) file.


### License

This project is licensed under the MIT License.
