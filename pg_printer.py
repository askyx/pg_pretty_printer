import gdb
import string
import re
import os
import sys

# TODO: some no printer filed add to child

current_file_path = os.path.abspath(__file__)

current_dir = os.path.dirname(current_file_path)

if current_dir not in sys.path:
    sys.path.append(current_dir)

from node_struct import *

printer = gdb.printing.RegexpCollectionPrettyPrinter("Greenplum-7.0.0")

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

def add_list(list, val, filde):
    if str(val[filde]) != '0x0':
        list.append((filde, val[filde].dereference()))

# max print 100
def getchars(arg, qoute = True, len = 100):
    if (str(arg) == '0x0'):
        return str(arg)

    retval = ''
    if qoute:
        retval += '\''

    i = 0
    while arg[i] != ord("\0") and i < len:
        character = int(arg[i].cast(gdb.lookup_type("char")))
        if chr(character) in string.printable:
            retval += "%c" % chr(character)
        else:
            retval += "\\x%x" % character
        i += 1

    if qoute:
        retval += '\''

    return retval

class BasePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def print_to_string(self, header, field):
        pod = field
        size = len(pod)
        ret = header
        if size > 1:
            ret += '{'

        ss = []
        for arg in pod:
            if arg[0] == 'QualCost':
                s = '{}: ({:.2f}..{:.2f})'.format(arg[1], float(self.val[arg[1]]['startup']), float(self.val[arg[1]]['per_tuple']))
            else:
                s = '%s: %s' % (arg[1], getchars(self.val[arg[1]]) if arg[0] == 'char*' else self.val[arg[1]])
            ss.append(s)

        ret += ', '.join(ss)

        if size > 1:
            ret += '}'

        return ret
    
    def print_children(self, field):
        list = []
        for arg in field:
            add_list(list, self.val, arg[1])
        return list
    
    def plan_to_string(self, type, plan):
        return '{} (cost={:.2f}..{:.2f} rows={:.0f} width={:.0f} memo={} plan_id={} parallel_aware={} parallel_safe = {})'.format(
            str(type),
            float(plan['startup_cost']),
            float(plan['total_cost']),
            float(plan['plan_rows']),
            float(plan['plan_width']),
            int(plan['operatorMemKB']),
            int(plan['plan_node_id']),
            bool(plan['parallel_aware']),
            bool(plan['parallel_safe'])
        )
    
    def plan_children(self, plan):
        list = []
        add_list(list, plan, 'targetlist')
        add_list(list, plan, 'qual')
        add_list(list, plan, 'initPlan')
        add_list(list, plan, 'extParam')
        add_list(list, plan, 'allParam')
        add_list(list, plan, 'flow')
        add_list(list, plan, 'lefttree')
        add_list(list, plan, 'righttree')
        return list
    
    def path_to_string(self, type, path):
        return '{} {} (cost={:.2f}..{:.2f} rows={:.0f} memo={} parallel_aware={} parallel_safe={} parallel_workers={} motionHazard={} rescannable={} sameslice_relids={})'.format(
            type,
            path['pathtype'],
            float(path['startup_cost']),
            float(path['total_cost']),
            float(path['rows']),
            float(path['memory']),
            bool(path['parallel_aware']),
            bool(path['parallel_safe']),
            int(path['parallel_workers']),
            bool(path['motionHazard']),
            bool(path['rescannable']),
            path['sameslice_relids']
        )

    #  RelOptInfo is so huge
    def path_children(self, path):
        list = []
        list.append(('locus', path['locus']))
        add_list(list, path, 'pathtarget')
        add_list(list, path, 'param_info')
        add_list(list, path, 'pathkeys')
        return list

    def join_to_string(self, type):
        ext = ' inner_unique: {} prefetch_inner: {}'.format(self.val['join']['inner_unique'], self.val['join']['prefetch_inner'])
        return type + ' ' + self.plan_to_string(self.val['join']['jointype'], self.val['join']['plan']) + ext

    def join_children(self):
        list = self.plan_children(self.val['join']['plan'])
        add_list(list, self.val['join'], 'joinqual')
        return list

    def jpath_to_string(self, type):
        ext = ' inner_unique: {}'.format(self.val['jpath']['inner_unique'])
        return type + ' ' + self.path_to_string(self.val['jpath']['jointype'], self.val['jpath']['path']) + ext

    def jpath_children(self):
        list = self.path_children(self.val['jpath']['path'])
        add_list(list, self.val['jpath'], 'joinrestrictinfo')
        add_list(list, self.val['jpath'], 'outerjoinpath')
        add_list(list, self.val['jpath'], 'innerjoinpath')
        return list

    def display_hint(self):
        return ''

