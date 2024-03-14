import gdb
import string
import re
import os
import sys
from functools import reduce
import operator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from node_struct import *

printer = gdb.printing.RegexpCollectionPrettyPrinter('REL_16_STABLE')

def register_printer(name):
    def __registe(_printer):
        printer.add_printer(name, '^' + name + '$', _printer)
    return __registe

def getTypeOutputInfo(t_oid):
    tupe = gdb.parse_and_eval('SearchSysCache1(TYPEOID, {})'.format(t_oid))
    tp = gdb.parse_and_eval('(Form_pg_type){}'.format(int(tupe['t_data']) + int(tupe['t_data']['t_hoff'])))
    gdb.parse_and_eval('ReleaseSysCache({})'.format(tupe.dereference().address))
    return [int(tp['typoutput']), (not bool(tp['typbyval'])) and int(tp['typlen']) == -1]

def cast(node, type_name):
    t = gdb.lookup_type(type_name)
    return node.cast(t.pointer())

def list_length(node):
    return int(node['length'])

def cast_to_pod(node, type):
    return node.cast(gdb.lookup_type(type))

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

class BasePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def get_item(self, field):
        f = field.split('.')
        return reduce(operator.getitem, f, self.val)

    def print_to_string(self, header, field):
        if len(field) == 0:
            return header
        head = header
        if re.search('path\.', field[0][1]):
            f = field[0][1].split('.')[:-1]
            head += self.path_to_string(reduce(operator.getitem, f, self.val)) + ' '
            field = [x for x in field if not re.search('path\.', x[1])]
        elif re.search('plan\.', field[0][1]):
            f = field[0][1].split('.')[:-1]
            head += self.plan_to_string(reduce(operator.getitem, f, self.val)) + ' '
            field = [x for x in field if not re.search('plan\.', x[1])]

        size = len(field)
        if size > 1:
            head += '{'

        ss = []
        for arg in field:
            if arg[0] == 'QualCost':
                s = '{}: ({:.2f}..{:.2f})'.format(arg[1], float(self.get_item(arg[1])['startup']), float(self.get_item(arg[1])['per_tuple']))
            elif arg[0] == 'Bitmapset*':
                s = '%s: %s' % (arg[1], '0x0'if str(self.get_item(arg[1])) == '0x0' else self.get_item(arg[1]).dereference())
            elif arg[0] == 'Selectivity':
                s = '{}: {:.4f}'.format(arg[1], float(self.get_item(arg[1])))
            else:
                s = '{}: {}'.format(arg[1], getchars(self.get_item(arg[1])) if arg[0] == 'char*' else self.get_item(arg[1]))
            ss.append(s)

        head += ', '.join(ss)

        if size > 1:
            head += '}'

        return head
    
    def add_to_list(self, list, arg):
        k = arg.split('.')
        v = reduce(operator.getitem, k, self.val)
        if str(v) != '0x0':
            if re.search('^parent$', k[-1]):
                list += [(arg, v['relids'])]
            else:
                list += [(arg, v.dereference())]

    def print_children(self, field):
        list = []
        for arg in field:
            self.add_to_list(list, arg[1])
        return list
    
    def print_children_array(self, k, v):
        list = []
        size = 0
        if k[0:11] == 'list_length':
            val = self.val[str(k[k.index('(') + 1 : k.index(')')])]
            if str(val) != '0x0':
                size = int(list_length(val))
        else:
            size = int(self.get_item(k)) 

        if size != 0:
            for arg in v:
                a_type = arg[0].split('[')[0]
                if str(self.get_item(arg[1])) != '0x0':
                    if a_type == 'bool':
                        list.append((arg[1], str([bool(self.get_item(arg[1])[i]) for i in range(size)])))
                    # if a_type in ['AttrNumber', 'Index', 'Oid', 'int']:
                    else:
                        list.append((arg[1], str([int(self.get_item(arg[1])[i]) for i in range(size)])))
        return list

    def plan_to_string(self, plan):
        return '(cost={:.2f}..{:.2f} rows={:.0f} width={:.0f} async_capable={} plan_id={} parallel_aware={} parallel_safe = {})'.format(
            float(plan['startup_cost']),
            float(plan['total_cost']),
            float(plan['plan_rows']),
            float(plan['plan_width']),
            int(plan['async_capable']),
            int(plan['plan_node_id']),
            bool(plan['parallel_aware']),
            bool(plan['parallel_safe'])
        )
    
    def path_to_string(self, path):
        return '{} (cost={:.2f}..{:.2f} rows={:.0f} parallel_aware={} parallel_safe={} parallel_workers={})'.format(
            path['pathtype'],
            float(path['startup_cost']),
            float(path['total_cost']),
            float(path['rows']),
            bool(path['parallel_aware']),
            bool(path['parallel_safe']),
            int(path['parallel_workers']),
        )

    def display_hint(self):
        return ''

