## PostgreSQL Pretty Printer Generator for GDB

GDB pretty printer for PostgreSQL, 在 gdb 中直接打印对象结构。

### How to use


1. clone 这个项目，然后选择你想使用得版本分支，当前一个分支就代表一个 PG 版本，或者是其他从 pg 衍生出来的数据库

    ```shell 
    git clone https://github.com/askyx/pretty_printer.git -b [target]
    ```

2. 如果你可以直接执行 `pg_config` 命令，则可以直接使用 cmake 安装(cmake 是为了以后可以在此项目中实现一个 PG 的一些插件，方便个人使用)

    ```shell
    cd pretty_printer
    cmake -Bbuild
    cmake --build build  --target install
    ```

3. 或者直接手动安装，主要就是把文件 `postgres-gdb.py` 拷贝到 pg 的 bin 目录下，并在 `~/.gdbinit` 中添加 `add-auto-load-safe-path` 命令，这样 gdb 就会自动加载这个文件。

    ```shell    
    cd pretty_printer
    ln -s `pwd`/postgres-gdb.py `pg_config --bindir`/postgres-gdb.py
    echo "add-auto-load-safe-path `pg_config --bindir`" >> ~/.gdbinit
    ```


同时建议在 `~/.gdbinit` 中添加以下设置，以便于查看更加友好的输出

```shell
set print pretty on
set pagination off
```

现在如果你在 gdb 中调试语句 `select 1;`， 现在查看 parse 变量，应该会看到如下输出

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


### Add your pretty printer

1. 在`printer/node_struct.py`中添加你自己的结构体
    * 如果是继承， 则需要展开父类的字段，如 `plan.startup_cost`
    * 如果是数组，则需要标记数组大小， 例如 `  ('int[ncolumns]', 'indexkeys'),`
    * 需要注意是否存在相互引用的问题， 典型的例子就是 `RestrictInfo` 结构体中包含 `parent_ec` 数组， 而 `parent_ec` 结构体又会指向当前结构体

2. 当前已经 cover 大部分结构体，除非你想对某结构体实现自己的打印格式，则需要自己尝试修改打印逻辑


### License

This project is licensed under the MIT License.