@register_printer('Bitmapset')
class BitmapsetPrinter(BasePrinter):
    def to_string(self):
        list = []
        index = int(gdb.parse_and_eval('bms_next_member({}, {})'.format(self.val.reference_value().address, -1)))
        while index >= 0:
            list.append(index)
            index = int(gdb.parse_and_eval('bms_next_member({}, {})'.format(self.val.reference_value().address, index)))

        return str(list)

@register_printer('Relids')
class RelidsPrinter(BasePrinter):
    def to_string(self):
        return self.val.address.cast(gdb.lookup_type('Bitmapset').pointer()).dereference()

pl = {
    'Alias': Alias,                 'RangeVar': RangeVar,       'TableFunc': TableFunc,             'IntoClause': IntoClause,
    'Var': Var,                     'Const': Const,             'Param': Param,                     'Aggref': Aggref,
    'GroupingFunc': GroupingFunc,   'WindowFunc': WindowFunc,   'SubscriptingRef': SubscriptingRef, 'FuncExpr': FuncExpr,
    'NamedArgExpr': NamedArgExpr,   'OpExpr': OpExpr,           'DistinctExpr': DistinctExpr,       'NullIfExpr': NullIfExpr,
    'FieldStore': FieldStore,       'RelabelType': RelabelType, 'CoerceViaIO': CoerceViaIO,         'ArrayCoerceExpr': ArrayCoerceExpr,
    'ScalarArrayOpExpr': ScalarArrayOpExpr,                     'BoolExpr': BoolExpr,               'SubLink': SubLink,
    'ConvertRowtypeExpr': ConvertRowtypeExpr,                   'CollateExpr': CollateExpr,         'CaseExpr': CaseExpr,
    'SubPlan': SubPlan,             'AlternativeSubPlan': AlternativeSubPlan,                       'FieldSelect': FieldSelect,
    'CaseWhen': CaseWhen,           'CaseTestExpr': CaseTestExpr,                                   'ArrayExpr': ArrayExpr,
    'RowExpr': RowExpr,             'RowCompareExpr': RowCompareExpr,                               'CoalesceExpr': CoalesceExpr,
    'MinMaxExpr': MinMaxExpr,       'SQLValueFunction': SQLValueFunction,                           'XmlExpr': XmlExpr,
    'JsonFormat': JsonFormat,       'JsonReturning': JsonReturning,                                 'JsonValueExpr': JsonValueExpr,
    'JsonConstructorExpr': JsonConstructorExpr,
    'JsonIsPredicate': JsonIsPredicate,    'NullTest': NullTest,    'BooleanTest': BooleanTest,
    'CoerceToDomain': CoerceToDomain,    'CoerceToDomainValue': CoerceToDomainValue,    'SetToDefault': SetToDefault,
    'CurrentOfExpr': CurrentOfExpr,    'NextValueExpr': NextValueExpr,    'InferenceElem': InferenceElem,    'TargetEntry': TargetEntry,
    'RangeTblRef': RangeTblRef,    'JoinExpr': JoinExpr,    'FromExpr': FromExpr,
    'OnConflictExpr': OnConflictExpr,
    'Query': Query,    'TypeName': TypeName,    'ColumnRef': ColumnRef,
    'ParamRef': ParamRef,    'A_Expr': A_Expr,    'A_Const': A_Const,
    'TypeCast': TypeCast,    'CollateClause': CollateClause,    'RoleSpec': RoleSpec,    'FuncCall': FuncCall,    'A_Star': A_Star,
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
    'RefreshMatViewStmt': RefreshMatViewStmt,    'CheckPointStmt': CheckPointStmt,    'DiscardStmt': DiscardStmt,
    'LockStmt': LockStmt,    'ConstraintsSetStmt': ConstraintsSetStmt,    'ReindexStmt': ReindexStmt,
    'CreateConversionStmt': CreateConversionStmt,    'CreateCastStmt': CreateCastStmt,    'CreateTransformStmt': CreateTransformStmt,
    'PrepareStmt': PrepareStmt,    'ExecuteStmt': ExecuteStmt,    'DeallocateStmt': DeallocateStmt,
    'DropOwnedStmt': DropOwnedStmt,    'ReassignOwnedStmt': ReassignOwnedStmt,    'AlterTSDictionaryStmt': AlterTSDictionaryStmt,
    'AlterTSConfigurationStmt': AlterTSConfigurationStmt,    'PublicationTable': PublicationTable,    'PublicationObjSpec': PublicationObjSpec,
    'CreatePublicationStmt': CreatePublicationStmt,    'AlterPublicationStmt': AlterPublicationStmt,    'CreateSubscriptionStmt': CreateSubscriptionStmt,
    'AlterSubscriptionStmt': AlterSubscriptionStmt,    'DropSubscriptionStmt': DropSubscriptionStmt,    'PlannerGlobal': PlannerGlobal,
    'PlannerInfo': PlannerInfo,    'RelOptInfo': RelOptInfo,    'IndexOptInfo': IndexOptInfo,
    'ForeignKeyOptInfo': ForeignKeyOptInfo,    'StatisticExtInfo': StatisticExtInfo,    'JoinDomain': JoinDomain,
    'EquivalenceClass': EquivalenceClass,    'EquivalenceMember': EquivalenceMember,    'PathKey': PathKey,    'PathTarget': PathTarget,    'ParamPathInfo': ParamPathInfo,
    'RestrictInfo': RestrictInfo,    'PlaceHolderVar': PlaceHolderVar,    'SpecialJoinInfo': SpecialJoinInfo,
    'OuterJoinClauseInfo': OuterJoinClauseInfo,    'AppendRelInfo': AppendRelInfo,    'RowIdentityVarInfo': RowIdentityVarInfo,
    'PlaceHolderInfo': PlaceHolderInfo,    'MinMaxAggInfo': MinMaxAggInfo,    'NestLoopParam': NestLoopParam,
    'PlannerParamItem': PlannerParamItem,    'AggInfo': AggInfo,    'AggTransInfo': AggTransInfo,
    'PlannedStmt': PlannedStmt,    'PlanRowMark': PlanRowMark,    'PartitionPruneInfo': PartitionPruneInfo,
    'PartitionedRelPruneInfo': PartitionedRelPruneInfo,    'PartitionPruneStep': PartitionPruneStep,    'PartitionPruneStepOp': PartitionPruneStepOp,
    'PartitionPruneStepCombine': PartitionPruneStepCombine,    'PlanInvalItem': PlanInvalItem,    'ExtensibleNode': ExtensibleNode,
    'ForeignKeyCacheInfo': ForeignKeyCacheInfo,    'Flow': Flow,    'PlanSlice': PlanSlice,
    'DirectDispatchInfo': DirectDispatchInfo,    'CdbPathLocus': CdbPathLocus, 'DistributionKey': DistributionKey,
}

