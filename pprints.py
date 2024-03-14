from collections.abc import Sequence
import gdb
import string

verbose = False
planTop = True

PlanNodes = ['Result', 'Repeat', 'ModifyTable','Append', 'Sequence', 'Motion', 
        'AOCSScan', 'BitmapAnd', 'BitmapOr', 'Scan', 'SeqScan', 'TableScan',
        'IndexScan', 'DynamicIndexScan', 'BitmapIndexScan',
        'BitmapHeapScan', 'BitmapAppendOnlyScan', 'BitmapTableScan',
        'DynamicTableScan', 'TidScan', 'SubqueryScan', 'FunctionScan',
        'TableFunctionScan', 'ValuesScan', 'ExternalScan', 'AppendOnlyScan',
        'Join', 'NestLoop', 'MergeJoin', 'HashJoin', 'ShareInputScan',
        'Material', 'Sort', 'Agg', 'Window', 'Unique', 'Hash', 'SetOp',
                'Limit', 'DML', 'SplitUpdate', 'AssertOp', 'RowTrigger',
                'PartitionSelector', 'ExecNodes', 'RemoteQuery' ]

PathNodes = ['Path', 'AppendOnlyPath', 'AOCSPath', 'ExternalPath', 'PartitionSelectorPath',
             'IndexPath', 'BitmapHeapPath', 'BitmapAndPath', 'BitmapOrPath', 'TidPath',
             'CdbMotionPath', 'ForeignPath', 'AppendPath', 'MergeAppendPath', 'ResultPath',
             'HashPath', 'MergePath', 'MaterialPath', 'NestPath', 'JoinPath', 'UniquePath',
             'RemoteQueryPath'] 

rtes = {}
rteindex = 0

outer_tlist = None
inner_tlist = None

def format_plan_tree(tree, indent=0):
    'formats a plan (sub)tree, with custom indentation'
    # if the pointer is NULL, just return (null) string
    global verbose
    global planTop
    global outer_tlist
    global inner_tlist
    if (str(tree) == '0x0'):
        return '-> (NULL)'

    node_extra = ''
    retval = ''
    scan_rte = ''
    type = format_type(tree['type'])
    if is_a(tree, 'Scan') or is_a(tree, 'SeqScan') or is_a(tree, 'TableScan') or is_a(tree, 'IndexScan') or is_a(tree, 'FunctionScan'):
        type = format_type(tree['type'])
        scan = cast(tree, 'Scan')
        node_extra += '<scanrelid=%(scanrelid)s' % {
            'scanrelid': scan['scanrelid'],
        }
        if is_a(tree, 'SeqScan'):
            type = 'Seq Scan'
            rindex = int(scan['scanrelid']) - 1
            rte = rtes[rindex]
            rte = cast(rte, 'RangeTblEntry')
            scan_rte += ' on %(rel)s' % {'rel': getchars(rte['relname'], False)}

        if is_a(tree, 'IndexScan'):
            indexscan = cast(tree, 'IndexScan')
            node_extra += ' indexid=%(indexid)s indexorderdir=%(indexorderdir)s' % {
                'indexid': indexscan['indexid'],
                'indexorderdir': indexscan['indexorderdir']
            }

        if is_a(tree, 'FunctionScan'):
            functionscan = cast(tree, 'FunctionScan')
            node_extra += ' funcordinality=%s' % functionscan['funcordinality']

        node_extra += '>'

    if is_a(tree, 'HashJoin') or is_a(tree, 'Join') or is_a(tree, 'NestLoop') or is_a(tree, 'MergeJoin'):
        join = cast(tree, 'Join')

        if str(join['jointype']) == 'JOIN_INNER':
            type = 'Inner'
        elif str(join['jointype']) == 'JOIN_LEFT':
            type = 'Left'
        elif str(join['jointype']) == 'JOIN_FULL':
            type = 'Full'
        elif str(join['jointype']) == 'JOIN_RIGHT':
            type = 'Right'
        elif str(join['jointype']) == 'JOIN_SEMI':
            type = 'Semi'
        elif str(join['jointype']) == 'JOIN_ANTI':
            type = 'Anti'


        if is_a(tree, 'HashJoin'):
            type = 'Hash ' + type
        elif is_a(tree, 'NestLoop'):
            type = 'NestLoop ' + type
        elif is_a(tree, 'MergeJoin'):
            type = 'Merge ' + type

        type += ' Join'

        node_extra += '<jointype=%(jointype)s>' % {
            'jointype': join['jointype'],
        }

    if is_a(tree, 'Hash'):
        type = format_type(tree['type'])
        hash = cast(tree, 'Hash')
        node_extra += '<skewTable=%(skewTable)s skewColumn=%(skewColumn)s skewInherit=%(skewInherit)s>' %{
            'skewTable': hash['skewTable'],
            'skewColumn': hash['skewColumn'],
            'skewInherit': (int(hash['skewInherit']) == 1),
        }

    if is_a(tree, 'Sort'):
        type = format_type(tree['type'])
        sort = cast(tree, 'Sort')
        node_extra += '<numCols=%(numCols)s>' % {
            'numCols': sort['numCols']
        }

    if is_a(tree, 'Agg'):
        agg = cast(tree, 'Agg')
        if str(agg['aggstrategy']) == 'AGG_PLAIN':
            type = 'Aggregate'
        elif str(agg['aggstrategy']) == 'AGG_SORTED':
            type = 'GroupAggregate'
        elif str(agg['aggstrategy']) == 'AGG_HASHED':
            type = 'HashAggregate'
        elif str(agg['aggstrategy']) == 'AGG_MIXED':
            type = 'MixedAggregate'
        elif str(agg['aggstrategy']) == 'AGG_BATCH_HASH':
            type = 'BatchHashAggregate'

        node_extra += '<aggstrategy=%(aggstrategy)s numCols=%(numCols)s numGroups=%(numGroups)s aggParams=%(aggParams)s>' % {
            'aggstrategy': agg['aggstrategy'],
            'numCols': agg['numCols'],
            'numGroups': agg['numGroups'],
            'aggParams': format_bitmapset(agg['aggParams']),
        }

    if is_a(tree, 'SetOp'):
        type = format_type(tree['type'])
        setop = cast(tree, 'SetOp')
        node_extra += '<cmd=%(cmd)s strategy=%(strategy)s numCols=%(numCols)s flagColIdx=%(flagColIdx)s firstFlag=%(firstFlag)s numGroups=%(numGroups)s>' % {
            'cmd': setop['cmd'],
            'strategy': setop['strategy'],
            'numCols': setop['numCols'],
            'flagColIdx': setop['flagColIdx'],
            'firstFlag': setop['firstFlag'],
            'numGroups': setop['numGroups']
        }

    if is_a(tree, 'Limit'):
        type = format_type(tree['type'])
        limit = cast(tree, 'Limit')
        node_extra += '<limitOffset=%(limitOffset)s limitCount=%(limitCount)s>' % {
            'limitOffset': format_node(limit['limitOffset']),
            'limitCount': format_node(limit['limitCount'])
        }

    if is_a(tree, 'Group'):
        type = format_type(tree['type'])
        group = cast(tree, 'Group')
        node_extra += '<numCols=%(numCols)s>' % {
            'numCols': group['numCols']
        }

    if is_a(tree, 'ClusterReduce'):
        type = format_type(tree['type'])
        clusterReduce = cast(tree, 'ClusterReduce')
        node_extra += '<reduce=%(reduce_oids)s>' % {
            'reduce_oids': format_node(clusterReduce['reduce_oids'])
        }

    if planTop:
        retval += '''\n'''

    planTop = False
    retval += '''-> %(type)s%(scan_rte)s (cost=%(startup).3f...%(total).3f rows=%(rows).0f width=%(width)s)''' % {
        'type': type,    # type of the Node
        'scan_rte': scan_rte,
        'startup': float(tree['startup_cost']),    # startup cost
        'total': float(tree['total_cost']),    # total cost
        'rows': float(tree['plan_rows']),    # number of rows
        'width': str(tree['plan_width']),    # tuple width (no header)
        # 'plan_node_id': str(tree['plan_node_id']),
    }

    if verbose and node_extra != '':
        retval += add_indent(node_extra, 1)

    if verbose:
      retval += format_optional_node_list(tree, 'targetlist')

    if is_a(tree, 'IndexScan'):
        retval += format_optional_node_list(tree, 'indexqual', 'IndexScan')

    # These are fields can be part of any node
    retval += format_optional_node_list(tree, 'initPlan')
    # retval += format_optional_node_list(tree, 'qual')

    if is_a(tree, 'Result'):
        result = cast(tree, 'Result')
        if str(result['resconstantqual']) != '0x0':
            # Resconstant qual might be a list
            if is_a(result['resconstantqual'], 'List'):
                resconstantqual = cast(result['resconstantqual'], 'List')
            else:
                resconstantqual = result['resconstantqual']

            retval += add_indent('[resconstantqual]', 1, True)
            retval += '\n'
            retval += format_node(resconstantqual, 2)


    if is_a(tree, 'HashJoin') or is_a(tree, 'Join') or is_a(tree, 'NestLoop') or is_a(tree, 'MergeJoin'):
        # All join nodes can have this field
        retval += format_optional_node_list(tree, 'joinqual', 'Join')

        if is_a(tree, 'HashJoin'):
            retval += add_indent('Hash Cond:', 1, True)
            node = cast(tree, 'HashJoin')
            outer_tlist = tree['lefttree']['targetlist']
            inner_tlist = tree['righttree']['targetlist']
            retval += format_node_list(node['hashclauses'], 0, False)

    if is_a(tree, 'Sort'):
        append = cast(tree, 'Sort')
        numcols = int(append['numCols'])

        retval += add_indent('Sort Key:', 1, True)

        index = ''
        for col in range(0,numcols):
            index += ' sortColIdx=%(sortColIdx)s' % {
                'sortColIdx': append['sortColIdx'][col],
            }
            if col < numcols-1:
                index += ','

        retval += add_indent(index, 0, False)

    if is_a(tree, 'Group'):
        group = cast(tree, 'Group')
        numcols = int(group['numCols'])
        retval += add_indent('Group Key:', 1, True)
        index = ''
        for col in range(0, numcols):
          index += ' grpColIdx=%(grpColIdx)s' % {
                'grpColIdx': group['grpColIdx'][col]
            }
          if col < numcols-1:
                index += ','

        retval += add_indent(index, 0, False)

    if is_a(tree, 'Agg'):
        agg = cast(tree, 'Agg')
        numcols = int(agg['numCols'])

        if (numcols >= 1):
            retval += add_indent('Group Key:', 1, True)

            index = ''
            for col in range(0,numcols):
                index += ' grpColIdx=%(grpColIdx)s' % {
                    'grpColIdx': agg['grpColIdx'][col]
                }
                if col < numcols-1:
                    index += ','

            retval += add_indent(index, 0, False)
        if str(tree['qual']) != '0x0':
            retval += add_indent('Filter: ', 1, True)
            retval += format_node_list(tree['qual'], 0, False)

    if is_a(tree, 'SeqScan'):
        if str(tree['qual']) != '0x0':
            retval += add_indent('Filter: ', 1, True)
            retval += format_node_list(tree['qual'], 0, False)

    if is_a(tree, 'SetOp'):
        setop = cast(tree, 'SetOp')
        numcols = int(setop['numCols'])

        retval += add_indent('[operators]', 1, True)

        index = ''
        for col in range(0,numcols):
            index += '[dupColIdx=%(dupColIdx)s dupOperator=%(dupOperator)s]' % {
                'dupColIdx': setop['dupColIdx'][col],
                'dupOperator': setop['dupOperators'][col],
            }
            if col < numcols-1:
                index += '\n'

        retval += add_indent(index, 2, True)

    if is_a(tree, 'FunctionScan'):
        retval += format_optional_node_list(tree, 'functions', 'FunctionScan')

    # format Append subplans
    if is_a(tree, 'Append'):
        append = cast(tree, 'Append')
        retval += '\n\t%s' % format_appendplan_list(append['appendplans'], 0)
    elif is_a(tree, 'SubqueryScan'):
        subquery = cast(tree, 'SubqueryScan')
        retval += '\n\t%s' % format_plan_tree(subquery['subplan'], 0)
    elif is_a(tree, 'ModifyTable'):
        modifytable= cast(tree, 'ModifyTable')
        retval += '\n\t%(plans)s' % format_appendplan_list(modifytable['plans'], 0)
    else:
        # format all the important fields (similarly to EXPLAIN)
        if str(tree['lefttree']) != '0x0': retval += '\n%s' % format_plan_tree(tree['lefttree'], 0)
        if str(tree['righttree']) != '0x0': retval += '\n%s' % format_plan_tree(tree['righttree'], 0)

    return add_indent(retval, indent + 1)



