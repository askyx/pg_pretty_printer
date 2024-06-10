import gdb
import string
import re
from functools import reduce
import platform

printer = gdb.printing.RegexpCollectionPrettyPrinter('REL_17_BETA1')

def register_printer(name):
    def __registe(_printer):
        printer.add_printer(name, '^' + name + '$', _printer)
    return __registe

def cast2ptr(node, type_name):
    t = gdb.lookup_type(type_name)
    return node.cast(t.pointer())

class Printer:
    def __init__(self, val) -> None:
        self.val = val

    def node_type(self):
        return str(self.val['type'])[2:]

# max print 100
def getchars(arg, quote = True, length = 100):
    if (str(arg) == '0x0'):
        return '0x0'

    retval = ''
    if quote:
        retval += '\''

    i = 0
    while arg[i] != ord('\0') and i < length:
        character = int(arg[i].cast(gdb.lookup_type('char')))
        if chr(character) in string.printable:
            retval += '%c' % chr(character)
        else:
            retval += '\\x%x' % character
        i += 1

    if quote:
        retval += '\''

    return retval


@register_printer('Bitmapset')
class BitmapsetPrinter(Printer):
    def bms_next_member(self, prevbit, bit_per_w):
        if str(self.val) == '0x0':
            return -2

        nwords = self.val['nwords']
        prevbit += 1
        mm = 0
        if bit_per_w == 64:
            mm = 0xFFFFFFFFFFFFFFFF
        else:
            mm = 0xFFFFFFFF

        mask = (mm << int(prevbit % bit_per_w)) & mm

        for wordnum in range(prevbit // bit_per_w, nwords):
            w = int(self.val['words'][wordnum] & mask)
            if w != 0:
                return int(wordnum * bit_per_w + w.bit_length() - len(bin(w).rstrip('0')) + 2)
            mask = mm
        return -2

    def to_string(self):
        # no print now
        return 'xx'
        # try:
        #     return getchars(gdb.parse_and_eval('bmsToString({})'.format(self.val.address)), False)
        # except gdb.error:
        #     return self.val
        # do it by yourself, flowing code is not work, it may cause 'maximum recursion depth exceeded in comparison' error
        # why? anything wrong with my code?
        # if we want run this to debug a core file, must resolve this issue first.
        list = []
        BITS_PER_BITMAPWORD = 64 if platform.architecture()[0] == '64bit' else 32
        index = bms_next_member(self.val, -1, BITS_PER_BITMAPWORD)
        while index >= 0:
            list.append(index)
            index = bms_next_member(self.val, index, BITS_PER_BITMAPWORD)

        return str(list)



@register_printer('A_Star')
class A_StarPrinter(Printer):
    def to_string(self):
        return '*'

@register_printer('QualCost')
class QualCostPrinter(Printer):
    def to_string(self):
        return '{{{:.2f}..{:.2f}}}'.format(float(self.val['startup']), float(self.val['per_tuple']))


@register_printer('A_Const')
class A_ConstPrinter(Printer):
    def to_string(self):
        if bool(self.val['isnull']):
            return ''
        vt = str(self.val['val']['node']['type'])[2:]
        ret = ''
        if vt == 'Integer':
            ret += str(self.val['val']['ival']['ival'])
        elif vt == 'Float':
            ret += getchars(self.val['val']['fval']['fval'])
        elif vt == 'Boolean':
            ret += str(self.val['val']['boolval']['boolval'])
        elif vt == 'BitString':
            ret += getchars(self.val['val']['bsval']['bsval'])
        elif vt == 'String':
            ret += getchars(self.val['val']['sval']['sval'])
        return '{} {{ {} }}'.format(vt, ret)

@register_printer('List')
class ListPrinter:
    class _iter(object):

        def __init__(self, type, list) -> None:
            self.type = type
            self.list = list
            self.size = list['length']
            self.count = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.count == self.size:
                raise StopIteration
            node = self.list['elements'][self.count]

            if str(self.type) == 'List':
                type = cast2ptr(node['ptr_value'], 'Node')['type']
                if int(type) > 0 and int(type) < gdb.parse_and_eval('(int) T_WindowObjectData'):
                    node = cast2ptr(node, str(type)[2:]).dereference()
                else:
                    node = node['ptr_value']
            elif str(self.type) == 'IntList':
                node = int(node['int_value'])
            elif str(self.type) == 'OidList':
                node = int(node['oid_value'])
            else:
                node = node['xid_value']

            result = (str(self.count), node)
            self.count += 1
            return result

    def __init__(self,  val) -> None:
        self.val = val
        self.type = str(self.val['type'])[2:]

    def to_string(self):
        return '%s with %s elements' % (self.type, self.val['length'])

    def children(self):
        return self._iter(self.type, self.val)

    def display_hint(self):
        if self.type == 'List':
            return None
        else:
            return 'array'

class PrinterGenerator:
    def __init__(self, val) -> None:
        self.val = val
        self.not_printable = ['type', 'xpr', 'parent_root', 'simple_rte_array',
                              'append_rel_array', 'join_rel_hash', 'join_rel_level',
                              'placeholder_array', 'placeholder_array_size', 'part_schemes',
                              'initial_rels', 'upper_rels', 'upper_targets', 'grouping_map', 'planner_cxt', 'isAltSubplan', 'isUsedSubplan',
                              'join_search_private', 'boundParams', 'subroots', 'partition_directory', 'attr_needed', 'attr_widths',
                              'fdwroutine', 'fdw_private', 'parent', 'top_parent', 'part_scheme', 'boundinfo', 'part_rels',
                              'partexprs', 'nullable_partexprs', 'rel', 'opclassoptions', 'indexprs', 'amcostestimate', 'em_parent',
                              'parent_ec', 'left_ec', 'right_ec', 'scansel_cache', 'initValue', 'location',

                              'simple_rel_array', 'simple_rel_array_size', 'sortgrouprefs',
                              'sortColIdx', 'sortOperators', 'collations', 'nullsFirst',    # Sort
                              'dupColIdx', 'dupOperators', 'dupCollations',                 # RecursiveUnion
                              'mergeFamilies', 'mergeCollations', 'mergeStrategies', 'mergeNullsFirst',  # MergeJoin
                              'hashOperators', # Memoize
                              'grpColIdx','grpOperators','grpCollations',  # Group
                              ]

    def is_target_type(self, val, type):
        try:
            val[type]
            return True
        except gdb.error:
            return False
        
    def get_type(self, val):
        if self.is_target_type(val, 'type'):
            return str(val['type'])[2:]
        elif self.is_target_type(val, 'xpr'):
            return str(val['xpr']['type'])[2:]
        elif self.is_target_type(val, 'path'):
            return str(val['path']['type'])[2:]
        elif self.is_target_type(val, 'plan'):
            return str(val['plan']['type'])[2:]
        elif self.is_target_type(val, 'jpath'):
            return str(val['jpath']['path']['type'])[2:]
        elif self.is_target_type(val, 'sort'):
            return str(val['sort']['plan']['type'])[2:]
        elif self.is_target_type(val, 'join'):
            return str(val['join']['plan']['type'])[2:]
        elif self.is_target_type(val, 'scan'):
            return str(val['scan']['plan']['type'])[2:]

        return None

    def printable(self, name):
        return name not in self.not_printable

    def get_convertable_type(self, type):
        if type in ['OidList', 'IntList', 'XidList']:
            return 'List'

        return None

class PathPrinterGenerator(PrinterGenerator):
    def __init__(self, val) -> None:
        super().__init__(val)
        self.type = self.get_type(self.val)
        self.basic_path = self.val.cast(gdb.lookup_type('Path'))
        self.actually_path = str(self.basic_path['pathtype'])[2:]
        self.extend_path = self.val.cast(gdb.lookup_type(self.type))

    def path_to_string(self):
        path = self.basic_path
        return '(cost: {:.2f}..{:.2f} rows: {:.0f} parallel{{aware: {} safe: {} workers: {}}}) parent: {}'.format(
                        float(path['startup_cost']), float(path['total_cost']), float(path['rows']),
                        bool(path['parallel_aware']), bool(path['parallel_safe']), int(path['parallel_workers']),
                        '0x0' if path['parent']['relids'] == 0 else path['parent']['relids'].dereference())

    def path_children(self):
        path = self.basic_path
        fields = []
        if path['parent']['reltarget'] != 0 and path['pathtarget'] != 0 and path['parent']['reltarget'] != path['pathtarget']:
            fields.append(('reltarget', path['pathtarget'].dereference()))

        if path['param_info']:
            fields.append(('param_info', path['param_info']['ppi_req_outer'].dereference()))

        if path['pathkeys']:
            fields.append(('pathkeys', path['pathkeys'].dereference()))

        return fields

    def common_to_string(self):
        if self.type == 'Path':
            return self.actually_path + ' ' + self.path_to_string()
        else:
            fields = []
            for field in self.extend_path.type.fields():
                if self.printable(field.name):

                    # print path field
                    if field.name == 'path' or field.name == 'jpath':
                        fields.append(self.path_to_string())
                        if field.name == 'jpath':
                            fields.append('{}: {}'.format('jointype', self.extend_path[field.name]['jointype']))
                            fields.append('{}: {}'.format('inner_unique', self.extend_path[field.name]['inner_unique']))
                        continue

                    # print no pointer field
                    if field.type.code != gdb.TYPE_CODE_PTR:
                        fields.append('{}: {}'.format(field.name, self.extend_path[field.name]))

                    # print char * field
                    if field.type.code == gdb.TYPE_CODE_PTR and self.extend_path[field.name] != 0 and str(field.type) == 'char *':
                        fields.append('{}: {}'.format(field.name, getchars(self.extend_path[field.name])))
        
            return self.actually_path + ' {' + ', '.join(fields) + '}'
    
    def common_children(self):
        if self.type == 'Path':
            for i in self.path_children():
                yield i
        else:
            for field in self.extend_path.type.fields():
                if self.printable(field.name):
                    if field.name == 'path' or field.name == 'jpath':
                        for i in self.path_children():
                            yield i
                        if field.name == 'jpath':
                            outer_type = self.get_type(self.extend_path[field.name]['outerjoinpath'])
                            inner_type = self.get_type(self.extend_path[field.name]['innerjoinpath'])
                            yield ('outerjoinpath', cast2ptr(self.extend_path[field.name]['outerjoinpath'], outer_type).dereference())
                            yield ('innerjoinpath', cast2ptr(self.extend_path[field.name]['innerjoinpath'], inner_type).dereference())
                            if self.extend_path[field.name]['joinrestrictinfo'] != 0:
                                yield ('joinrestrictinfo', self.extend_path[field.name]['joinrestrictinfo'].dereference())
                        continue
                    
                    # char * printed in common_to_string
                    if str(field.type) != 'char *' and self.extend_path[field.name] != 0 :

                        # Relids is def of Bitmapset *, print it
                        if field.type.code == gdb.TYPE_CODE_PTR or str(field.type) == 'Relids':

                            #  get type and convert it
                            type = self.get_type(self.extend_path[field.name])

                            # convert to base type
                            base_type = self.get_convertable_type(type)
                            if base_type:
                                yield (field.name, cast2ptr(self.extend_path[field.name], base_type).dereference())
                            else:
                                yield (field.name, self.extend_path[field.name].dereference())

class PlanPrinterGenerator(PrinterGenerator):
    def __init__(self, val) -> None:
        super().__init__(val)
        self.type = self.get_type(self.val)
        self.basic_plan = self.val.cast(gdb.lookup_type('Plan'))
        self.extend_plan = self.val.cast(gdb.lookup_type(self.type))
        self.array_filed = []

        if self.type in ['MergeAppend', 'Sort']:
            self.print_sort(self.extend_plan)
        elif self.type == 'RecursiveUnion':
            self.print_RecursiveUnion_array(self.extend_plan)
        elif self.type == 'Memoize':
            self.print_Memoize_array(self.extend_plan)
        elif self.type in ['Group', 'Agg']:
            self.print_Group_array(self.extend_plan)
        elif self.type == 'MergeJoin':
            self.print_MergeJoin_array(self.extend_plan)

    def plan_to_string(self):
        plan = self.basic_plan
        return '(cost: {:.2f}..{:.2f} rows: {:.0f} width: {} parallel{{aware: {} safe: {}}}) async_capable: {} node_id: {}'.format(
                        float(plan['startup_cost']), float(plan['total_cost']), float(plan['plan_rows']), int(plan['plan_width']),
                        bool(plan['parallel_aware']), bool(plan['parallel_safe']), bool(plan['async_capable']), int(plan['plan_node_id']))

    def plan_children(self):
        plan = self.basic_plan
        fields = []

        if plan['targetlist']:
            fields.append(('targetlist', plan['targetlist'].dereference()))
        if plan['qual']:
            fields.append(('qual', plan['qual'].dereference()))
        if plan['lefttree']:
            outer_type = self.get_type(plan['lefttree'])
            fields.append(('lefttree', cast2ptr(plan['lefttree'], outer_type).dereference()))
        if plan['righttree']:
            inner_type = self.get_type(plan['righttree'])
            fields.append(('righttree', cast2ptr(plan['righttree'], inner_type).dereference()))
        if plan['extParam']:
            fields.append(('extParam', plan['extParam'].dereference()))
        if plan['allParam']:
            fields.append(('allParam', plan['allParam'].dereference()))

        return fields

    def get_array(self, val, keys, numCols):
        slist = []
        if numCols > 0:
            values = ([int(val[key][i]) for i in range(numCols)] for key in keys)
            for key, value in zip(keys, values):
                slist.append((key, str(value)))
        return slist

    def print_sort(self, val):
        numCols = int(val['numCols'])
        self.array_filed = self.get_array(val, ['sortColIdx','sortOperators', 'collations', 'nullsFirst'], numCols)
    
    def print_RecursiveUnion_array(self, val):
        numCols = int(val['numCols'])
        self.array_filed = self.get_array(val, ['dupColIdx', 'dupOperators', 'dupCollations'], numCols)

    def print_Memoize_array(self, val):
        numCols = int(val['numKeys'])
        self.array_filed = self.get_array(val, ['hashOperators', 'collations'], numCols)
    
    def print_Group_array(self, val):
        numCols = int(val['numCols'])
        self.array_filed = self.get_array(val, ['grpColIdx', 'grpOperators', 'grpCollations'], numCols)

    def print_MergeJoin_array(self, val):
        numCols = int(val['mergeclauses']['length'])
        self.array_filed = self.get_array(val, ['mergeFamilies','mergeCollations','mergeStrategies', 'mergeNullsFirst'], numCols)

    def common_to_string(self):
        fields = []
        for field in self.extend_plan.type.fields():
            if self.printable(field.name):

                # print plan field
                if field.name == 'plan' or field.name == 'scan' or field.name == 'sort' or field.name == 'join':
                    fields.append(self.plan_to_string())
                    if field.name == 'scan':
                        fields.append('{}: {}'.format('scanrelid', self.extend_plan[field.name]['scanrelid']))

                    elif field.name == 'join':
                        fields.append('{}: {}'.format('jointype', self.extend_plan[field.name]['jointype']))
                        fields.append('{}: {}'.format('inner_unique', self.extend_plan[field.name]['inner_unique']))

                # print no pointer field
                elif field.type.code != gdb.TYPE_CODE_PTR:
                    fields.append('{}: {}'.format(field.name, self.extend_plan[field.name]))

                # print char * field
                elif field.type.code == gdb.TYPE_CODE_PTR and self.extend_plan[field.name] != 0 and str(field.type) == 'char *':
                    fields.append('{}: {}'.format(field.name, getchars(self.extend_plan[field.name])))

        return self.type + ' {' + ', '.join(fields) + '}'

    def common_children(self):
        if self.type == 'Sort':
            for i in self.plan_children():
                yield i
            for i in self.array_filed:
                yield i
        else:
            for field in self.extend_plan.type.fields():
                if self.printable(field.name):
                    if field.name in ['plan', 'scan', 'sort', 'join']:
                        for i in self.plan_children():
                            yield i
                        if field.name == 'sort':
                            sort = self.extend_plan['sort']
                            for i in self.print_sort(sort):
                                yield i

                        if field.name == 'join' and self.extend_plan[field.name]['joinqual']:
                            yield ('joinqual', self.extend_plan[field.name]['joinqual'].dereference())

                    # char * printed in common_to_string
                    elif str(field.type) != 'char *' and self.extend_plan[field.name] != 0 :

                        # Relids is def of Bitmapset *, print it
                        if field.type.code == gdb.TYPE_CODE_PTR or str(field.type) == 'Relids':

                            #  get type and convert it
                            type = self.get_type(self.extend_plan[field.name])

                            # convert to base type
                            base_type = self.get_convertable_type(type)
                            if base_type:
                                yield (field.name, cast2ptr(self.extend_plan[field.name], base_type).dereference())
                            else:
                                yield (field.name, self.extend_plan[field.name].dereference())

            if self.type in ['RecursiveUnion', 'Memoize', 'Group', 'Agg', 'MergeJoin']:
                for i in self.array_filed:
                    yield i

@register_printer('(Node|Expr)')
class CommonPrinter(Printer):
    def to_string(self):
        self.type = self.node_type()
        return cast2ptr(self.val.address, self.type).dereference()

# printer for basic object
class NodePrinterGnerator(PrinterGenerator):
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

    def common_children(self):
        for field in self.val.type.fields():
            if self.printable(field.name):
                # char * printed in common_to_string
                if str(field.type) != 'char *':

                    # Relids is def of Bitmapset *, print it
                    if str(field.type) == 'Relids' and self.val[field.name] != 0:
                        yield (field.name, cast2ptr(self.val[field.name], 'Bitmapset').dereference())

                    elif field.type.code == gdb.TYPE_CODE_PTR and self.val[field.name] != 0:

                        #  get type and convert it
                        type = self.get_type(self.val[field.name])

                        # convert to base type
                        base_type = self.get_convertable_type(type)
                        if base_type:
                            yield (field.name, cast2ptr(self.val[field.name], base_type).dereference())
                        else:
                            yield (field.name, self.val[field.name].dereference())

class Gnerator:
    def __init__(self) -> None:
        self.printer_nodes = [
            'Alias',              'RangeVar',             'TableFunc',        'IntoClause',            'Var',
            'Const',              'Param',            'Aggref',               'GroupingFunc',         'WindowFunc',         'WindowFuncRunCondition',
            'MergeSupportFunc',   'SubscriptingRef', 'FuncExpr',  'NamedArgExpr',   'OpExpr',  'DistinctExpr',   'NullIfExpr',  'ScalarArrayOpExpr',  'BoolExpr',   'SubLink',
            'SubPlan',            'AlternativeSubPlan',           'FieldSelect',      'FieldStore',           'RelabelType',         'CoerceViaIO',         'ArrayCoerceExpr',     'ConvertRowtypeExpr',        'CollateExpr',
            'CaseExpr',           'CaseWhen',         'CaseTestExpr',     'ArrayExpr',       'RowExpr',        'RowCompareExpr',         'CoalesceExpr',
            'MinMaxExpr',         'SQLValueFunction',         'XmlExpr',      'JsonFormat',        'JsonReturning',        'JsonValueExpr',
            'JsonConstructorExpr',    'JsonIsPredicate',  'JsonBehavior',   'JsonExpr',    'JsonTablePath',    'JsonTablePathScan',    'JsonTableSiblingJoin', 'NullTest',
            'BooleanTest',        'MergeAction',      'CoerceToDomain',   'CoerceToDomainValue',    'SetToDefault',      'CurrentOfExpr',      'NextValueExpr',      'InferenceElem',
            'TargetEntry',        'RangeTblRef',      'JoinExpr',     'FromExpr',       'OnConflictExpr',      'Query',       'TypeName',     'ColumnRef',
            'ParamRef',           'A_Expr',                 'TypeCast',        'CollateClause',    'RoleSpec',      'FuncCall',        'A_Indices',
            'A_Indirection',      'A_ArrayExpr',      'ResTarget',      'MultiAssignRef',     'SortBy',     'WindowDef',   'RangeSubselect',    'RangeFunction',   'RangeTableFunc',
            'RangeTableFuncCol',  'RangeTableSample',   'ColumnDef',   'TableLikeClause', 'IndexElem', 'DefElem',   'LockingClause',
            'XmlSerialize',       'PartitionElem',    'PartitionSpec',     'PartitionBoundSpec',     'PartitionRangeDatum',     'SinglePartitionSpec',   'PartitionCmd',
            'RangeTblEntry',      'RTEPermissionInfo',    'RangeTblFunction',       'TableSampleClause',    'WithCheckOption',   'SortGroupClause',    'GroupingSet',
            'WindowClause',       'RowMarkClause',    'WithClause',    'InferClause',        'OnConflictClause',     'CTESearchClause',      'CTECycleClause',
            'CommonTableExpr',    'MergeWhenClause',  'TriggerTransition',  'JsonOutput', 'JsonArgument',  'JsonFuncExpr',   'JsonTablePathSpec',   'JsonTable',
            'JsonTableColumn',    'JsonKeyValue', 'JsonParseExpr', 'JsonScalarExpr',    'JsonSerializeExpr',    'JsonObjectConstructor',    'JsonArrayConstructor', 'JsonArrayQueryConstructor',
            'JsonAggConstructor', 'JsonObjectAgg', 'JsonArrayAgg',  'RawStmt',    'InsertStmt',   'DeleteStmt',  'UpdateStmt', 'MergeStmt',
            'SelectStmt',         'SetOperationStmt',         'ReturnStmt',   'PLAssignStmt',          'CreateSchemaStmt',         'AlterTableStmt',       'ReplicaIdentityStmt',
            'AlterTableCmd',      'AlterCollationStmt',   'AlterDomainStmt',    'GrantStmt',     'ObjectWithArgs',     'AccessPriv',  'GrantRoleStmt',
            'AlterDefaultPrivilegesStmt', 'CopyStmt',  'VariableSetStmt',    'VariableShowStmt', 'CreateStmt',    'Constraint',   'CreateTableSpaceStmt',
            'DropTableSpaceStmt', 'AlterTableSpaceOptionsStmt',    'AlterTableMoveAllStmt',    'CreateExtensionStmt',  'AlterExtensionStmt', 'AlterExtensionContentsStmt',    'CreateFdwStmt',
            'AlterFdwStmt',       'CreateForeignServerStmt',  'AlterForeignServerStmt',        'CreateForeignTableStmt',       'CreateUserMappingStmt',    'AlterUserMappingStmt',
            'DropUserMappingStmt',  'ImportForeignSchemaStmt',    'CreatePolicyStmt', 'AlterPolicyStmt',   'CreateAmStmt',    'CreateTrigStmt',
            'CreateEventTrigStmt',    'AlterEventTrigStmt',   'CreatePLangStmt', 'CreateRoleStmt',    'AlterRoleStmt',    'AlterRoleSetStmt', 'DropRoleStmt',  'CreateSeqStmt',
            'AlterSeqStmt',       'DefineStmt',  'CreateDomainStmt',   'CreateOpClassStmt',   'CreateOpClassItem',   'CreateOpFamilyStmt',
            'AlterOpFamilyStmt',  'DropStmt',   'TruncateStmt',    'CommentStmt',  'SecLabelStmt',   'DeclareCursorStmt',   'ClosePortalStmt', 'FetchStmt', 'IndexStmt',
            'CreateStatsStmt',    'StatsElem',    'AlterStatsStmt',   'CreateFunctionStmt',  'FunctionParameter',  'AlterFunctionStmt',  'DoStmt', 'InlineCodeBlock',   'CallStmt',
            'CallContext',        'RenameStmt',       'AlterObjectDependsStmt',   'AlterObjectSchemaStmt',     'AlterOwnerStmt',  'AlterOperatorStmt',     'AlterTypeStmt',
            'RuleStmt',           'NotifyStmt',           'ListenStmt',       'UnlistenStmt',          'TransactionStmt',        'CompositeTypeStmt',      'CreateEnumStmt',
            'CreateRangeStmt',          'AlterEnumStmt',        'ViewStmt',      'LoadStmt',      'CreatedbStmt',         'AlterDatabaseStmt',       'AlterDatabaseRefreshCollStmt',
            'AlterDatabaseSetStmt',      'DropdbStmt',        'AlterSystemStmt',      'ClusterStmt',     'VacuumStmt',        'VacuumRelation',       'ExplainStmt',        'CreateTableAsStmt',
            'RefreshMatViewStmt',      'CheckPointStmt',      'DiscardStmt',        'LockStmt',        'ConstraintsSetStmt',        'ReindexStmt',        'CreateConversionStmt',
            'CreateCastStmt',      'CreateTransformStmt',          'PrepareStmt',     'ExecuteStmt',         'DeallocateStmt',     'DropOwnedStmt',      'ReassignOwnedStmt',
            'AlterTSDictionaryStmt',      'AlterTSConfigurationStmt',      'PublicationTable',       'PublicationObjSpec',        'CreatePublicationStmt',       'AlterPublicationStmt',
            'CreateSubscriptionStmt',         'AlterSubscriptionStmt',      'DropSubscriptionStmt',       'PlannerGlobal',
            'PlannerInfo',        'RelOptInfo',       'IndexOptInfo',     'ForeignKeyOptInfo',     'StatisticExtInfo',  'JoinDomain',        'EquivalenceClass',     'EquivalenceMember',
            'PathKey',     'PathKeyInfo',    'PathTarget',      'ParamPathInfo',        'IndexClause',          'PlannedStmt',   'PlanRowMark', 'NestLoopParam',     
            'GroupingSetData',      'RollupData', 'RestrictInfo',     'PlaceHolderVar',  'SpecialJoinInfo',
            'OuterJoinClauseInfo',  'AppendRelInfo',     'RowIdentityVarInfo',       'PlaceHolderInfo',     'MinMaxAggInfo',   'PlannerParamItem',      'AggInfo',     'AggTransInfo',
            'PartitionPruneInfo',  'PartitionedRelPruneInfo',    'PartitionPruneStepOp', 'PartitionPruneStepCombine', 'PlanInvalItem', 'ExprState', 'IndexInfo', 'ExprContext',
            'ReturnSetInfo',   'ProjectionInfo',  'JunkFilter', 'OnConflictSetState',    'MergeActionState', 'ResultRelInfo', 'EState',    'WindowFuncExprState',  'SetExprState',
            'SubPlanState',    'DomainConstraintState',    'ResultState',  'ProjectSetState',    'ModifyTableState', 'AppendState',   'MergeAppendState',    'RecursiveUnionState',
            'BitmapAndState', 'BitmapOrState', 'ScanState', 'SeqScanState',  'SampleScanState',    'IndexScanState',   'IndexOnlyScanState',  'BitmapIndexScanState',   'BitmapHeapScanState',
            'TidScanState',  'TidRangeScanState',  'SubqueryScanState',  'FunctionScanState',  'ValuesScanState',    'TableFuncScanState',   'CteScanState',    'NamedTuplestoreScanState',
            'WorkTableScanState',    'ForeignScanState', 'CustomScanState',   'JoinState',   'NestLoopState',   'MergeJoinState',  'HashJoinState',  'MaterialState',  'MemoizeState',
            'SortState',   'IncrementalSortState',    'GroupState',   'AggState',    'WindowAggState',   'UniqueState', 'GatherState',   'GatherMergeState',    'HashState',    'SetOpState',
            'LockRowsState',   'LimitState',  'IndexAmRoutine', 'TableAmRoutine',    'TsmRoutine',   'EventTriggerData',    'TriggerData',  'TupleTableSlot', 'FdwRoutine',
            'ExtensibleNode',   'ErrorSaveContext',    'IdentifySystemCmd',    'BaseBackupCmd',    'CreateReplicationSlotCmd', 'DropReplicationSlotCmd',    'AlterReplicationSlotCmd',
            'StartReplicationCmd',    'ReadReplicationSlotCmd',   'TimeLineHistoryCmd',  'UploadManifestCmd',  'SupportRequestSimplify', 'SupportRequestSelectivity', 'SupportRequestCost',
            'SupportRequestRows',   'SupportRequestIndexCondition',    'SupportRequestWFuncMonotonic', 'SupportRequestOptimizeWindowClause',    'Integer',  'Float',  'Boolean',    'String',
            'BitString',   'ForeignKeyCacheInfo',     'AllocSetContext', 'GenerationContext', 'SlabContext',   'BumpContext',
            'TIDBitmap', 'WindowObjectData']

        self.path_nodes = [
            'Path', 'AggPath', 'MinMaxAggPath', 'WindowAggPath', 'SetOpPath', 'RecursiveUnionPath', 'LockRowsPath', 'ModifyTablePath', 'LimitPath',
            'GatherMergePath', 'NestPath', 'IndexPath', 'BitmapHeapPath', 'BitmapAndPath', 'MergeAppendPath', 'BitmapOrPath', 'GroupResultPath',
            'TidPath', 'TidRangePath', 'SubqueryScanPath', 'ForeignPath', 'CustomPath', 'AppendPath', 'MaterialPath', 'SortPath', 'ProjectSetPath',
            'ProjectionPath', 'HashPath', 'MergePath', 'GatherPath', 'UniquePath', 'MemoizePath', 'GroupingSetsPath', 'UpperUniquePath', 'GroupPath',
            'IncrementalSortPath',
        ]

        self.plan_nodes = [
            'Plan', 'Join', 'Result', 'ProjectSet', 'ModifyTable', 'Append', 'MergeAppend',  'RecursiveUnion', 'BitmapAnd', 'BitmapOr', 'Scan', 'SeqScan', 'SampleScan',
            'IndexScan', 'IndexOnlyScan', 'BitmapIndexScan', 'BitmapHeapScan', 'TidScan', 'TidRangeScan', 'SubqueryScan', 'FunctionScan', 'ValuesScan', 'TableFuncScan', 'CteScan',
            'NamedTuplestoreScan', 'WorkTableScan', 'ForeignScan', 'CustomScan', 'NestLoop',  'MergeJoin', 'HashJoin', 'Material', 'Memoize',
            'Sort', 'IncrementalSort', 'Group', 'Agg', 'WindowAgg', 'Unique', 'Gather', 'GatherMerge', 'Hash', 'SetOp', 'LockRows', 'Limit',
        ]

    def gen_printer(self, name, BasePrinter):
        class Printer(BasePrinter):
            def to_string(self):
                return self.common_to_string()

            def children(self):
                return self.common_children()

        Printer.__name__ = name
        return Printer

    def gnerator(self):
        [printer.add_printer(node, '^' + node + '$', self.gen_printer(node, NodePrinterGnerator)) for node in self.printer_nodes]
        [printer.add_printer(node, '^' + node + '$', self.gen_printer(node, PathPrinterGenerator)) for node in self.path_nodes]
        [printer.add_printer(node, '^' + node + '$', self.gen_printer(node, PlanPrinterGenerator)) for node in self.plan_nodes]

gen = Gnerator()
gen.gnerator()

def register_postgres_printers(obj):
    gdb.printing.register_pretty_printer(obj, printer, True)