# TODO: deal with sort option for numCols in 
#       Motion, Sort 
plans = {
    'Result': Result,
    'ProjectSet': ProjectSet,
    'ModifyTable': ModifyTable,
    'Append': Append,
    'MergeAppend': MergeAppend,
    'RecursiveUnion': RecursiveUnion,
    'BitmapAnd': BitmapAnd,
    'BitmapOr': BitmapOr,
    'Scan': Scan,
    'Material': Material,
    'Memoize': Memoize,
    'Sort': Sort,
    'Group': Group,
    'Agg': Agg,
    'WindowAgg': WindowAgg,
    'Unique': Unique,
    'Gather': Gather,
    'GatherMerge': GatherMerge,
    'Hash': Hash,
    'SetOp': SetOp,
    'LockRows': LockRows,
    'Limit': Limit,
    'Motion': Motion,
}

joins = {
    'NestLoop': NestLoop,
    'MergeJoin': MergeJoin,
    'HashJoin': HashJoin,
}

paths = {
    'IndexPath': IndexPath,
    'BitmapHeapPath': BitmapHeapPath,
    'BitmapAndPath': BitmapAndPath,
    'BitmapOrPath': BitmapOrPath,
    'TidPath': TidPath,
    'SubqueryScanPath': SubqueryScanPath,
    'ForeignPath': ForeignPath,
    'CustomPath': CustomPath,
    'AppendPath': AppendPath,
    'MergeAppendPath': MergeAppendPath,
    'GroupResultPath': GroupResultPath,
    'MaterialPath': MaterialPath,
    'UniquePath': UniquePath,
    'GatherPath': GatherPath,
    'GatherMergePath': GatherMergePath,
    'ProjectionPath': ProjectionPath,
    'ProjectSetPath': ProjectSetPath,
    'SortPath': SortPath,
    'GroupPath': GroupPath,
    'UpperUniquePath': UpperUniquePath,
    'AggPath': AggPath,
    'GroupingSetsPath': GroupingSetsPath,
    'MinMaxAggPath': MinMaxAggPath,
    'WindowAggPath': WindowAggPath,
    'SetOpPath': SetOpPath,
    'RecursiveUnionPath': RecursiveUnionPath,
    'LockRowsPath': LockRowsPath,
    'ModifyTablePath': ModifyTablePath,
    'LimitPath': LimitPath,
    'CdbMotionPath': CdbMotionPath,
    'AppendOnlyPath': AppendOnlyPath,
    'AOCSPath': AOCSPath,
    'PartitionSelectorPath': PartitionSelectorPath,
    'CtePath': CtePath,
    'TableFunctionScanPath': TableFunctionScanPath,
    'TupleSplitPath': TupleSplitPath,
    'SplitUpdatePath': SplitUpdatePath,
}

basic = ['Plan', 'Expr', 'Path', 'Node', 'Join']

jpath = {
    'MergePath': MergePath,
    'HashPath': HashPath,
}