def format_optional_node_list(node, fieldname, cast_to=None, skip_tag=False, newLine=True, indent=1):
    if cast_to != None:
        node = cast(node, cast_to)

    retval = ''
    indent_add = 0
    if str(node[fieldname]) != '0x0':
        if skip_tag == False:
            retval += add_indent('[%s]' % fieldname, indent, True)
            indent_add = 1

        retval += '%s' % format_node_list(node[fieldname], indent + indent_add, newLine)
    return retval

def format_optional_node_field(node, fieldname, cast_to=None, skip_tag=False, indent=1):
    if cast_to != None:
        node = cast(node, cast_to)

    if str(node[fieldname]) != '0x0':
        if skip_tag == True:
            return add_indent('%s' % format_node(node[fieldname]), indent, True)
        else:
            return add_indent('[%s] %s' % (fieldname, format_node(node[fieldname])), indent, True)
    return ''

def format_restrict_info(node, indent=0):
    retval = 'RestrictInfo [is_pushed_down=%(is_pushed_down)s can_join=%(can_join)s outerjoin_delayed=%(outerjoin_delayed)s]' % {
        'push_down': (int(node['is_pushed_down']) == 1),
        'can_join': (int(node['can_join']) == 1),
        'outerjoin_delayed': (int(node['outerjoin_delayed']) == 1)
    }
    retval += format_optional_node_field(node, 'clause', skip_tag=True)
    retval += format_optional_node_field(node, 'orclause', skip_tag=True)

    return add_indent(retval, indent)

def format_query_info(node, indent=0):
    retval = 'Query [commandType=%(commandType)s querySource=%(querySource)s queryId=%(queryId)s canSetTag=%(canSetTag)s resultRelation=%(resultRelation)s]' % {
        'commandType': node['commandType'],
        'querySource': node['querySource'],
        'queryId': node['queryId'],
        'canSetTag': (int(node['canSetTag']) == 1),
        'resultRelation': node['resultRelation'],
    }
    retval += format_optional_node_field(node, 'utilityStmt')
    retval += format_optional_node_list(node, 'cteList')
    retval += format_optional_node_list(node, 'rtable')
    retval += format_optional_node_field(node, 'jointree')
    retval += format_optional_node_list(node, 'targetList')
    retval += format_optional_node_list(node, 'withCheckOptions')
    retval += format_optional_node_list(node, 'returningList')
    retval += format_optional_node_list(node, 'groupClause')
    retval += format_optional_node_field(node, 'havingQual')
    retval += format_optional_node_list(node, 'windowClause')
    retval += format_optional_node_list(node, 'distinctClause')
    retval += format_optional_node_list(node, 'sortClause')
    # retval += format_optional_node_list(node, 'scatterClause')
    retval += format_optional_node_field(node, 'limitOffset')
    retval += format_optional_node_field(node, 'limitCount')
    retval += format_optional_node_list(node, 'rowMarks')
    retval += format_optional_node_field(node, 'setOperations')
    retval += format_optional_node_list(node, 'constraintDeps')
    # retval += format_optional_node_field(node, 'intoPolicy')

    return add_indent(retval, 0)

def format_execnode_info(node, indent=0):
    retval = 'ExecNodes [baselocatortype=%(baselocatortype)s en_relid=%(en_relid)s en_funcid=%(en_funcid)s]' % {
        # 'RelationAccessType': node['RelationAccessType'],
        'baselocatortype': node['baselocatortype'],
        'en_relid': (int(node['en_relid']) == 1),
        'en_funcid': (int(node['en_funcid']) == 1),
    }
    retval += format_optional_node_list(node, 'en_expr')
    retval += format_optional_node_list(node, 'en_dist_vars')
    retval += '\n\t[nodeids]'
    retval += format_oid_list(node['nodeids'])

    return add_indent(retval, indent)

def format_appendplan_list(lst, indent):
    retval = format_node_list(lst, indent, True)
    return add_indent(retval, indent + 1)

def format_alter_table_cmd(node, indent=0):
    retval = '''AlterTableCmd (subtype=%(subtype)s name=%(name)s behavior=%(behavior)s)''' % {
        'subtype': node['subtype'],
        'name': getchars(node['name']),
        'behavior': node['behavior'],
    }

    retval += format_optional_node_field(node, 'def')
    retval += format_optional_node_field(node, 'transform')
    retval += format_optional_node_list(node, 'partoids')

    return add_indent(retval, indent)

