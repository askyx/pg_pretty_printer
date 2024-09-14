<p align="center">
  <br>A generator for quickly generating GDB pretty printers for PostgreSQL.<br>
</p>

## PostgreSQL Pretty Printer Generator for GDB

This GDB pretty printer provides a more informative representation of PostgreSQL pointer objects, making it easier to debug PostgreSQL programs.

* supports all most pg structure types, totally 400+ (but except type in executor)
* easy to use, just one command to install
* easy to extend, This is backward compatible. If there are no significant changes or new types added, it may not even need to be modified.

* this is implemented on REL_17_BETA1

### requirements

* GDB 15 or later
* Python 3.10 or later

> works on Ubuntu 24.04 LTS will

### How to use


<!-- 1. clone this repo to your machine, and checkout to the target branch which you want to use. each branch corresponds to a specific PostgreSQL version or a database distributed by PostgreSQL. -->
1. clone this repo to your machine

    ```shell 
    git clone https://github.com/askyx/pg_pretty_printer.git
    ```

2. make sure you can execute `pg_config`, do flowing command to install the pretty printer to your GDB.

    ```shell
    cd pg_pretty_printer
    cmake -Bbuild
    cmake --build build  --target install
    ```

I strongly recommend you to add following line to your.gdbinit file too, to make the output more readable:

```shell
set print pretty on
set pagination off
```

now if you use gdb to debug ``select 1;``, you will see the pretty printer for PostgreSQL objects. just like this:

```shell
$1 = Query {commandType: CMD_SELECT, querySource: QSRC_ORIGINAL, queryId: 0, canSetTag: true, resultRelation: 0, hasAggs: false, hasWindowFuncs: false, hasTargetSRFs: false, hasSubLinks: false, hasDistinctOn: false, hasRecursive: false, hasModifyingCTE: false, hasForUpdate: false, hasRowSecurity: false, isReturn: false, mergeTargetRelation: 0, override: OVERRIDING_NOT_SET, groupDistinct: false, limitOption: LIMIT_OPTION_COUNT, stmt_location: 0, stmt_len: 8} = {
  jointree = ,
  targetList = List with 1 elements = {
    0 = TargetEntry {resno: 1, resname: '?column?', ressortgroupref: 0, resorigtbl: 0, resorigcol: 0, resjunk: false} = {
      expr = Const {consttype: 23, consttypmod: -1, constcollid: 0, constlen: 4, constvalue: 1, constisnull: false, constbyval: true}
    }
  }
}
```

### How

#### 1. how to get the pointer object information in GDB and implement a pretty printer for PostgreSQL objects.

When we compiling the program, if we choose to retain symbol information, we can obtain this information through certain means. In gdb, we can retrieve it using the fields function within the type. For example, consider the following example:


```c++
(gdb) b planner
Breakpoint 1 at 0x55a0564fc233: file /workspaces/postgres/src/backend/optimizer/plan/planner.c, line 397.
(gdb) c
Continuing.

Breakpoint 1, planner (parse=0x55a05825e918, ...) at /workspaces/postgres/src/backend/optimizer/plan/planner.c:397
397             if (planner_hook)
(gdb) python v = gdb.parse_and_eval('parse')
(gdb) python print(gdb.types.get_basic_type(v.dereference().type).fields())
[<gdb.Field object at 0x7f4fd4e23af0>, <gdb.Field object at 0x7f4fd4e217d0>, <gdb.Field object at 0x7f4fd4c1edd0>, <gdb.Field object at 0x7f4fd4c1edb0>, <gdb.Field object at 0x7f4fd4c1edf0>, <gdb.Field object at 0x7f4fd4c1ee10>, <gdb.Field object at 0x7f4fd4c1ee30>, <gdb.Field object at 0x7f4fd4c1ee70>, <gdb.Field object at 0x7f4fd4c1eeb0>, <gdb.Field object at 0x7f4fd4c1eef0>, <gdb.Field object at 0x7f4fd4c1ef30>, <gdb.Field object at 0x7f4fd4c1ef70>, <gdb.Field object at 0x7f4fd4c1efb0>, <gdb.Field object at 0x7f4fd4c1eff0>, <gdb.Field object at 0x7f4fd4c1f030>, <gdb.Field object at 0x7f4fd4c1f070>, <gdb.Field object at 0x7f4fd4c1f0b0>, <gdb.Field object at 0x7f4fd4c1f0f0>, <gdb.Field object at 0x7f4fd4c1f130>, <gdb.Field object at 0x7f4fd4c1f170>, <gdb.Field object at 0x7f4fd4c1f1b0>, <gdb.Field object at 0x7f4fd4c1f1f0>, <gdb.Field object at 0x7f4fd4c1f230>, <gdb.Field object at 0x7f4fd4c1f270>, <gdb.Field object at 0x7f4fd4c1f2b0>, <gdb.Field object at 0x7f4fd4c1f2f0>, <gdb.Field object at 0x7f4fd4c1f330>, <gdb.Field object at 0x7f4fd4c1f370>, <gdb.Field object at 0x7f4fd4c1f3b0>, <gdb.Field object at 0x7f4fd4c1f3f0>, <gdb.Field object at 0x7f4fd4c1f430>, <gdb.Field object at 0x7f4fd4c1f470>, <gdb.Field object at 0x7f4fd4c1f4b0>, <gdb.Field object at 0x7f4fd4c1f4f0>, <gdb.Field object at 0x7f4fd4c1f530>, <gdb.Field object at 0x7f4fd4c1f570>, <gdb.Field object at 0x7f4fd4c1f5b0>, <gdb.Field object at 0x7f4fd4c1f5f0>, <gdb.Field object at 0x7f4fd4c1f630>, <gdb.Field object at 0x7f4fd4c1f670>, <gdb.Field object at 0x7f4fd4c1f6b0>, <gdb.Field object at 0x7f4fd4c1f6f0>, <gdb.Field object at 0x7f4fd4c1f730>, <gdb.Field object at 0x7f4fd4c1f770>]
(gdb) python filds = (gdb.types.get_basic_type(v.dereference().type).fields())
(gdb) python print(filds[0])
<gdb.Field object at 0x7f4fd4e21830>
(gdb) python print(filds[0].name)
type
(gdb) python print(filds[0].type)
NodeTag
(gdb)
```

The array printed by `python print(gdb.types.get_basic_type(v.dereference().type).fields())` contains all the field information of the `Query` structure. We can extract the fields from this list. The Field definition is as follows. 

```python
@final
class Field:
    bitpos: int | None
    enumval: int
    name: str | None
    artificial: bool
    is_base_class: bool
    bitsize: int
    type: Type | None
    parent_type: Type
```

After that, we can loop through these fields and use the extracted information to print the fields you want in the structure. For example, the following function mainly checks if the field is of a no pointer type, and if so, prints it here.

```python
    def common_to_string(self):
        fields = []
        node = self.get_type(self.val)

        for field in self.val.type.fields():
            if self.printable(field.name):

                # Relids is def of Bitmapset *
                if str(field.type) == 'Relids':
                    continue

                # print no pointer field
                if field.type.code != gdb.TYPE_CODE_PTR:
                    fields.append('{}: {}'.format(field.name, self.val[field.name]))

                # print char * field
                if field.type.code == gdb.TYPE_CODE_PTR and self.val[field.name] != 0 and str(field.type) == 'char *':
                    fields.append('{}: {}'.format(field.name, getchars(self.val[field.name])))
        
        #  no printable fields
        if len(fields) == 0:
            return None
        return node + ' {' + ', '.join(fields) + '}'
```

Using the above function, if you print a `FuncExpr`, it will print in gdb:
```
FuncExpr {funcid: 1740, funcresulttype: 1700, funcretset: false, funcvariadic: false, funcformat: COERCE_IMPLICIT_CAST, funccollid: 0, inputcollid: 0}
```

The `args` of `FuncExpr` is a pointer and needs to be dereferenced, so it is handled later.

Following the above approach, we canimplement a prettye printer for pg. unless there are significant changes, the printer should still work normally.


#### 2. How to Make It More Convenient and Secure for Us to Use

Normally, the gdb script can be directly placed in `.gdbinit` and then it will be take effect when you use gdb to debug a program. However, for this project, it cannot be done so simply. Directly placing the script in `.gdbinit` can affect the entire environment. The most direct consequence is that it will cause type conflicts. In this project, we support print about 400+ types of structures (and more may be added later), some of which have very generic names, such as `Node`. If other projects use the same structure name and when you use gdb debug it at this time, you will get a type conflicts, causing normal debugging to be difficult.

Therefore, We used gdb's `auto-load` mechanism here. The script will only be loaded when you are debugging the `postgres` process; it will not be triggered for other programs.

### License

This project is licensed under the MIT License.
