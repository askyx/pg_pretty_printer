# pg pretty printer

Fri Jul 28 14:26:34 CST 2023

`gdb` 中结构格式化打印 `postgreSQL`  中的结构体

```sql
\t
\o  xxx
select oid, typname from pg_type ;
select oid, oprname from pg_operator ;

```

## require

* python 3.10
* gdb 12

## 功能特性

- `gdb` pretty打印pg结构体
- type oper以及var等自动分析
- [TODO]常量打印
- [TODO]自定义打印等级

* 新增参数
  - pg_retes : rtable, 辅助分析，没有设置则类似pprint，实质是保存当前对象所依赖的rtable的地址，在不同阶段，rtable 不一样，可能需要灵活调整
    * 某些重对象中包含rtable，后续在遇到类似对象得时候，动态分析
  - pg_verbose : 输出等级
    * 后续计划支持更多等级
    * trace : 类似pprint，不会解析
    * verbose ： 类似explan verbose， 尝试解析，且输出 targetlist
    * plain : 类似explain， 尝试简介输出
  - pg_print : 設置pretty_printer 功能开关

## 技术栈

* gdb pretty print
* python 
* postgreSQL

## 安装和使用

```
.gdbinit

source xxxx

```

## 示例代码

```sql

(gdb) p * queryDesc->plannedstmt
$2 = [commandType: CMD_SELECT, queryId: 0, hasReturning: false, hasModifyingCTE: false, canSetTag: true, transientPlan: false, dependsOnRole: false, parallelModeNeeded: false, jitFlags: 0] = {
  rtable = List with 19 elements = {
    0 = RangeTblEntry: [kind: RTE_SUBQUERY     , alias: 'x'              , relid:        0, relkind: 0 '\000'],
    1 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'x1'             , relid:    32966, relkind: 114 'r'],
    2 = RangeTblEntry: [kind: RTE_JOIN         , alias: 'unnamed_join'   , relid:        0, relkind: 0 '\000'],
    3 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'x2'             , relid:    32920, relkind: 114 'r'],
    4 = RangeTblEntry: [kind: RTE_JOIN         , alias: 'unnamed_join'   , relid:        0, relkind: 0 '\000'],
    5 = RangeTblEntry: [kind: RTE_SUBQUERY     , alias: 't'              , relid:        0, relkind: 0 '\000'],
    6 = RangeTblEntry: [kind: RTE_SUBQUERY     , alias: 'h'              , relid:        0, relkind: 0 '\000'],
    7 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'g1'             , relid:    32942, relkind: 114 'r'],
    8 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'g'              , relid:    32963, relkind: 114 'r'],
    9 = RangeTblEntry: [kind: RTE_JOIN         , alias: 'unnamed_join'   , relid:        0, relkind: 0 '\000'],
    10 = RangeTblEntry: [kind: RTE_SUBQUERY     , alias: 'g3'             , relid:        0, relkind: 0 '\000'],
    11 = RangeTblEntry: [kind: RTE_JOIN         , alias: 'unnamed_join'   , relid:        0, relkind: 0 '\000'],
    12 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'sys_business_area', relid:    32841, relkind: 114 'r'],
    13 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r'              , relid:    32841, relkind: 114 'r'],
    14 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r'              , relid:    32841, relkind: 114 'r'],
    15 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r1'             , relid:    32841, relkind: 114 'r'],
    16 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r'              , relid:    32841, relkind: 114 'r'],
    17 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r'              , relid:    32841, relkind: 114 'r'],
    18 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'r'              , relid:    32841, relkind: 114 'r']
  },
  planTree = Unique (cost=171.72..171.74 rows=1 width=1364 plan_node_id=0) <numCols: 6> = {
    lefttree = Sort (cost=171.72..171.73 rows=1 width=1364 plan_node_id=1) <numCols: 6> = {
      lefttree = {
        join = Join (cost=147.82..171.71 rows=1 width=1364 plan_node_id=2) <jointype: JOIN_LEFT, inner_unique: false> = {
          lefttree = {
            join = Join (cost=147.82..161.26 rows=1 width=1146 plan_node_id=3) <jointype: JOIN_RIGHT, inner_unique: false> = {
              lefttree = SeqScan (cost=0.00..12.50 rows=250 width=292 plan_node_id=4) <scanrelid: 2>,
              righttree = Hash (cost=147.81..147.81 rows=1 width=1000 plan_node_id=5) <skewTable: 32966, skewColumn: 1, skewInherit: false, rows_total: 0> = {
                lefttree = SubqueryScan (cost=85.48..147.81 rows=1 width=1000 plan_node_id=6) <scanrelid: 1, scanstatus: SUBQUERY_SCAN_NONTRIVIAL> = {
                  subplan = Group (cost=85.48..147.80 rows=1 width=1192 plan_node_id=7) <numCols: 8> = {
                    qual = List with 1 elements = {
                      0 = [opno: 98, opfuncid: 67, opresulttype: 16, opretset false, opcollid 0, inputcollid 100] = {
                        args = List with 2 elements = {
                          0 = RelabelType[resulttype: 25, resulttypmod: -1, resultcollid: 100, relabelformat: COERCE_IMPLICIT_CAST] = {
                            arg = [casetype: 1043, casecollid: 100] = {
                              args = List with 3 elements = {
                                0 = CaseWhen = {
                                  expr = [opno: 98, opfuncid: 67, opresulttype: 16, opretset false, opcollid 0, inputcollid 100] = {
                                    args = List with 2 elements = {
                                      0 = RelabelType[resulttype: 25, resulttypmod: -1, resultcollid: 100, relabelformat: COERCE_IMPLICIT_CAST] = {
                                        arg = [varno: -2, varattno: 9, vartype: 1043, vartypmod: 34, varcollid: 100, varlevelsup: 0, varnosyn: 13, varattnosyn: 6]
                                      },
                                      1 = 'busi_reg_city_code'
                                    }
                                  },
                                  result = [varno: -2, varattno: 10, vartype: 1043, vartypmod: 68, varcollid: 100, varlevelsup: 0, varnosyn: 13, varattnosyn: 1]
                                },
                                1 = CaseWhen = {
                                  expr = [opno: 98, opfuncid: 67, opresulttype: 16, opretset false, opcollid 0, inputcollid 100] = {
                                    args = List with 2 elements = {
                                      0 = RelabelType[resulttype: 25, resulttypmod: -1, resultcollid: 100, relabelformat: COERCE_IMPLICIT_CAST] = {
                                        arg = [varno: -2, varattno: 9, vartype: 1043, vartypmod: 34, varcollid: 100, varlevelsup: 0, varnosyn: 13, varattnosyn: 6]
...........

```