def bms_next_member(val, prevbit, bit_per_w):
    if str(val) == '0x0':
        return -2

    nwords = val['nwords']
    prevbit += 1
    mm = 0
    if bit_per_w == 64:
        mm = 0xFFFFFFFFFFFFFFFF
    else:
        mm = 0xFFFFFFFF

    mask = (mm << int(prevbit % bit_per_w)) & mm

    for wordnum in range(prevbit // bit_per_w, nwords):
        w = int(val['words'][wordnum] & mask)
        if w != 0:
            return int(wordnum * bit_per_w + w.bit_length() - len(bin(w).rstrip('0')) + 2)
        mask = mm
    return -2

@register_printer('Bitmapset')
class BitmapsetPrinter(BasePrinter):
    def to_string(self):
        return getchars(gdb.parse_and_eval('nodeToString({})'.format(self.val.reference_value().address)), False)
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

@register_printer('Relids')
class RelidsPrinter(BasePrinter):
    def to_string(self):
        return getchars(gdb.parse_and_eval('nodeToString({})'.format(self.val.referenced_value().address)), False)

pl = {
    'Alias': Alias,                         'RangeVar': RangeVar,               'TableFunc': TableFunc,             'IntoClause': IntoClause,
    'Var': Var,                             'Const': Const,                     'Param': Param,                     'Aggref': Aggref,
    'GroupingFunc': GroupingFunc,           'WindowFunc': WindowFunc,           'SubscriptingRef': SubscriptingRef, 'FuncExpr': FuncExpr,
    'NamedArgExpr': NamedArgExpr,           'OpExpr': OpExpr,                   'DistinctExpr': DistinctExpr,       'NullIfExpr': NullIfExpr,
    'FieldStore': FieldStore,               'RelabelType': RelabelType,         'CoerceViaIO': CoerceViaIO,         'ArrayCoerceExpr': ArrayCoerceExpr,
    'CaseWhen': CaseWhen,                   'CaseTestExpr': CaseTestExpr,       'ArrayExpr': ArrayExpr,             'RowExpr': RowExpr,
    'RowCompareExpr': RowCompareExpr,       'CoalesceExpr': CoalesceExpr,       'MinMaxExpr': MinMaxExpr,           'SubLink': SubLink,
    'SQLValueFunction': SQLValueFunction,   'XmlExpr': XmlExpr,                 'JsonFormat': JsonFormat,           'JsonReturning': JsonReturning,                                     'JsonValueExpr': JsonValueExpr,
    'ScalarArrayOpExpr': ScalarArrayOpExpr,                     'BoolExpr': BoolExpr,                   
    'ConvertRowtypeExpr': ConvertRowtypeExpr,                   'CollateExpr': CollateExpr,             'CaseExpr': CaseExpr,
    'JsonConstructorExpr': JsonConstructorExpr,
    'JsonIsPredicate': JsonIsPredicate,    'NullTest': NullTest,    'BooleanTest': BooleanTest,
    'SubPlan': SubPlan,             'AlternativeSubPlan': AlternativeSubPlan,                       'FieldSelect': FieldSelect,
    'CoerceToDomain': CoerceToDomain,    'CoerceToDomainValue': CoerceToDomainValue,    'SetToDefault': SetToDefault,
    'CurrentOfExpr': CurrentOfExpr,    'NextValueExpr': NextValueExpr,    'InferenceElem': InferenceElem,    'TargetEntry': TargetEntry,
    'RangeTblRef': RangeTblRef,    'JoinExpr': JoinExpr,    'FromExpr': FromExpr,
    'OnConflictExpr': OnConflictExpr,
    'Query': Query,    'TypeName': TypeName,    'ColumnRef': ColumnRef,
    'ParamRef': ParamRef,    'A_Expr': A_Expr,    'A_Const': A_Const,
    'TypeCast': TypeCast,    'CollateClause': CollateClause,    'RoleSpec': RoleSpec,    'FuncCall': FuncCall,   
    'A_Indices': A_Indices,    'A_Indirection': A_Indirection,    'A_ArrayExpr': A_ArrayExpr,
    'ResTarget': ResTarget,    'MultiAssignRef': MultiAssignRef,    'SortBy': SortBy,    'WindowDef': WindowDef,
    'RangeSubselect': RangeSubselect,    'RangeFunction': RangeFunction,    'RangeTableFunc': RangeTableFunc,
    'RangeTableFuncCol': RangeTableFuncCol,    'RangeTableSample': RangeTableSample,    'ColumnDef': ColumnDef,    'TableLikeClause': TableLikeClause,
    'IndexElem': IndexElem,    'DefElem': DefElem,    'LockingClause': LockingClause,
    'XmlSerialize': XmlSerialize,    'PartitionElem': PartitionElem,    'PartitionSpec': PartitionSpec,
    'PartitionBoundSpec': PartitionBoundSpec,    'PartitionRangeDatum': PartitionRangeDatum,
    'PartitionCmd': PartitionCmd,    'RangeTblEntry': RangeTblEntry,    'RTEPermissionInfo': RTEPermissionInfo,
    'RangeTblFunction': RangeTblFunction,    'TableSampleClause': TableSampleClause,    'WithCheckOption': WithCheckOption,
    'SortGroupClause': SortGroupClause,
    'GroupingSet': GroupingSet,    'WindowClause': WindowClause,    'RowMarkClause': RowMarkClause,
    'WithClause': WithClause,    'InferClause': InferClause,    'OnConflictClause': OnConflictClause,
    'CTESearchClause': CTESearchClause,    'CTECycleClause': CTECycleClause,    'CommonTableExpr': CommonTableExpr,
    'MergeWhenClause': MergeWhenClause,    'MergeAction': MergeAction,    'TriggerTransition': TriggerTransition,
    'JsonOutput': JsonOutput,    'JsonKeyValue': JsonKeyValue,    'JsonObjectConstructor': JsonObjectConstructor,
    'JsonArrayConstructor': JsonArrayConstructor,    'JsonArrayQueryConstructor': JsonArrayQueryConstructor,    'JsonAggConstructor': JsonAggConstructor,
    'JsonObjectAgg': JsonObjectAgg,    'JsonArrayAgg': JsonArrayAgg,    'RawStmt': RawStmt,
    'InsertStmt': InsertStmt,    'DeleteStmt': DeleteStmt,    'UpdateStmt': UpdateStmt,
    'MergeStmt': MergeStmt,    'SelectStmt': SelectStmt,    'SetOperationStmt': SetOperationStmt,
    'ReturnStmt': ReturnStmt,    'PLAssignStmt': PLAssignStmt,    'CreateSchemaStmt': CreateSchemaStmt,
    'AlterTableStmt': AlterTableStmt,    'ReplicaIdentityStmt': ReplicaIdentityStmt,    'AlterTableCmd': AlterTableCmd,
    'AlterCollationStmt': AlterCollationStmt,    'AlterDomainStmt': AlterDomainStmt,    'GrantStmt': GrantStmt,
    'ObjectWithArgs': ObjectWithArgs,    'AccessPriv': AccessPriv,    'GrantRoleStmt': GrantRoleStmt,
    'AlterDefaultPrivilegesStmt': AlterDefaultPrivilegesStmt,    'CopyStmt': CopyStmt,    'VariableSetStmt': VariableSetStmt,
    'VariableShowStmt': VariableShowStmt,    'CreateStmt': CreateStmt,    'Constraint': Constraint,
    'CreateTableSpaceStmt': CreateTableSpaceStmt,    'DropTableSpaceStmt': DropTableSpaceStmt,    'AlterTableSpaceOptionsStmt': AlterTableSpaceOptionsStmt,
    'AlterTableMoveAllStmt': AlterTableMoveAllStmt,    'CreateExtensionStmt': CreateExtensionStmt,    'AlterExtensionStmt': AlterExtensionStmt,
    'AlterExtensionContentsStmt': AlterExtensionContentsStmt,    'CreateFdwStmt': CreateFdwStmt,    'AlterFdwStmt': AlterFdwStmt,
    'CreateForeignServerStmt': CreateForeignServerStmt,    'AlterForeignServerStmt': AlterForeignServerStmt,    'CreateForeignTableStmt': CreateForeignTableStmt,
    'CreateUserMappingStmt': CreateUserMappingStmt,    'AlterUserMappingStmt': AlterUserMappingStmt,    'DropUserMappingStmt': DropUserMappingStmt,
    'ImportForeignSchemaStmt': ImportForeignSchemaStmt,    'CreatePolicyStmt': CreatePolicyStmt,    'AlterPolicyStmt': AlterPolicyStmt,
    'CreateAmStmt': CreateAmStmt,    'CreateTrigStmt': CreateTrigStmt,    'CreateEventTrigStmt': CreateEventTrigStmt,
    'AlterEventTrigStmt': AlterEventTrigStmt,    'CreatePLangStmt': CreatePLangStmt,    'CreateRoleStmt': CreateRoleStmt,
    'AlterRoleStmt': AlterRoleStmt,    'AlterRoleSetStmt': AlterRoleSetStmt,    'DropRoleStmt': DropRoleStmt,
    'CreateSeqStmt': CreateSeqStmt,    'AlterSeqStmt': AlterSeqStmt,    'DefineStmt': DefineStmt,
    'CreateDomainStmt': CreateDomainStmt,    'CreateOpClassStmt': CreateOpClassStmt,    'CreateOpClassItem': CreateOpClassItem,
    'CreateOpFamilyStmt': CreateOpFamilyStmt,    'AlterOpFamilyStmt': AlterOpFamilyStmt,    'DropStmt': DropStmt,
    'TruncateStmt': TruncateStmt,    'CommentStmt': CommentStmt,    'SecLabelStmt': SecLabelStmt,
    'DeclareCursorStmt': DeclareCursorStmt,    'ClosePortalStmt': ClosePortalStmt,    'FetchStmt': FetchStmt,
    'IndexStmt': IndexStmt,    'CreateStatsStmt': CreateStatsStmt,    'StatsElem': StatsElem,
    'AlterStatsStmt': AlterStatsStmt,    'CreateFunctionStmt': CreateFunctionStmt,    'FunctionParameter': FunctionParameter,
    'AlterFunctionStmt': AlterFunctionStmt,    'DoStmt': DoStmt,    'CallStmt': CallStmt,
    'RenameStmt': RenameStmt,    'AlterObjectDependsStmt': AlterObjectDependsStmt,    'AlterObjectSchemaStmt': AlterObjectSchemaStmt,
    'AlterOwnerStmt': AlterOwnerStmt,    'AlterOperatorStmt': AlterOperatorStmt,    'AlterTypeStmt': AlterTypeStmt,
    'RuleStmt': RuleStmt,    'NotifyStmt': NotifyStmt,    'ListenStmt': ListenStmt,
    'UnlistenStmt': UnlistenStmt,    'TransactionStmt': TransactionStmt,    'CompositeTypeStmt': CompositeTypeStmt,
    'CreateEnumStmt': CreateEnumStmt,    'CreateRangeStmt': CreateRangeStmt,    'AlterEnumStmt': AlterEnumStmt,
    'ViewStmt': ViewStmt,    'LoadStmt': LoadStmt,    'CreatedbStmt': CreatedbStmt,
    'AlterDatabaseStmt': AlterDatabaseStmt,    'AlterDatabaseRefreshCollStmt': AlterDatabaseRefreshCollStmt,    'AlterDatabaseSetStmt': AlterDatabaseSetStmt,
    'DropdbStmt': DropdbStmt,    'AlterSystemStmt': AlterSystemStmt,    'ClusterStmt': ClusterStmt,
    'VacuumStmt': VacuumStmt,
    'VacuumRelation': VacuumRelation,    'ExplainStmt': ExplainStmt,    'CreateTableAsStmt': CreateTableAsStmt,
    'RefreshMatViewStmt': RefreshMatViewStmt,     'DiscardStmt': DiscardStmt,
    'LockStmt': LockStmt,    'ConstraintsSetStmt': ConstraintsSetStmt,    'ReindexStmt': ReindexStmt,
    'CreateConversionStmt': CreateConversionStmt,    'CreateCastStmt': CreateCastStmt,    'CreateTransformStmt': CreateTransformStmt,
    'PrepareStmt': PrepareStmt,    'ExecuteStmt': ExecuteStmt,    'DeallocateStmt': DeallocateStmt,
    'DropOwnedStmt': DropOwnedStmt,    'ReassignOwnedStmt': ReassignOwnedStmt,    'AlterTSDictionaryStmt': AlterTSDictionaryStmt,
    'AlterTSConfigurationStmt': AlterTSConfigurationStmt,    'PublicationTable': PublicationTable,    'PublicationObjSpec': PublicationObjSpec,
    'CreatePublicationStmt': CreatePublicationStmt,    'AlterPublicationStmt': AlterPublicationStmt,    'CreateSubscriptionStmt': CreateSubscriptionStmt,
    'AlterSubscriptionStmt': AlterSubscriptionStmt,    'DropSubscriptionStmt': DropSubscriptionStmt,    'PlannerGlobal': PlannerGlobal,
    'PlannerInfo': PlannerInfo,    'RelOptInfo': RelOptInfo,
    'ForeignKeyOptInfo': ForeignKeyOptInfo,    'StatisticExtInfo': StatisticExtInfo,    'JoinDomain': JoinDomain,
    'EquivalenceClass': EquivalenceClass,    'EquivalenceMember': EquivalenceMember,    'PathKey': PathKey,    'PathTarget': PathTarget,    'ParamPathInfo': ParamPathInfo,
    'RestrictInfo': RestrictInfo,    'PlaceHolderVar': PlaceHolderVar,    'SpecialJoinInfo': SpecialJoinInfo,
    'OuterJoinClauseInfo': OuterJoinClauseInfo,    'AppendRelInfo': AppendRelInfo,    'RowIdentityVarInfo': RowIdentityVarInfo,
    'PlaceHolderInfo': PlaceHolderInfo,    'MinMaxAggInfo': MinMaxAggInfo,    'NestLoopParam': NestLoopParam,
    'PlannerParamItem': PlannerParamItem,    'AggInfo': AggInfo,    'AggTransInfo': AggTransInfo,
    'PlannedStmt': PlannedStmt,    'PlanRowMark': PlanRowMark,    'PartitionPruneInfo': PartitionPruneInfo,
    'PartitionedRelPruneInfo': PartitionedRelPruneInfo,    'PartitionPruneStep': PartitionPruneStep,    'PartitionPruneStepOp': PartitionPruneStepOp,
    'PartitionPruneStepCombine': PartitionPruneStepCombine,    'PlanInvalItem': PlanInvalItem,    'ExtensibleNode': ExtensibleNode,
    'ForeignKeyCacheInfo': ForeignKeyCacheInfo, 'IndexOptInfo': IndexOptInfo,

    # path
    'Path': Path,    'IndexPath': IndexPath,    'BitmapHeapPath': BitmapHeapPath,    'BitmapAndPath': BitmapAndPath,    'BitmapOrPath': BitmapOrPath,
    'TidPath': TidPath,    'SubqueryScanPath': SubqueryScanPath,    'ForeignPath': ForeignPath,    'CustomPath': CustomPath,
    'AppendPath': AppendPath,    'MergeAppendPath': MergeAppendPath,    'GroupResultPath': GroupResultPath,    'MaterialPath': MaterialPath,
    'UniquePath': UniquePath,    'GatherPath': GatherPath,    'GatherMergePath': GatherMergePath,    'ProjectionPath': ProjectionPath,
    'ProjectSetPath': ProjectSetPath,    'SortPath': SortPath,    'GroupPath': GroupPath,    'UpperUniquePath': UpperUniquePath,
    'AggPath': AggPath,    'GroupingSetsPath': GroupingSetsPath,    'MinMaxAggPath': MinMaxAggPath,    'WindowAggPath': WindowAggPath,
    'SetOpPath': SetOpPath,    'RecursiveUnionPath': RecursiveUnionPath,    'LockRowsPath': LockRowsPath,    'ModifyTablePath': ModifyTablePath,
    'LimitPath': LimitPath,    'MergePath': MergePath,    'HashPath': HashPath, 'JoinPath': JoinPath,  'NestPath': NestPath,

    # plan
    'Plan': Plan,    'Result': Result,    'ProjectSet': ProjectSet,    'ModifyTable': ModifyTable,    'Append': Append,    'MergeAppend': MergeAppend,
    'RecursiveUnion': RecursiveUnion,    'BitmapAnd': BitmapAnd,    'BitmapOr': BitmapOr,    'Scan': Scan,    'SeqScan': SeqScan,    'SampleScan': SampleScan,
    'IndexScan': IndexScan,    'IndexOnlyScan': IndexOnlyScan,    'BitmapIndexScan': BitmapIndexScan,    'BitmapHeapScan': BitmapHeapScan,
    'TidScan': TidScan,    'TidRangeScan': TidRangeScan,    'SubqueryScan': SubqueryScan,    'FunctionScan': FunctionScan,
    'ValuesScan': ValuesScan,    'TableFuncScan': TableFuncScan,    'CteScan': CteScan,    'NamedTuplestoreScan': NamedTuplestoreScan,
    'WorkTableScan': WorkTableScan,    'ForeignScan': ForeignScan,    'CustomScan': CustomScan,    'Material': Material,
    'Memoize': Memoize,    'Sort': Sort,    'Group': Group,    'Agg': Agg,    'WindowAgg': WindowAgg,
    'Unique': Unique,    'Gather': Gather,    'GatherMerge': GatherMerge,    'Hash': Hash,    'SetOp': SetOp,
    'LockRows': LockRows,    'Limit': Limit,    'NestLoop': NestLoop,    'MergeJoin': MergeJoin,    'HashJoin': HashJoin,
}

def split_field(s):
    pod_item = []
    pointer_item = []
    array_item = []

    for key, val in s:
        if re.search('\[', key):
            array_item.append([key, val])
        elif re.search('\*', key) and key != 'char*' and key != 'Bitmapset*':
            pointer_item.append([key, val])
        else:
            pod_item.append([key, val])

    return [pod_item, pointer_item, array_item]

def node_type(node):
    return str(node['type'])[2:]

def gen_printer_class(name, fields):
    class Printer(BasePrinter):
        def to_string(self):
            if name == 'Path':
                if node_type(self.val) == 'Path':
                    return self.path_to_string(self.val)
                else:
                    return cast(self.val.address, node_type(self.val)).dereference()
            elif name == 'Plan':
                return cast(self.val.address, node_type(self.val)).dereference()
            else:
                return self.print_to_string('%s ' % name, fields[0])

        def children(self):
            list = []
            if name == 'Path':
                if node_type(self.val) != 'Path':
                    return []
            elif name == 'Plan':
                return []
            if len(fields[2]) != 0:
                result = {}
                for t in fields[2]:
                    key = t[0][t[0].index('[') + 1 : t[0].index(']')]
                    if key in result:
                        result[key].append(t)
                    else:
                        result[key] = [t]

                for k, v in result.items():
                    list += self.print_children_array(k, v)

            return list + self.print_children(fields[1])

    Printer.__name__ = name
    return Printer

@register_printer('(Node|Expr)')
class CommonPrinter(BasePrinter):
    def to_string(self):
        self.type = node_type(self.val)
        return cast(self.val.address, self.type).dereference()

@register_printer('A_Star')
class A_StarPrinter(BasePrinter):
    def to_string(self):
        return '*'

def gen_val_printer_class(name):
    class Printer(BasePrinter):
        def to_string(self):
            vt = node_type(self.val)
            ret = ''
            if vt == 'Integer':
                ret += str(self.val['ival'])
            elif vt == 'Boolean':
                ret += bool(self.val['boolval'])
            elif vt == 'Float':
                ret += getchars(self.val['fval'])
            elif vt == 'String':
                ret += getchars(self.val['sval'])
            elif vt == 'BitString':
                ret += getchars(self.val['bsval'])
            return '{} [ {} ]'.format(vt, ret)

    Printer.__name__ = name
    return Printer

val_printer = ['Integer', 'Boolean', 'Float', 'String', 'BitString']

@register_printer('ValUnion')
class ValUnionPrinter(BasePrinter):
    def to_string(self):
        vt = str(self.val['node']['type'])[2:]
        ret = ''
        if vt == 'Integer':
            ret += str(self.val['ival']['ival'])
        elif vt == 'Float':
            ret += getchars(self.val['fval']['fval'])
        elif vt == 'Boolean':
            ret += str(self.val['boolval']['boolval'])
        elif vt == 'BitString':
            ret += getchars(self.val['bsval']['bsval'])
        elif vt == 'String':
            ret += getchars(self.val['sval']['sval'])
        return '{} [ {} ]'.format(vt, ret)

def generate_printer():
    for name, s in pl.items():
        pointerx = gen_printer_class(name, split_field(s))
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name in val_printer:
        pointerx = gen_val_printer_class(name)
        printer.add_printer(name, '^' + name + '$', pointerx)

generate_printer()


class ListIt(object):
    def __init__(self, list) -> None:
        self.elements = list['elements']
        self.size = list['length']
        self.count = 0

    def __iter__(self):
        return self

    def __len__(self):
        return int(self.size)

    def __next__(self):
        if self.count == self.size:
            raise StopIteration

        node = self.elements[self.count]
        self.count += 1
        return node


@register_printer('List')
class ListPrinter:
    class _iter(object):
        def __init__(self, it, type) -> None:
            self.it = it
            self.type = type
            self.count = 0

        def __iter__(self):
            return self

        def __next__(self):
            node = next(self.it)
            if str(self.type) == 'List':
                node = cast(node['ptr_value'], 'Node').dereference()
            elif str(self.type) == 'IntList':
                node = int(node['int_value'])
            else:
                node = int(node['oid_value'])

            result = (str(self.count), node)
            self.count += 1
            return result

    def __init__(self,  val) -> None:
        self.val = val
        self.type = str(self.val['type'])[2:]

    def to_string(self):
        return '%s with %s elements' % (self.type, self.val['length'])

    def children(self):
        return self._iter(ListIt(self.val), self.type)

    def display_hint(self):
        if self.type == 'List':
            return None
        else:
            return 'array'



# @register_printer('Const')
# class ConstPrinter(BasePrinter):
#     def to_string(self):
#         if bool(self.val['constisnull']) == True:
#             return 'Null'
#         else:
#             pfunc = getTypeOutputInfo(int(self.val['consttype']))
#             return str(gdb.parse_and_eval('OidOutputFunctionCall({}, {})'.format(pfunc[0], int(self.val['constvalue']))).dereference())

class Printer(BasePrinter):
    def to_string(self):
        return getchars(gdb.parse_and_eval('pretty_format_node_dump(nodeToString({}))'.format(self.val.reference_value().address)), False, 100000000)
            
printer.add_printer('AnyNode', '^Node$', Printer)


gdb.printing.register_pretty_printer(
    gdb.current_objfile(),
    printer, True)

class printVerbose(gdb.Parameter):
    def __init__(self) -> None:
        super(printVerbose, self).__init__('print pg_pretty', gdb.COMMAND_DATA, gdb.PARAM_ENUM, ['off', 'origin', 'trace', 'info'])
        self.value = 'trace'

    def get_set_string(self) -> str:
        if self.value == 'off':
            for p in printer.subprinters:
                p.enabled = False
            return 'All printers are disabled, just print the object with default behavior'
        elif self.value == 'origin':
            for p in printer.subprinters:
                p.enabled = False
                if p.name == 'AnyNode':
                    p.enabled = True
            return 'Print all objects that inherit from ''Node'' using the built-in ''pprint'' function, attention, this will not used while gdb a core file'
        elif self.value == 'trace':
            for p in printer.subprinters:
                p.enabled = True
                if p.name == 'AnyNode':
                    p.enabled = False
            return 'Print all objects like ''pprint'' but in python, work anywhere'
        elif self.value == 'info':
            for p in printer.subprinters:
                if p.name == 'AnyNode':
                    p.enabled = False
            return 'Trying to call some built-in functions to simple object, but may loss of information'

    def get_show_string(self, pvalue):
        if self.value == 'off':
            return 'Current value is {}, All printers are disabled, just print the object with default behavior'.format(self.value)
        elif self.value == 'origin':
            return 'Current value is {}, Print all objects that inherit from ''Node'' using the built-in ''pprint'' function, attention, this will not used while gdb a core file'.format(self.value)
        elif self.value == 'trace':
            return 'Current value is {}, Print all objects like ''pprint'' but in python, work anywhere'.format(self.value)
        elif self.value == 'info':
            return 'Current value is {}, Trying to call some built-in functions to simple object, but may loss of information'.format(self.value)

printVerbose()