def format_alter_partition_cmd(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'AlterPartitionCmd (location=%(location)s)' % {
        'location': node['location']
    }

    retval += format_optional_node_field(node, 'partid')
    retval += format_optional_node_field(node, 'arg1')
    retval += format_optional_node_field(node, 'arg2')

    return add_indent(retval, indent)

def format_partition_cmd(node, indent=0):
    retval = 'PartitionCmd' % {
    }

    retval += format_optional_node_field(node, 'name')
    retval += format_optional_node_field(node, 'bound')

    return add_indent(retval, indent)

def format_alter_partition_id(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'AlterPartitionId (idtype=%(idtype)s location=%(location)s)' % {
        'idtype': node['idtype'],
        'location': node['location']
    }

    if (str(node['partiddef']) != '0x0'):
        if is_a(node['partiddef'], 'List'):
            partdef = '\n[partiddef]\n'
            partdef += add_indent('%s' % format_node_list(cast(node['partiddef'], 'List'), 0, True),1)
            retval += add_indent(partdef, 1)
        elif is_a(node['partiddef'], 'String'):
            partdef = '\n[partiddef]'
            partdef += add_indent('String: %s' % node['partiddef'], 1)
            retval += add_indent(partdef, 1)

    return add_indent(retval, indent)

def format_pg_part_rule(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'PgPartRule (partIdStr=%(partIdStr)s isName=%(isName)s topRuleRank=%(topRuleRank)s relname=%(relname)s)' % {
        'partIdStr': node['partIdStr'],
        'isName': (int(node['isName']) == 1),
        'topRuleRank': node['topRuleRank'],
        'relname': node['relname']
    }

    retval += format_optional_node_field(node, 'pNode')
    retval += format_optional_node_field(node, 'topRule')

    return add_indent(retval, indent)

def format_partition_node(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'PartitionNode'


    retval += format_optional_node_field(node, 'part')
    retval += format_optional_node_field(node, 'default_part')
    retval += format_optional_node_list(node, 'rules')

    return add_indent(retval, indent)

def format_partition_elem(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'PartitionElem (partName=%(partName)s isDefault=%(isDefault)s AddPartDesc=%(AddPartDesc)s partno=%(partno)s rrand=%(rrand)s location=%(location)s)' % {
        'partName': node['partName'],
        'isDefault': (int(node['isDefault']) == 1),
        'AddPartDesc': node['AddPartDesc'],
        'partno': node['partno'],
        'rrand': node['rrand'],
        'location': node['location']
    }

    retval += format_optional_node_field(node, 'boundSpec')
    retval += format_optional_node_field(node, 'subSpec')
    retval += format_optional_node_field(node, 'storeAttr')
    retval += format_optional_node_list(node, 'colencs')

    return add_indent(retval, indent)

def format_index_elem(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'IndexElem [name=%(name)s indexcolname=%(indexcolname)s ordering=%(ordering)s nulls_ordering=%(nulls_ordering)s]' % {
        'name': getchars(node['name']),
        'indexcolname': getchars(node['indexcolname']),
        'ordering': node['ordering'],
        'nulls_ordering': node['nulls_ordering'],
    }

    retval += format_optional_node_field(node, 'expr')
    retval += format_optional_node_list(node, 'collation')
    retval += format_optional_node_field(node, 'opclass')

    return add_indent(retval, indent)

def format_path(node, indent=0):
    extra = ''
    retval = '%(type)s [pathtype=%(pathtype)s parent=%(parent)s rows=%(rows)s startup_cost=%(startup_cost)s total_cost=%(total_cost)s' % {
        'type': format_type(node['type']),    # type of the Node
        'pathtype': node['pathtype'],
        'parent': node['parent'],
        'rows': node['rows'],
        'startup_cost': node['startup_cost'],
        'total_cost': node['total_cost'],
    }

    if is_a(node, 'JoinPath') or is_a(node, 'NestPath') or is_a(node, 'MergePath') or is_a(node, 'HashPath'):
        joinpath = cast(node, 'JoinPath')
        extra = ' jointype=%s' % (joinpath['jointype'])

    retval += '%s]' % (extra)


    retval += format_optional_node_field(node, 'parent')
    retval += format_optional_node_field(node, 'param_info')
    retval += format_optional_node_list(node, 'pathkeys', newLine=False)

    if is_a(node, 'JoinPath') or is_a(node, 'NestPath') or is_a(node, 'MergePath') or is_a(node, 'HashPath'):
        joinpath = cast(node, 'JoinPath')
        retval += format_optional_node_field(joinpath, 'outerjoinpath')
        retval += format_optional_node_field(joinpath, 'innerjoinpath')
        retval += format_optional_node_list(joinpath, 'joinrestrictinfo')

    if is_a(node, 'MaterialPath'):
        retval += format_optional_node_field(node, 'subpath', 'MaterialPath')

    if is_a(node, 'UniquePath'):
        retval += format_optional_node_field(node, 'subpath', 'UniquePath')

    if is_a(node, 'RemoteQueryPath'):
        remoteQueryPath = cast(node, 'RemoteQueryPath')
        retval += format_optional_node_field(remoteQueryPath, 'rqpath_en')
        retval += format_optional_node_field(remoteQueryPath, 'leftpath')
        retval += format_optional_node_field(remoteQueryPath, 'rightpath')

    return add_indent(retval, indent)

def format_partition_bound_spec(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'PartitionBoundSpec (pWithTnameStr=%(pWithTnameStr)s location=%(location)s)' % {
        'pWithTnameStr': node['pWithTnameStr'],
        'location': node['location'],
    }

    retval += format_optional_node_field(node, 'partStart')
    retval += format_optional_node_field(node, 'partEnd')
    retval += format_optional_node_field(node, 'partEvery')
    retval += format_optional_node_list(node, 'everyGenList', newLine=False)

    return add_indent(retval, indent)

def format_partition_values_spec(node, indent=0):
    retval = 'PartitionValuesSpec [location=%(location)s]' % {
        'location': node['location'],
    }

    retval += format_optional_node_list(node, 'partValues')

    return add_indent(retval, indent)

def format_partition_range_item(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'PartitionRangeItem (partedge=%(partedge)s everycount=%(everycount)s location=%(location)s)' % {
        'partedge': node['partedge'],
        'everycount': node['everycount'],
        'location': node['location'],
    }

    retval += format_optional_node_list(node, 'partRangeVal')

    return add_indent(retval, indent)

def format_partition(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'Partition [partid=%(partid)s parrelid=%(parrelid)s parkind=%(parkind)s parlevel=%(parlevel)s paristemplate=%(paristemplate)s parnatts=%(parnatts)s paratts=%(paratts)s parclass=%(parclass)s]' % {
        'partid': node['partid'],
        'parrelid': node['parrelid'],
        'parkind': node['parkind'],
        'parlevel': node['parlevel'],
        'paristemplate': (int(node['paristemplate']) == 1),
        'parnatts': node['parnatts'],
        'paratts': node['paratts'],
        'parclass': node['parclass']
    }

    return add_indent(retval, indent)

def format_type_cast(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'TypeCast [location=%(location)s]' % {
        'location': node['location'],
    }

    retval += format_optional_node_field(node, 'typeName')
    retval += format_optional_node_field(node, 'arg')

    return add_indent(retval, indent)

def format_cdb_process(node, indent=0):
    retval = 'CdbProcess [listenerAddr=%(listenerAddr)s listenerPort=%(listenerPort)s pid=%(pid)s contentid=%(contentid)s]' % {
        'listenerAddr': getchars(node['listenerAddr']),
        'listenerPort': node['listenerPort'],
        'pid': node['pid'],
        'contentid': node['contentid'],
    }

    return add_indent(retval, indent)

def format_def_elem(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'DefElem [defnamespace=%(defnamespace)s defname=%(defname)s defaction=%(defaction)s]' % {
        'defnamespace': node['defnamespace'],
        'defname': node['defname'],
        'defaction': node['defaction'],
    }

    retval += format_optional_node_field(node, 'arg')

    return add_indent(retval, indent)

def format_type_name(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'TypeName [typeOid=%(typeOid)s setof=%(setof)s pct_type=%(pct_type)s typemod=%(typemod)s location=%(location)s]' % {
        'typeOid': node['typeOid'],
        'setof': (int(node['setof']) == 1),
        'pct_type': (int(node['pct_type']) == 1),
        'typemod': node['typemod'],
        'location': node['location'],
    }

    retval += format_optional_node_field(node, 'names')
    retval += format_optional_node_field(node, 'typmods')
    retval += format_optional_node_field(node, 'arrayBounds')

    return add_indent(retval, indent)

def format_param(node, indent=0):
    if (str(node) == '0x0'):
        return '(NIL)'

    retval = 'Param (paramkind=%(paramkind)s paramid=%(paramid)s paramtype=%(paramtype)s paramtypmod=%(paramtypmod)s location=%(location)s)' % {
        'paramkind': node['paramkind'],
        'paramid': node['paramid'],
        'paramtype': node['paramtype'],
        'paramtypmod': node['paramtypmod'],
        'location': node['location']
    }

    return add_indent(retval, indent)

def format_subplan(node, indent=0):
    retval = 'SubPlan [subLinkType=%(subLinkType)s plan_id=%(plan_id)s plan_name=%(plan_name)s]' % {
        'subLinkType': node['subLinkType'],
        'plan_id': node['plan_id'],
        'plan_name': node['plan_name'],
    }

    retval += format_optional_node_field(node, 'testexpr')
    # retval += format_optional_node_list(node, 'paramIds')
    retval += format_optional_node_list(node, 'args')

    return add_indent(retval, indent)


def format_partition_rule(node, indent=0):
    retval = '''PartitionRule (parruleid=%(parruleid)s paroid=%(paroid)s parchildrelid=%(parchildrelid)s parparentoid=%(parparentoid)s parisdefault=%(parisdefault)s parname=%(parname)s parruleord=%(parruleord)s partemplatespaceId=%(partemplatespaceId)s)''' % {
        'parruleid': node['parruleid'],
        'paroid': node['paroid'],
        'parchildrelid': node['parchildrelid'],
        'parparentoid': node['parparentoid'],
        'parisdefault': (int(node['parisdefault']) == 1),
        'parname': node['parname'],
        'parruleord': node['parruleord'],
        'partemplatespaceId': node['partemplatespaceId'],
    }
    if (str(node['parrangestart']) != '0x0'):
        retval += '\n\t[parrangestart parrangestartincl=%(parrangestartincl)s] %(parrangestart)s' % {
            'parrangestart': format_node_list(cast(node['parrangestart'], 'List'), 1, True),
            'parrangestartincl': (int(node['parrangestartincl']) == 1),
        }

    if (str(node['parrangeend']) != '0x0'):
        retval += '\n\t[parrangeend parrangeendincl=%(parrangeendincl)s] %(parrangeend)s' % {
            'parrangeend': format_node_list(cast(node['parrangeend'], 'List'), 0, True),
            'parrangeendincl': (int(node['parrangeendincl']) == 1),
        }

    retval += format_optional_node_list(node, 'parrangeevery')
    retval += format_optional_node_list(node, 'parlistvalues')
    retval += format_optional_node_list(node, 'parreloptions')
    retval += format_optional_node_field(node, 'children')

    return add_indent(retval, indent)

def format_type(t, indent=0):
    'strip the leading T_ from the node type tag'

    t = str(t)

    if t.startswith('T_'):
        t = t[2:]

    return add_indent(t, indent)


def format_int_list(lst, indent=0):
    'format list containing integer values directly (not warapped in Node)'

    # handle NULL pointer (for List we return NIL
    if (str(lst) == '0x0'):
        return '(NIL)'

    # we'll collect the formatted items into a Python list
    tlist = []
    item = lst['head']

    # walk the list until we reach the last item
    while str(item) != '0x0':

        # get item from the list and just grab 'int_value as int'
        tlist.append(int(item['data']['int_value']))

        # next item
        item = item['next']

    return add_indent(str(tlist), indent)


def format_oid_list(lst, indent=0):
    'format list containing Oid values directly (not warapped in Node)'

    # handle NULL pointer (for List we return NIL)
    if (str(lst) == '0x0'):
        return '(NIL)'

    # we'll collect the formatted items into a Python list
    tlist = []
    try:
        item = lst['head']

        # walk the list until we reach the last item
        while str(item) != '0x0':

            # get item from the list and just grab 'oid_value as int'
            tlist.append(int(item['data']['oid_value']))

            # next item
            item = item['next']
    except:
        print("error format_oid_list")
        # for col in range(0, lst['length']):
        #     element = lst['elements'][col]
        #     tlist.append(int(element['oid_value']))

    return add_indent(str(tlist), indent)


def format_node_list(lst, indent=0, newline=False):
    'format list containing Node values'

    # handle NULL pointer (for List we return NIL)
    if (str(lst) == '0x0'):
        return add_indent('(NULL)', indent)

    # we'll collect the formatted items into a Python list
    tlist = []

    len = int(lst['length'])

    try:
        i = 0
        # walk the list until we reach the last item
        while i < len:

            item = lst['head']['data']
            i += 1
            # we assume the list contains Node instances, so grab a reference
            # and cast it to (Node*)
            node = cast(item['ptr_value'], 'Node')

            # append the formatted Node to the result list
            tlist.append(str(i) + ': \t' + format_node(node))

    except:
        print("error format_node_list")

    retval = str(tlist)
    if newline:
        retval = "\n".join([str(t) for t in tlist])

    return  add_indent(retval, indent)


def format_char(value):
    '''convert the 'value' into a single-character string (ugly, maybe there's a better way'''

    str_val = str(value.cast(gdb.lookup_type('char')))

    # remove the quotes (start/end)
    return str_val.split(' ')[1][1:-1]


def format_bitmapset(bitmapset):
    if (str(bitmapset) == '0x0'):
        return '0x0'

    num_words = int(bitmapset['nwords'])
    retval = '0x'
    for word in reversed(range(num_words)):
        retval += '%08x' % int(bitmapset['words'][word])
    return retval


def format_node_array(array, start_idx, length, indent=0):

    items = []
    for i in range(start_idx, start_idx + length - 1):
        items.append(str(i) + " => " + format_node(array[i]))

    return add_indent(("\n".join(items)), indent)

def format_alias(node):
    return getchars(node['aliasname'])


def format_node(node, indent=0, pretty = False):
    'format a single Node instance (only selected Node types supported)'
    global verbose
    global planTop

    if str(node) == '0x0':
        return add_indent('(NULL)', indent)

    retval = ''
    type_str = str(node['type'])

    if is_a(node, 'TargetEntry'):
        node = cast(node, 'TargetEntry')

        retval = format_target_entry(node)

    elif is_a(node, 'ClusterReduce'):
        node = cast(node, 'Plan')
        planTop = True
        retval = format_plan_tree(node)

    elif is_a(node, 'Alias'):
        node = cast(node, 'Alias')

        retval = format_alias(node)

    elif is_a(node, 'SortGroupClause'):
        node = cast(node, 'SortGroupClause')

        retval = format_sort_group_clause(node)

    elif is_a(node, 'TableLikeClause'):
        node = cast(node, 'TableLikeClause')

        retval = format_table_like_clause(node)

    elif is_a(node, 'Var'):
        node = cast(node, 'Var')

        retval = format_var(node)

    elif is_a(node, 'Const'):
        node = cast(node, 'Const')

        retval = format_const(node)

    elif is_a(node, 'Aggref'):
        node = cast(node, 'Aggref')

        retval = format_aggref(node)

    elif is_a(node, 'A_Expr'):
        node = cast(node, 'A_Expr')

        retval = format_a_expr(node)

    elif is_a(node, 'A_Const'):
        node = cast(node, 'A_Const')

        retval = format_a_const(node)

    elif is_a(node, 'CaseExpr'):
        node = cast(node, 'CaseExpr')

        retval = format_case_expr(node)

    elif is_a(node, 'CoalesceExpr'):
        node = cast(node, 'CoalesceExpr')

        retval = format_coalesce_expr(node)

    elif is_a(node, 'CaseWhen'):
        node = cast(node, 'CaseWhen')

        retval = format_case_when(node)

    elif is_a(node, 'RangeTblRef'):
        node = cast(node, 'RangeTblRef')

        retval = 'RangeTblRef (rtindex=%d)' % (int(node['rtindex']), )

    elif is_a(node, 'RelOptInfo'):
        node = cast(node, 'RelOptInfo')

        retval = format_reloptinfo(node)

    elif is_a(node, 'RangeTblEntry'):
        node = cast(node, 'RangeTblEntry')

        retval = format_rte(node)

    elif is_a(node, 'GenericExprState'):
        node = cast(node, 'GenericExprState')

        retval = format_generic_expr_state(node)

    elif is_a(node, 'PlannerInfo'):
        retval = format_planner_info(node)

    elif is_a(node, 'PlannedStmt'):
        node = cast(node, 'PlannedStmt')

        retval = format_planned_stmt(node)

    elif is_a(node, 'CreateStmt'):
        node = cast(node, 'CreateStmt')

        retval = format_create_stmt(node)

    elif is_a(node, 'IndexStmt'):
        node = cast(node, 'IndexStmt')

        retval = format_index_stmt(node)

    elif is_a(node, 'AlterTableStmt'):
        node = cast(node, 'AlterTableStmt')

        retval = format_alter_table_stmt(node)

    elif is_a(node, 'RangeVar'):
        node = cast(node, 'RangeVar')

        retval = format_range_var(node)

    elif is_a(node, 'List'):
        node = cast(node, 'List')

        retval = format_node_list(node, 0, True)

    elif is_a(node, 'Plan'):
        retval = format_plan_tree(node)

    elif is_a(node, 'RestrictInfo'):
        node = cast(node, 'RestrictInfo')

        retval = format_restrict_info(node)

    elif is_a(node, 'OpExpr'):
        node = cast(node, 'OpExpr')

        retval = format_op_expr(node)

    elif is_a(node, 'NullIfExpr'):
        node = cast(node, 'OpExpr')

        retval = format_op_expr(node)

    elif is_a(node, 'DistinctExpr'):
        node = cast(node, 'OpExpr')

        retval = format_op_expr(node)

    elif is_a(node, 'FuncExpr'):
        node = cast(node, 'FuncExpr')

        retval = format_func_expr(node)

    elif is_a(node, 'RelabelType'):
        node = cast(node, 'RelabelType')

        retval = format_relabel_type(node)

    elif is_a(node, 'CoerceViaIO'):
        node = cast(node, 'CoerceViaIO')

        retval = format_coerce_via_io(node)

    elif is_a(node, 'ScalarArrayOpExpr'):
        node = cast(node, 'ScalarArrayOpExpr')

        retval = format_scalar_array_op_expr(node)

    elif is_a(node, 'BoolExpr'):
        node = cast(node, 'BoolExpr')

        retval = format_bool_expr(node)

    elif is_a(node, 'SubLink'):
        node = cast(node, 'SubLink')

        retval = format_sublink(node)

    elif is_a(node, 'FromExpr'):
        node = cast(node, 'FromExpr')

        retval = format_from_expr(node)

    elif is_a(node, 'JoinExpr'):
        node = cast(node, 'JoinExpr')

        retval = format_join_expr(node)

    elif is_a(node, 'AlterTableCmd'):
        node = cast(node, 'AlterTableCmd')

        retval = format_alter_table_cmd(node)

    elif is_a(node, 'AlterPartitionCmd'):
        node = cast(node, 'AlterPartitionCmd')

        retval = format_alter_partition_cmd(node)

    elif is_a(node, 'PartitionCmd'):
        node = cast(node, 'PartitionCmd')

        retval = format_partition_cmd(node)

    elif is_a(node, 'AlterPartitionId'):
        node = cast(node, 'AlterPartitionId')

        retval = format_alter_partition_id(node)

    elif is_a(node, 'PgPartRule'):
        node = cast(node, 'PgPartRule')

        retval = format_pg_part_rule(node)

    elif is_a(node, 'PartitionNode'):
        node = cast(node, 'PartitionNode')

        retval = format_partition_node(node)

    elif is_a(node, 'PartitionElem'):
        node = cast(node, 'PartitionElem')

        retval = format_partition_elem(node)

    elif is_a(node, 'IndexElem'):
        node = cast(node, 'IndexElem')

        retval = format_index_elem(node)

    elif is_a(node, 'Path'):
        node = cast(node, 'Path')

        retval = format_path(node)

    elif is_a(node, 'PartitionBoundSpec'):
        node = cast(node, 'PartitionBoundSpec')

        retval = format_partition_bound_spec(node)

    elif is_a(node, 'PartitionValuesSpec'):
        node = cast(node, 'PartitionValuesSpec')

        retval = format_partition_values_spec(node)

    elif is_a(node, 'PartitionRangeItem'):
        node = cast(node, 'PartitionRangeItem')

        retval = format_partition_range_item(node)

    elif is_a(node, 'Partition'):
        node = cast(node, 'Partition')

        retval = format_partition(node)

    elif is_a(node, 'PartitionBy'):
        node = cast(node, 'PartitionBy')

        retval = format_partition_by(node)

    elif is_a(node, 'PartitionSpec'):
        node = cast(node, 'PartitionSpec')

        retval = format_partition_spec(node)

    elif is_a(node, 'Constraint'):
        node = cast(node, 'Constraint')

        retval = format_constraint(node)

    elif is_a(node, 'DefElem'):
        node = cast(node, 'DefElem')

        retval = format_def_elem(node)

    elif is_a(node, 'TypeName'):
        node = cast(node, 'TypeName')

        retval = format_type_name(node)

    elif is_a(node, 'Param'):
        node = cast(node, 'Param')

        retval = format_param(node)

    elif is_a(node, 'String'):
        node = cast(node, 'Value')

        if pretty:
            retval = getchars(node['val']['str'], False)
        else:
            retval = 'String [%s]' % getchars(node['val']['str'])

    elif is_a(node, 'SubPlan'):
        node = cast(node, 'SubPlan')

        retval = format_subplan(node)

    elif is_a(node, 'PartitionRule'):
        node = cast(node, 'PartitionRule')

        retval = format_partition_rule(node)

    elif is_a(node, 'TypeCast'):
        node = cast(node, 'TypeCast')

        retval = format_type_cast(node)

    elif is_a(node, 'CdbProcess'):
        node = cast(node, 'CdbProcess')

        retval = format_cdb_process(node)

    elif is_a(node, 'OidList'):
        retval = 'OidList: %s' % format_oid_list(node)

    elif is_a(node, 'IntList'):
        retval = 'IntList: %s' % format_int_list(node)

    elif is_a(node, 'Query'):
        node = cast(node, 'Query')

        retval = format_query_info(node)

    elif is_a(node, 'ExecNodes'):
        node = cast(node, 'ExecNodes')

        retval = format_execnode_info(node)

    # elif is_a(node, 'RemoteQueryPath'):
    #     node = cast(node, 'Path')
    #     retval = format_execnode_info(node)

    elif is_pathnode(node):
        node = cast(node, 'Path')

        retval = format_path(node)

    elif is_plannode(node):
        node = cast(node, 'Plan')

        retval = format_plan_tree(node)


    else:
        # default - just print the type name
        retval = format_type(type_str)

    return add_indent(str(retval), indent)

def is_pathnode(node):
    for nodestring in PathNodes:
        #print "testing %s against %s" % (nodestring, node.address)
        if is_a(node, nodestring):
            return True

    return False

def is_plannode(node):
    for nodestring in PlanNodes:
        if is_a(node, nodestring):
            return True

    return False

def format_planner_info(info, indent=0):

    # Query *parse;			/* the Query being planned */
    # *glob;				/* global info for current planner run */
    # Index	query_level;	/* 1 at the outermost Query */
    # struct PlannerInfo *parent_root;	/* NULL at outermost Query */
    # List	   *plan_params;	/* list of PlannerParamItems, see below */

    retval = '''rel:
%(rel)s
rte:
%(rte)s
''' % {
        'rel':
        format_node_array(info['simple_rel_array'], 1,
                          int(info['simple_rel_array_size'])),
        'rte':
        format_node_array(info['simple_rte_array'], 1,
                          int(info['simple_rel_array_size']))
    }

    return add_indent(retval, indent)


def format_planned_stmt(plan, indent=0):
    global planTop

    planTop = True
    rtables = format_node_list(plan['rtable'], 2, True)
    retval = '''          type: %(type)s
        queryId: %(qid)s
   hasReturning: %(has_returning)s
hasModifyingCTE: %(has_modify_cte)s
   relationOids: %(relation_oids)s
       planTree: %(tree)s
         rtable: \n%(rtable)s
    result rels: %(result_rels)s
   utility stmt: %(util_stmt)s
 paramExecTypes: %(paramExecTypes)s
       subplans: \n%(subplans)s''' % {
           'type': plan['commandType'],
           'qid' : plan['queryId'],
 'has_returning' : (int(plan['hasReturning']) == 1),
'has_modify_cte' : (int(plan['hasModifyingCTE']) == 1),
           'tree': format_plan_tree(plan['planTree']),
         'rtable': rtables,
  'relation_oids': format_oid_list(plan['relationOids']),
    'result_rels': format_int_list(plan['resultRelations']),
      'util_stmt': format_node(plan['utilityStmt']),
       'subplans': format_node_list(plan['subplans'], 1, True),
 'paramExecTypes': format_oid_list(plan['paramExecTypes'])
    }

    return add_indent(retval, indent)

def format_create_stmt(node, indent=0):
    retval = 'CreateStmt [oncommit=%(oncommit)s tablespacename=%(tablespacename)s if_not_exists=%(if_not_exists)s]' % {
        'oncommit': node['oncommit'],
        'tablespacename': node['tablespacename'],
        'if_not_exists': (int(node['if_not_exists']) == 1),
        }

    retval += add_indent('[relation] %s' % format_node(node['relation'], 0), 1, True)

    retval += add_indent('[tableElts] %s' % format_node_list(node['tableElts'], 0, True), 1, True)

    if (str(node['inhRelations']) != '0x0'):
        retval += add_indent('[inhRelations] %s' % format_oid_list(node['inhRelations']), 1, True)

    retval += format_optional_node_field(node, 'ofTypename')
    retval += format_optional_node_list(node, 'constraints')
    retval += format_optional_node_list(node, 'options', newLine=False)

    return add_indent(retval, indent)

def format_index_stmt(node, indent=0):
    retval = 'IndexStmt [idxname=%(idxname)s accessMethod=%(accessMethod)s tableSpace=%(tableSpace)s idxcomment=%(idxcomment)s indexOid=%(indexOid)s oldNode=%(oldNode)s unique=%(unique)s primary=%(primary)s isconstraint=%(isconstraint)s deferrable=%(deferrable)s initdeferred=%(initdeferred)s concurrent=%(concurrent)s]' % {
        'idxname': getchars(node['idxname']),
        'accessMethod': getchars(node['accessMethod']),
        'tableSpace': node['tableSpace'],
        'idxcomment': node['idxcomment'],
        'indexOid': node['indexOid'],
        'oldNode': node['oldNode'],
        'unique': (int(node['unique']) == 1),
        'primary': (int(node['primary']) == 1),
        'isconstraint': (int(node['isconstraint']) == 1),
        'deferrable': (int(node['deferrable']) == 1),
        'initdeferred': (int(node['initdeferred']) == 1),
        'concurrent': (int(node['concurrent']) == 1),
        }

    retval += format_optional_node_field(node, 'relation')
    retval += format_optional_node_list(node, 'indexParams')
    retval += format_optional_node_list(node, 'options', newLine=False)
    retval += format_optional_node_field(node, 'whereClause')
    retval += format_optional_node_list(node, 'excludeOpNames')

    return add_indent(retval, indent)

def format_alter_table_stmt(node, indent=0):
    retval = 'AlterTableStmt [relkind=%(relkind)s missing_ok=%(missing_ok)s]' % {
        'relkind': node['relkind'],
        'missing_ok': (int(node['missing_ok']) == 1),
    }
    retval += format_optional_node_field(node, 'relation')
    retval += format_optional_node_list(node, 'cmds')

    return add_indent(retval, indent)

def format_range_var(node, indent=0):
    retval = 'RangeVar ['

    if (str(node['catalogname']) != '0x0'):
        retval += 'catalogname=%(catalogname)s ' % { 'catalogname': getchars(node['catalogname']) }

    if (str(node['schemaname']) != '0x0'):
        retval += 'schemaname=%(schemaname)s ' % { 'schemaname': getchars(node['schemaname']) }

    retval += 'relname=%(relname)s inh=%(inh)s relpersistence=%(relpersistence)s alias=%(alias)s location=%(location)s]' % {
        'relname': getchars(node['relname']),
        'inh': (int(node['inh']) == 1),
        'relpersistence': node['relpersistence'],
        'alias': node['alias'],
        'location': node['location'],
    }

    return add_indent(retval, indent)

def format_partition_by(node, indent=0):
    retval = 'PartitionBy [partType=%(partType)s partDepth=%(partDepth)s bKeepMe=%(bKeepMe)s partQuiet=%(partQuiet)s location=%(location)s]' % {
        'partType': node['partType'],
        'partDepth': node['partDepth'],
        'bKeepMe': (int(node['bKeepMe']) == 1),
        'partQuiet': node['partQuiet'],
        'location': node['location'],
    }

    retval += format_optional_node_field(node, 'keys')
    retval += format_optional_node_field(node, 'keyopclass')
    retval += format_optional_node_field(node, 'subPart')
    retval += format_optional_node_field(node, 'partSpec')
    retval += format_optional_node_field(node, 'partDefault')
    retval += format_optional_node_field(node, 'parentRel')

    return add_indent(retval, indent)

def format_partition_spec(node, indent=0):
    retval = 'PartitionSpec [istemplate=%(istemplate)s location=%(location)s]' % {
        'istemplate': node['istemplate'],
        'location': node['location'],
    }

    retval += format_optional_node_list(node, 'partElem')
    retval += format_optional_node_list(node, 'enc_clauses', newLine=False)
    retval += format_optional_node_field(node, 'subSpec')

    return add_indent(retval, indent)

def format_constraint(node, indent=0):
    retval = 'Constraint [contype=%(contype)s conname=%(conname)s deferrable=%(deferrable)s initdeferred=%(initdeferred)s location=%(location)s is_no_inherit=%(is_no_inherit)s' % {
        'contype': node['contype'],
        'conname': getchars(node['conname']),
        'deferrable': (int(node['deferrable']) == 1),
        'initdeferred': (int(node['initdeferred']) == 1),
        'location': node['location'],
        'is_no_inherit': (int(node['is_no_inherit']) == 1),
    }

    if (str(node['indexname']) != '0x0'):
        retval += ' indexname=%s' % getchars(node['indexname'])
    if (str(node['indexspace']) != '0x0'):
        retval += ' indexspace=%s' % node['indexspace']
        retval += ' access_method=%s' % node['access_method']

    foreign_key_matchtypes = {
        'f': 'FKCONSTR_MATCH_FULL',
        'p': 'FKCONSTR_MATCH_PARTIAL',
        's': 'FKCONSTR_MATCH_SIMPLE',
    }

    if (foreign_key_matchtypes.get(node['fk_matchtype']) != None):
        retval += ' fk_matchtype=%s' % foreign_key_matchtypes.get(node['fk_matchtype'])

    foreign_key_actions = {
        'a': 'FKONSTR_ACTION_NOACTION',
        'r': 'FKCONSTR_ACTION_RESTRICT',
        'c': 'FKCONSTR_ACTION_CASCADE',
        'n': 'FKONSTR_ACTION_SETNULL',
        'd': 'FKONSTR_ACTION_SETDEFAULT',
    }

    if (foreign_key_actions.get(node['fk_upd_action']) != None):
        retval += ' fk_upd_action=%s' % foreign_key_actions.get(node['fk_upd_action'])

    if (foreign_key_actions.get(node['fk_upd_action']) != None):
        retval += ' fk_del_action=%s' % foreign_key_actions.get(node['fk_upd_action'])

    if (node['old_pktable_oid'] != 0):
        retval += ' old_pktable_oid=%s' % node['old_pktable_oid']

    retval += ' skip_validation=%s' % (int(node['skip_validation']) == 1)
    retval += ' initially_valid=%s' % (int(node['initially_valid']) == 1)

    retval += ']'


    retval += format_optional_node_field(node, 'raw_expr')

    if (str(node['cooked_expr']) != '0x0'):
        retval += add_indent('[cooked_expr] %s' % node['cooked_expr'], 1, True)

    retval += format_optional_node_list(node, 'keys')
    retval += format_optional_node_list(node, 'exclusions')
    retval += format_optional_node_list(node, 'options')
    retval += format_optional_node_field(node, 'where_clause')
    retval += format_optional_node_field(node, 'pktable')
    retval += format_optional_node_field(node, 'old_conpfeqop')

    return add_indent(retval, indent)

def format_reloptinfo(node, indent=0):
    retval = 'RelOptInfo (kind=%(kind)s relids=%(relids)s rtekind=%(rtekind)s relid=%(relid)s rows=%(rows)s)' % {
        'kind': node['reloptkind'],
        'rows': node['rows'],
        'relid': node['relid'],
        'relids': format_bitmapset(node['relids']),
        'rtekind': node['rtekind'],
    }

    return add_indent(retval, indent)


def format_rte(node, indent=0):
    global rtes
    global rteindex
    retval = 'RangeTblEntry (rtekind=%(rtekind)s \t relname=%(relname)s \t relalias=%(relalias)s relid=%(relid)s relkind=%(relkind)s' % {
        'relid': node['relid'],
        'rtekind': node['rtekind'],
        'relalias': format_node(node['alias']),
        'relname': getchars(node['relname']),
        'relkind': format_char(node['relkind'])
    }
    rtes[rteindex] = node
    rteindex += 1

    if int(node['inh']) != 0:
        retval += ' inh=%(inh)s' % { 'inh': (int(node['inh']) == 1) }

    retval += ")"

    return add_indent(retval, indent)

def format_generic_expr_state(node, indent=0):
    exprstate = node['xprstate']
    child = cast(node['arg'], 'ExprState')
    return '''GenericExprState [evalFunc=%(evalFunc)s childEvalFunc= %(childEvalFunc)s]
\t%(expr)s''' % {
#\tChild Expr:
#%(childexpr)s''' % {
            'expr': format_node(exprstate['expr']),
            'evalFunc': format_node(exprstate['evalfunc']),
            'childexpr': format_node(child['expr']),
            'childEvalFunc': child['evalfunc']
    }


def format_op_expr(node, indent=0):
    '''OpExpr [opno=98 opfuncid=67 opresulttype=16 inputcollid=100]
          RelabelType [resulttype=25 resulttypmod=-1 resultcollid=100 relabelformat=COERCE_IMPLICIT_CAST]
                  Var [varno=OUTER varattno=6 varcollid=100 levelsup=0 location=496]
          RelabelType [resulttype=25 resulttypmod=-1 resultcollid=100 relabelformat=COERCE_IMPLICIT_CAST]
                  Var [varno=INNER varattno=2 varcollid=100 levelsup=0 location=480]
       ((tb_audit_provpayandreceive_down.pass_id)::text = (tb_audit_provpayandreceive_down_1.pass_id)::text)
    '''

    retval = ''
    nodetag = 'OpExpr'

    if is_a(cast(node, 'Node'), 'DistinctExpr'):
        nodetag =  'DistinctExpr'

    if is_a(cast(node, 'Node'), 'NullIfExpr'):
        nodetag =  'NullIfExpr'

    if verbose or nodetag == 'DistinctExpr' or nodetag == 'NullIfExpr':
      retval += """%(nodetag)s [opno=%(opno)s opfuncid=%(opfuncid)s opresulttype=%(opresulttype)s""" % {
        'nodetag': nodetag,
        'opno': node['opno'],
        'opfuncid': node['opfuncid'],
        'opresulttype': node['opresulttype'],
      }
    else:
      larg = ''
      ltype = ''
      rarg = ''
      rtype = ''
      op = ''

      l = node['args']['head']
      r = node['args']['head']['next']
      lnode = cast(l['data']['ptr_value'], 'Node')
      rnode = cast(r['data']['ptr_value'], 'Node')

      def pp_node(node):
          node = cast(node, 'RelabelType')
          node = node['arg']
          return format_node(node)
      
      if is_a(lnode, 'RelabelType'):
        larg = pp_node(lnode)
      else:
        larg = format_node(lnode)

      if is_a(rnode, 'RelabelType'):
        rarg = pp_node(rnode)
      else:
        rarg = format_node(rnode)


      if node['opfuncid'] == 67:
          op = '='
          ltype = 'text'
          rtype = 'text'
      elif node['opfuncid'] == 743:
          op = '>='
          ltype = 'text'
          rtype = 'text'
      elif node['opfuncid'] == 477:
          op = '>'
          ltype = 'int8'
          rtype = 'int4'
      else:
          op = 'unkown'
          ltype = 'unkown'
          rtype = 'unkown'

      retval += """((%(larg)s)::%(ltype)s %(op)s (%(rarg)s)::%(rtype)s)""" % {
            'larg': larg,
            'ltype': ltype,
            'op': op,
            'rarg': rarg,
            'rtype': rtype,
        }


    if verbose:
      if node['opcollid'] != 0:
        retval += ' opcollid=%s' % node['opcollid']
      if node['inputcollid'] != 0:
        retval += ' inputcollid=%s' % node['inputcollid']
      retval += ']'

      retval+= format_optional_node_list(node, 'args', skip_tag=True)

    return add_indent(retval, indent)

def format_func_expr(node, indent=0):

    retval = """FuncExpr [funcid=%(funcid)s funcresulttype=%(funcresulttype)s funcretset=%(funcretset)s funcformat=%(funcformat)s""" % {
        'funcid': node['funcid'],
        'funcresulttype': node['funcresulttype'],
        'funcretset': (int(node['funcretset']) == 1),
        'funcvaridaic': (int(node['funcvariadic']) == 1),
        'funcformat': node['funcformat'],
    }

    if node['funccollid'] != 0:
        retval += ' funccollid=%s' % node['funccollid']
    if node['inputcollid'] != 0:
        retval += ' inputcollid=%s' % node['inputcollid']

    retval += ' location=%(location)s]' % {
        'location': node['location'],
    }

    retval += format_optional_node_list(node, 'args', skip_tag=True)

    return add_indent(retval, indent)

def format_relabel_type(node, indent=0):

    retval = """RelabelType [resulttype=%(resulttype)s resulttypmod=%(resulttypmod)s""" % {
        'resulttype': node['resulttype'],
        'resulttypmod': node['resulttypmod'],
    }

    if node['resultcollid'] != 0:
        retval += ' resultcollid=%s' % node['resultcollid']

    retval += ' relabelformat=%(relabelformat)s]' % {
        'relabelformat': node['relabelformat'],
    }

    retval += format_optional_node_field(node, 'arg', skip_tag=True)

    return add_indent(retval, indent)

def format_coerce_via_io(node, indent=0):

    retval = """CoerceViaIO [resulttype=%(resulttype)s coerceformat=%(coerceformat)s location=%(location)s""" % {
        'resulttype': node['resulttype'],
        'coerceformat': node['coerceformat'],
        'location': node['location'],
    }

    if node['resultcollid'] != 0:
        retval += ' resultcollid=%s' % node['resultcollid']

    retval += ']'

    retval += format_optional_node_field(node, 'arg', skip_tag=True)

    return add_indent(retval, indent)

def format_scalar_array_op_expr(node, indent=0):
    retval = """ScalarArrayOpExpr [opno=%(opno)s opfuncid=%(opfuncid)s useOr=%(useOr)s]
%(clauses)s""" % {
        'opno': node['opno'],
        'opfuncid': node['opfuncid'],
        'useOr': (int(node['useOr']) == 1),
        'clauses': format_node_list(node['args'], 1, True)
    }
    return add_indent(retval, indent)

def format_a_expr(node, indent=0):
    retval = "A_Expr [kind=%(kind)s location=%(location)s]" % {
        'kind': node['kind'],
        'location': node['location'],
        }

    retval += format_optional_node_list(node, 'name', newLine=False)
    retval += format_optional_node_field(node, 'lexpr')
    retval += format_optional_node_field(node, 'rexpr')

    return add_indent(retval, indent)

def format_a_const(node, indent=0):
    retval = "A_Const [val=(%(val)s) location=%(location)s]" % {
        'val': format_node(node['val'].address),
        'location': node['location'],
        }

    return add_indent(retval, indent)

def format_case_expr(node, indent=0):
    retval = 'CaseExpr [casetype=%(casetype)s casecollid=%(casecollid)s] ' % {
        'casetype': node['casetype'],
        'casecollid': node['casecollid'],
    }

    retval += format_optional_node_field(node, 'arg')
    retval += format_optional_node_list(node, 'args')
    retval += format_optional_node_field(node, 'defresult')

    return add_indent(retval, indent)

def format_coalesce_expr(node, indent=0):
    retval = "CoalesceExpr [coalescetype=%(coalescetype)s location=%(location)s]" % {
        'coalescetype': node['coalescetype'],
        'location': node['location'],
        }

    retval += format_optional_node_list(node, 'args')

    return add_indent(retval, indent)

def format_case_when(node, indent=0):
    retval = '''CaseWhen''' % {
            'result': format_node(node['result'])
    }

    retval += format_optional_node_field(node, 'expr', skip_tag=True)
    retval += format_optional_node_field(node, 'result')

    return add_indent(retval, indent)

def format_bool_expr(node, indent=0):

    retval = 'BoolExpr [op=%s]' % node['boolop']
    retval += format_optional_node_list(node, 'args', skip_tag=True)

    return add_indent(retval, indent)

def format_from_expr(node, indent=0):
    retval = 'FromExpr'
    retval += format_optional_node_list(node, 'fromlist')
    retval += format_optional_node_field(node, 'quals')

    return add_indent(retval, indent)

def format_sublink(node, indent=0):
    retval = """SubLink [subLinkType=%(subLinkType)s location=%(location)s]""" % {
        'subLinkType': node['subLinkType'],
        'location': (int(node['location']) == 1),
    }

    retval += format_optional_node_field(node, 'testexpr')
    retval += format_optional_node_list(node, 'operName')
    retval += format_optional_node_field(node, 'subselect')

    return add_indent(retval, indent)

def format_join_expr(node, indent=0):
    retval = """JoinExpr [jointype=%(jointype)s isNatural=%(isNatural)s]""" % {
        'jointype': node['jointype'],
        'isNatural': (int(node['isNatural']) == 1),
    }

    retval += format_optional_node_field(node, 'larg')
    retval += format_optional_node_field(node, 'rarg')
    retval += format_optional_node_list(node, 'usingClause')
    retval += format_optional_node_field(node, 'quals')

    return add_indent(retval, indent)

def format_target_entry(node, indent=0):
    retval = 'TargetEntry [resno=%(resno)s resname=%(name)s ressortgroupref=%(ressortgroupref)s origtbl=%(tbl)s origcol=%(col)s junk=%(junk)s]' % {
        'resno': node['resno'],
        'name': getchars(node['resname']),
        'ressortgroupref': node['ressortgroupref'],
        'tbl': node['resorigtbl'],
        'col': node['resorigcol'],
        'junk': (int(node['resjunk']) == 1),
    }

    retval += format_optional_node_field(node, 'expr', skip_tag=True)

    return add_indent(retval, indent)

def format_sort_group_clause(node, indent=0):
    retval = 'SortGroupClause [tleSortGroupRef=%(tleSortGroupRef)s eqop=%(eqop)s sortop=%(sortop)s nulls_first=%(nulls_first)s hashable=%(hashable)s]' % {
        'tleSortGroupRef': node['tleSortGroupRef'],
        'eqop': node['eqop'],
        'sortop': node['sortop'],
        'nulls_first': (int(node['nulls_first']) == 1),
        'hashable': (int(node['hashable']) == 1),
    }

    return add_indent(retval, indent)

def format_table_like_clause(node):
    retval = "TableLikeClause [options=%08x]" % int(node['options'])

    retval += format_optional_node_field(node, 'relation')

    return retval

def get_rte_col(ret, varindex):
    col = ''
    currindex = 0
    lst = ret['eref']['colnames']

    item = lst['head']

    while str(item) != '0x0':
        currindex += 1
        node = cast(item['data']['ptr_value'], 'Node')
        col = format_node(node, 0, True)
        if currindex == varindex:
            return col
        item = item['next']

    return col

def format_var(node, indent=0):
    if node['varno'] == 65000:
        varno = "INNER"
    elif node['varno'] == 65001:
        varno = "OUTER"
        if outer_tlist:
            print(outer_tlist)
    else:
        varno = node['varno']
        if len(rtes) != 0:
            rte = rtes[int(varno) - 1]
            rte = cast(rte, 'RangeTblEntry')
            col = get_rte_col(rte, int(node['varattno']))
            return add_indent(col, indent)

    retval = 'Var [varno=%(varno)s varattno=%(attno)s' % {
        'varno': varno,
        'attno': node['varattno'],
    }


    if node['varcollid'] != 0:
        retval += ' varcollid=%s' % node['varcollid']

    retval += ' levelsup=%(levelsup)s' % {
        'levelsup': node['varlevelsup']
    }

    # if node['varnoold'] != 0:
    #     retval += ' varnoold=%s' % node['varnoold']

    # if node['varoattno'] != 0:
    #     retval += ' varoattno=%s' % node['varoattno']

    if node['location'] != -1:
        retval += ' location=%s' % node['location']

    retval += ']'

    return add_indent(retval, indent)

def format_const(node, indent=0):
    if verbose:
      retval = "Const [consttype=%s" % node['consttype']
      if (node['consttypmod'] != -1):
        retval += " consttypmod=%s" % node['consttypmod']

      if node['constcollid']:
        retval += " constcollid=%s" % node['constcollid']

      retval += " constlen=%s constvalue=" % node['constlen']
    else:
      retval = "Const ["

    # Print the value if the type is int4 (23)
    if(int(node['consttype']) == 23):
        retval += "%s" % node['constvalue']
    # Print the value if type is oid
    elif(int(node['consttype']) == 26):
        retval += "%s" % node['constvalue']
    elif(int(node['consttype']) == 20):
        retval += "%s" % node['constvalue']
    else:
        retval += "%s" % hex(int(node['constvalue']))

    if verbose:
      retval += " constisnull=%(constisnull)s constbyval=%(constbyval)s" % {
            'constisnull': (int(node['constisnull']) == 1),
            'constbyval': (int(node['constbyval']) == 1) }

    retval += ']'

    return add_indent(retval, indent)

def format_aggref(node, indent=0):
    retval = ''
    if not verbose:
        func = ''
        args = ''
        if node['aggfnoid'] == 2147:
            func = 'count'
            anode = cast(node['args'], 'List')
            anode = anode['head']['data']['ptr_value']
            if is_a(cast(anode, 'Node'), 'TargetEntry'):
              anode = cast(anode, 'TargetEntry')
              anode = anode['expr']
            args = format_node(anode)
        else:
            func = 'unkown'
            args = 'unkown'


        retval = '''%(func)s(%(args)s)''' % {
            'func': func,
            'args': args
        }
    else:
      retval = '''Aggref (aggfnoid=%(fnoid)s aggtype=%(aggtype)s''' % {
          'fnoid': node['aggfnoid'],
          'aggtype': node['aggtype'],
      }

      if node['aggcollid'] != 0:
          retval += ' aggcollid=%s' % node['aggcollid']

      if node['inputcollid'] != 0:
          retval += ' inputcollid=%s' % node['inputcollid']

      retval += ''' aggtranstype=%(aggtranstype)s aggstar=%(aggstar)s aggvariadic=%(aggvariadic)s aggkind='%(aggkind)s' agglevelsup=%(agglevelsup)s aggsplit=%(aggsplit)s location=%(location)s)''' % {
          'aggtranstype': node['aggtranstype'],
          'aggstar': (int(node['aggstar']) == 1),
          'aggvariadic': (int(node['aggvariadic']) == 1),
          'aggkind': format_char(node['aggkind']),
          'agglevelsup': node['agglevelsup'],
          'aggsplit': node['aggsplit'],
          'location': node['location'],
      }

      retval += format_optional_node_list(node, 'args', skip_tag=True)
      retval += format_oid_list(node['aggargtypes'])
      retval += format_optional_node_list(node, 'aggdirectargs')
      retval += format_optional_node_list(node, 'aggorder')
      retval += format_optional_node_list(node, 'aggdistinct')
      retval += format_optional_node_field(node, 'aggfilter')
    return add_indent(retval, indent)

def is_a(n, t):
    '''checks that the node has type 't' (just like IsA() macro)'''

    return (str(n['type']) == ('T_' + t))


def is_node(l):
    '''return True if the value looks like a Node (has 'type' field)'''

    try:
        x = l['type']
        return True
    except:
        return False


def cast(node, type_name):
    '''wrap the gdb cast to proper node type'''

    # lookup the type with name 'type_name' and cast the node to it
    t = gdb.lookup_type(type_name)
    return node.cast(t.pointer())


def add_indent(val, indent, add_newline=False):
    retval = ''
    if add_newline == True:
        retval += '\n'

    retval += "\n".join([(("\t" * indent) + l) for l in val.split("\n")])
    return retval

def getchars(arg, qoute = True):
    if (str(arg) == '0x0'):
        return str(arg)

    retval = ''
    if qoute:
        retval += '"'

    i=0
    while arg[i] != ord("\0"):
        character = int(arg[i].cast(gdb.lookup_type("char")))
        if chr(character) in string.printable:
            retval += "%c" % chr(character)
        else:
            retval += "\\x%x" % character
        i += 1

    if qoute:
        retval += '"'

    return retval


class PgPrintCommand(gdb.Command):

    def __init__(self):
        super(PgPrintCommand, self).__init__("pgprint", gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, False)

    def invoke(self, arg, from_tty):
        arg_list = gdb.string_to_argv(arg)
        if len(arg_list) != 1:
            raise gdb.GdbError ("Usage: pgprint var")

        l = gdb.parse_and_eval(arg_list[0])


        print(format_node(l))


PgPrintCommand()


