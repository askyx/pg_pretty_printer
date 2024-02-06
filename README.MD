## PostgreSQL Pointer Pretty Printer Generator for GDB

This GDB pretty printer provides a more informative representation of PostgreSQL pointer objects, making it easier to debug PostgreSQL programs.




### Installation

To install the pretty printer, add the following line to your .gdbinit file:

```shell

git clone xxx -b [target]

```

support 


* Postgres
* Greenplum
* Tbase
* Openguase









### Print Level

* off
* oringin
  like pprint
  * can not call in core file, need call func
* trace
  like pprint， buf in python
  * work anywhere
* info
  * call some func to eval pointer


### License

This project is licensed under the MIT License.