* 设置 rte

```sql
  subplans = List with 6 elements = {
    0 = SeqScan (cost=0.00..10.38 rows=1 width=146 plan_node_id=16) on r = {
      qual = List with 1 elements = {
        0 = ((r.id)::text = ([paramkind: PARAM_EXEC, paramid: 0, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      }
    },
    1 = SeqScan (cost=0.00..10.38 rows=1 width=218 plan_node_id=17) on r = {
      qual = List with 1 elements = {
        0 = ((r.id)::text = ([paramkind: PARAM_EXEC, paramid: 1, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      }
    },
    2 = SeqScan (cost=0.00..10.38 rows=1 width=146 plan_node_id=18) on r1 = {
      qual = List with 1 elements = {
        0 = ((r1.id)::text = ([paramkind: PARAM_EXEC, paramid: 2, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      }
    },
    3 = SeqScan (cost=10.38..20.75 rows=1 width=218 plan_node_id=19) on r = {
      qual = List with 1 elements = {
        0 = ((r.id)::text = ([paramkind: PARAM_EXEC, paramid: 3, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      },
      initPlan = List with 1 elements = {
        0 = [startup_cost: 0.00, per_call_cost: 10.38, subLinkType: EXPR_SUBLINK, plan_id: 3, plan_name: 0x5566f2c4db98 "InitPlan 3 (returns $3)", firstColType: 1043, firstColTypmod: 68, firstColCollation: 100, useHashTable: false, unknownEqFalse: false, parallel_safe: false] = {
          setParam = IntList with 1 elements = {3}
        }
      }
    },
    4 = SeqScan (cost=0.00..10.38 rows=1 width=218 plan_node_id=20) on r = {
      qual = List with 1 elements = {
        0 = ((r.id)::text = ([paramkind: PARAM_EXEC, paramid: 4, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      }
    },
    5 = SeqScan (cost=0.00..10.38 rows=1 width=146 plan_node_id=21) on r = {
      qual = List with 1 elements = {
        0 = ((r.id)::text = ([paramkind: PARAM_EXEC, paramid: 5, paramtype: 1043, paramtypmod: 68, paramcollid: 100])::text)
      }
    }
  },
  relationOids = OidList with 11 elements = {32966, 32920, 32942, 32963, 32841, 32841, 32841, 32841, 32841, 32841, 32841},
  paramExecTypes = OidList with 6 elements = {1043, 1043, 1043, 1043, 1043, 1043}

```