def split_field(name, s):
    pod_item = []
    pointer_item = []

    for key, val in s:
        if key == 'Join' or key == 'Plan' or key == 'Path' or key == 'JoinPath':
            pass
        elif key == 'DirectDispatchInfo':
            pointer_item.append([key, val])
        elif re.search('\*', key) and key != 'char*':
            pointer_item.append([key, val])
        else:
            pod_item.append([key, val])

    return [pod_item, pointer_item]

def gen_printer_class(name, fields, is_plan = False, is_join = False, is_path = False, is_jpath = False):
    class Printer(BasePrinter):
        def to_string(self):
            if is_plan:
                return self.plan_to_string(name, self.val['plan']) + self.print_to_string(' ', fields[0])
            elif is_join:
                return self.join_to_string(name) + self.print_to_string(' ', fields[0])
            elif is_path:
                return self.path_to_string(name, self.val['path']) + self.print_to_string(' ', fields[0])
            elif is_jpath:
                return self.jpath_to_string(name) + self.print_to_string(' ', fields[0])
            else:
                return self.print_to_string('%s ' % name, fields[0])

        def children(self):
            if is_plan:
                return self.print_children(fields[1]) + self.plan_children(self.val['plan'])
            elif is_join:
                return self.print_children(fields[1]) + self.join_children()
            elif is_path:
                return self.print_children(fields[1]) + self.path_children(self.val['path'])
            elif is_jpath:
                return self.print_children(fields[1]) + self.jpath_children()
            else:
                return self.print_children(fields[1])

    Printer.__name__ = name
    return Printer

def get_node_type(node):
    type = str(node['type'])[2:]
    if type == 'String' or type == 'Integer' or type == 'Float' or type == 'BitString':
        return 'Value'
    return type

def gen_base_printer_class(name):
    class Printer(BasePrinter):
        def to_string(self):
            self.type = get_node_type(self.val)
            if self.type == 'A_Star':
                return '*'
            elif self.type == 'Path':
                return self.path_to_string(self.type, self.val)
            elif self.type == 'NestPath':
                return self.jpath_to_string(self.type)
            return cast(self.val.address, self.type).dereference()

        def children(self):
            if self.type == 'Path':
                return self.path_children(self.val)
            elif self.type == 'NestPath':
                return self.jpath_children()

            return []
        
    Printer.__name__ = name
    return Printer

def generate_printer():
    for name, s in pl.items():
        pointerx = gen_printer_class(name, split_field(name, s))
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name, s in plans.items():
        pointerx = gen_printer_class(name, split_field(name, s), True)
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name, s in joins.items():
        pointerx = gen_printer_class(name, split_field(name, s), False, True)
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name, s in paths.items():
        pointerx = gen_printer_class(name, split_field(name, s), False, False, True)
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name, s in jpath.items():
        pointerx = gen_printer_class(name, split_field(name, s), False, False, False, True)
        printer.add_printer(name, '^' + name + '$', pointerx)
    for name in basic:
        pointerx = gen_base_printer_class(name)
        printer.add_printer(name, '^' + name + '$', pointerx)

generate_printer()


class ListIt(object):
    def __init__(self, list) -> None:
        self.head = list['head']
        self.size = list['length']
        self.count = 0

    def __iter__(self):
        return self

    def __len__(self):
        return int(self.size)

    def __next__(self):
        if self.count == self.size:
            raise StopIteration

        head = self.head
        self.head = self.head['next']
        self.count += 1

        return head

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
                node = cast(node['data']['ptr_value'], 'Node').dereference()
            elif str(self.type) == 'IntList':
                node = int(node['data']['int_value'])
            else:
                node = int(node['data']['oid_value'])

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

@register_printer('Value')
class ValuePrinter(BasePrinter):
    def to_string(self):
        vt = str(self.val['type'])[2:]
        ret = ''
        if vt == 'Integer':
            ret += str(self.val['val']['ival'])
        elif vt == 'Float' or vt == 'BitString' or vt == 'String':
            ret += getchars(self.val['val']['str'])
        return '{}[ {} ]'.format(vt, ret)


# @register_printer('Const')
# class ConstPrinter(BasePrinter):
#     def to_string(self):
#         if bool(self.val['constisnull']) == True:
#             return 'Null'
#         else:
#             pfunc = getTypeOutputInfo(int(self.val['consttype']))
#             return str(gdb.parse_and_eval('OidOutputFunctionCall({}, {})'.format(pfunc[0], int(self.val['constvalue']))).dereference())

def gen_base_any_node_printer_class():
    class Printer(BasePrinter):
        def to_string(self):
            return getchars(gdb.parse_and_eval('pretty_format_node_dump(nodeToString({}))'.format(self.val.reference_value().address)), False, 100000000)
            
    Printer.__name__ = 'AnyNode'
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