## attention

个人使用，还在持续演化中...

## 后续规划

* 完善安装方法，实现自动安装
  * 自动抓取部分元数据信息
  * gdb auto load ?? 
* 使用 oid， 动态查询元数据信息，辅助分析
  * 部分信息只凭借gdb难以获取
* 持续补全，且支持不同pg版本
* 其他数据库支持
* 更多的使用场景
  * optimizer 基础数据结构
    * plan tree 
    * path tree
  * storage
    * dump page
    * print page
    * wal
    * tx


## questions

### query中多层子查询

单独解析 Query 中的 rtable


```sql

select * from ta where (ta.a, ta.b) < (select a+1, b from tb where ta.a = tb.a);

$57 = CMD_SELECT = {
  rtable = List with 1 elements = {
    0 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'ta'             , relid:    16389, relkind: 114 'r']
  },
  jointree = FromExpr = {
    fromlist = List with 1 elements = {
      0 = RangeTblRef: 1
    },
    quals = SubLink[subLinkType: ROWCOMPARE_SUBLINK, subLinkId: 0] = {
      testexpr = RowCompareExpr[rctype: ROWCOMPARE_LT] = {
        opnos = OidList with 2 elements = {97, 97},
        opfamilies = OidList with 2 elements = {1976, 1976},
        inputcollids = OidList with 2 elements = {0, 0},
        largs = List with 2 elements = {
          0 = ta.a,
          1 = ta.b
        },
        rargs = List with 2 elements = {
          0 = Param[paramkind: PARAM_SUBLINK, paramid: 1, paramtype: 23, paramtypmod: -1, paramcollid: 0],
          1 = Param[paramkind: PARAM_SUBLINK, paramid: 2, paramtype: 23, paramtypmod: -1, paramcollid: 0]
        }
      },
      operName = List with 1 elements = {
        0 = <
      },
      subselect = CMD_SELECT = {
        rtable = List with 1 elements = {
          0 = RangeTblEntry: [kind: RTE_RELATION     , alias: 'tb'             , relid:    24599, relkind: 114 'r']
        },
        jointree = FromExpr = {
          fromlist = List with 1 elements = {
            0 = RangeTblRef: 1
          },
          quals = (ta.a = ta.a)
        },
        targetList = List with 2 elements = {
          0 = "?column?" = {(ta.a + 1)},
          1 = "b" = {ta.b}
        }
      }
    }
  },
  targetList = List with 2 elements = {
    0 = "a" = {ta.a},
    1 = "b" = {ta.b}
  }
}


```