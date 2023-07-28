import gdb
import string

printer = gdb.printing.RegexpCollectionPrettyPrinter("PostgreSQL 17devel")

class printerRtes(gdb.Parameter):
    def __init__(self) -> None:
        super(printerRtes, self).__init__('pg_retes', gdb.COMMAND_DATA, gdb.PARAM_STRING)
        self.value = 'None'
        self.rtes = None

    def get_set_string(self) -> str:
        if self.value == 'None':
            return ''
        self.rtes = gdb.parse_and_eval(self.value)
        node = cast(self.rtes, 'List').dereference()
        print(node)
        return ''
    
    def get_show_string(self, svalue: str) -> str:
        if self.rtes != None:
            node = cast(self.rtes, 'List').dereference()
            print(node)
        return ''

    def get_rte(self, index: int) -> gdb.Value:
        node = cast(self.rtes, 'List')
        return node['elements'][index - 1]

rtes = printerRtes()

class PgType:
    def __init__(self) -> None:
        self.types = {}
        with open('/home/asky/pg-pretty-printers/pg_type.txt') as file:
            for line in file:
                kv = line.strip().split()
                if len(kv) != 0:
                    self.types[int(kv[0])] = kv[2]

    def get_type(self, key: int) -> str:
        if key in self.types:
            return self.types[key]
        else:
            return 'unkowne_type'

class PgOperator:
    def __init__(self) -> None:
        self.oper = {}
        with open('/home/asky/pg-pretty-printers/pg_operator.txt') as file:
            for line in file:
                kv = line.strip().split()
                if len(kv) != 0:
                    self.oper[int(kv[0])] = kv[2]

    def get_oper(self, key: int) -> str:
        if key in self.oper:
            return self.oper[key]
        else:
            return 'unkowne_oper'

pg_type = PgType()
pg_oper = PgOperator()

def register_printer(name):
    def __registe(_printer):
        printer.add_printer(name, '^' + name + '$', _printer)
    return __registe

def is_a(n, t):
    if not is_node(n):
        return False

    return (str(n['type']) == ('T_' + t))

def get_node_type(node):
    type = str(node['type'])[2:]
    return type

def is_node(l):
    try:
        x = l['type']
        return True
    except:
        return False

# max print 100
def getchars(arg, qoute = True, len = 100):
    if (str(arg) == '0x0'):
        return str(arg)

    retval = ''
    if qoute:
        retval += '\''

    i=0
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

def cast(node, type_name):
    t = gdb.lookup_type(type_name)
    return node.cast(t.pointer())

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
        
        result = self.elements[self.count]
        self.count += 1

        return result

def add_list(list, val, filde):
    if str(val[filde]) != '0x0':
        list.append((filde, val[filde].dereference()))

def plan_to_string(type, plan):
    '''
    print plan
    '''
    return '%s (cost=%.2f..%.2f rows=%.0f width=%.0f plan_node_id=%s)' %(
        type,
        float(plan['startup_cost']),
        float(plan['total_cost']),
        float(plan['plan_rows']),
        float(plan['plan_width']),
        plan['plan_node_id']
    )

def plan_children(plan):
    list = []
    if gdb.parameter('pg_verbose'):
        add_list(list, plan, 'targetlist')
    add_list(list, plan, 'qual')
    add_list(list, plan, 'initPlan')
    add_list(list, plan, 'lefttree')
    add_list(list, plan, 'righttree')
    return list

def path_to_string(type, path):
    '''
    print path
    '''
    return '%s %s (cost=%.2f..%.2f rows=%.0f)' %(
        type,
        path['pathtype'],
        float(path['startup_cost']),
        float(path['total_cost']),
        float(path['rows'])
    )

def path_children(path):
    list = []
    add_list(list, path, 'pathtarget')
    add_list(list, path, 'param_info')
    add_list(list, path, 'pathkeys')
    # add_list(list, path, 'reduce_info_list')
    return list

@register_printer('Query')
class QueryPrinter:
    'print Query'
    def __init__(self, val) -> None:
        self.val = val

    def add_list(self, filde):
        if str(self.val[filde]) != '0x0':
            return (filde, self.val[filde].dereference())

    def to_string(self):
        return str(self.val['commandType'])

    def children(self):
        list = []
        add_list(list, self.val, 'cteList')
        add_list(list, self.val, 'utilityStmt')
        add_list(list, self.val, 'rtable')
        add_list(list, self.val, 'jointree')
        add_list(list, self.val, 'targetList')
        add_list(list, self.val, 'onConflict')
        add_list(list, self.val, 'returningList')
        add_list(list, self.val, 'groupClause')
        add_list(list, self.val, 'groupingSets')
        add_list(list, self.val, 'havingQual')
        add_list(list, self.val, 'windowClause')
        add_list(list, self.val, 'distinctClause')
        add_list(list, self.val, 'sortClause')
        add_list(list, self.val, 'limitOffset')
        add_list(list, self.val, 'rowMarks')
        add_list(list, self.val, 'setOperations')
        add_list(list, self.val, 'constraintDeps')
        add_list(list, self.val, 'withCheckOptions')
        return list
    
@register_printer('List')
class ListPrinter:
    'print List'
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
                # if is_node(node['ptr_value']):
                try:
                    node = cast(node['ptr_value'], 'Node').dereference()
                except:
                    # TODO
                    node = cast(node['ptr_value'], 'ReduceInfo').dereference()
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

@register_printer('Node')
class NodePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        type = get_node_type(self.val)
        return self.val.address.cast(gdb.lookup_type(type).pointer()).dereference()

@register_printer('Expr')
class ExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        type = get_node_type(self.val)
        return self.val.address.cast(gdb.lookup_type(type).pointer()).dereference()

@register_printer('Path')
class PathPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        type = get_node_type(self.val)
        return self.val.address.cast(gdb.lookup_type(type).pointer()).dereference()

@register_printer('FuncExpr')
class FuncExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'FuncExpr[funcid: %s, funcresulttype: %s, funcretset: %s, funcvariadic: %s, funcformat: %s, funccollid: %s, inputcollid: %s]' % (
            self.val['funcid'],
            self.val['funcresulttype'],
            self.val['funcretset'],
            self.val['funcvariadic'],
            self.val['funcformat'],
            self.val['funccollid'],
            self.val['inputcollid']
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'args')
        return list

@register_printer('AlternativeSubPlan')
class AlternativeSubPlanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'AlternativeSubPlan'
    
    def children(self):
        list = []
        add_list(list, self.val, 'subplans')
        return list

@register_printer('SubLink')
class SubLinkPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'SubLink[subLinkType: %s, subLinkId: %s]' % (
            self.val['subLinkType'],
            self.val['subLinkId'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'testexpr')
        add_list(list, self.val, 'operName')
        add_list(list, self.val, 'subselect')
        return list

@register_printer('FieldSelect')
class SubLinkPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'FieldSelect[fieldnum: %s, resulttype: %s, resulttypmod: %s, resultcollid: %s]' % (
            self.val['fieldnum'],
            self.val['resulttype'],
            self.val['resulttypmod'],
            self.val['resultcollid'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'arg')
        return list

@register_printer('FieldStore')
class SubLinkPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'FieldStore[resulttype: %s]' % (
            self.val['resulttype'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'arg')
        add_list(list, self.val, 'newvals')
        add_list(list, self.val, 'fieldnums')
        return list

@register_printer('ReduceInfo')
class ReduceInfoPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'ReduceInfo[type: %s, nkey: %s]' % (
            self.val['type'],
            self.val['nkey'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'storage_nodes')
        add_list(list, self.val, 'exclude_exec')
        add_list(list, self.val, 'values')
        add_list(list, self.val, 'relids')
        nkey = int(self.val['nkey'])
        while nkey > 0:
            nkey -= 1
            list.append(('keys' + str(nkey), self.val['keys'][nkey].dereference()))
        return list

@register_printer('SubscriptingRef')
class SubscriptingRefPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'SubscriptingRef[refcontainertype: %s, refelemtype: %s, reftypmod: %s, refcollid: %s]' % (
            self.val['refcontainertype'],
            self.val['refelemtype'],
            self.val['reftypmod'],
            self.val['refcollid'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'refupperindexpr')
        add_list(list, self.val, 'reflowerindexpr')
        add_list(list, self.val, 'refexpr')
        add_list(list, self.val, 'refassgnexpr')
        return list

@register_printer('CoalesceExpr')
class CoalesceExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'CoalesceExpr[coalescetype: %s, coalescecollid: %s]' % (
            self.val['coalescetype'],
            self.val['coalescecollid'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'args')
        return list

@register_printer('CaseExpr')
class CaseExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[casetype: %s, casecollid: %s]' % (self.val['casetype'], self.val['casecollid'])

    def children(self):
        list = []
        add_list(list, self.val, 'arg')
        add_list(list, self.val, 'args')
        add_list(list, self.val, 'defresult')
        return list

@register_printer('Param')
class ParamPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[paramkind: %s, paramid: %s, paramtype: %s, paramtypmod: %s, paramcollid: %s]' % (
            self.val['paramkind'],
            self.val['paramid'],
            self.val['paramtype'],
            self.val['paramtypmod'],
            self.val['paramcollid']
        )

@register_printer('PlannerParamItem')
class PlannerParamItemPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[paramId: %s]' % (
            self.val['paramId'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'item')
        return list

@register_printer('RestrictInfo')
class RestrictInfoPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'RestrictInfo [is_pushed_down: %s, outerjoin_delayed: %s, can_join: %s, pseudoconstant: %s, leakproof: %s, security_level: %s, clause_relids: %s, required_relids: %s, outer_relids: %s, nullable_relids: %s, left_relids: %s, right_relids: %s, eval_cost: %s]' % (
            self.val['is_pushed_down'],
            self.val['outerjoin_delayed'],
            self.val['can_join'],
            self.val['pseudoconstant'],
            self.val['leakproof'],
            self.val['security_level'],
            self.val['clause_relids'],
            self.val['required_relids'],
            self.val['outer_relids'],
            self.val['nullable_relids'],
            self.val['left_relids'],
            self.val['right_relids'],
            self.val['eval_cost'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'clause')
        add_list(list, self.val, 'orclause')
        add_list(list, self.val, 'parent_ec')
        add_list(list, self.val, 'mergeopfamilies')
        add_list(list, self.val, 'left_ec')
        add_list(list, self.val, 'right_ec')
        add_list(list, self.val, 'left_em')
        add_list(list, self.val, 'right_em')
        add_list(list, self.val, 'scansel_cache')
        return list


@register_printer('CaseWhen')
class CaseWhenPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'CaseWhen'

    def children(self):
        list = []
        add_list(list, self.val, 'expr')
        add_list(list, self.val, 'result')
        return list

@register_printer('TargetEntry')
class TargetEntryPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        if str(self.val['resname']) == '0x0':
            return '[resno: %s]' % self.val['resno']
        else:
            return self.val['resname']
    
    def children(self):
        return {
            ('expr', self.val['expr'].dereference()),
        }
    
    def display_hint(self):
        return 'array'

@register_printer('RangeTblEntry')
class RangeTblEntryPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        alias = self.val['eref'].dereference()
        retval = 'RangeTblEntry: [kind: %-17s' % (self.val['rtekind'])
        if str(alias['aliasname']) != '0x0': retval += ', alias: %-17s' % getchars(alias['aliasname'])
        retval += ', relid: %8s' % self.val['relid']
        retval += ', relkind: %s' % ((self.val['relkind']))
        retval += ']'
        return retval
    
    def children(self):
        if gdb.parameter('pg_verbose') == False:
            return []
        cols = self.val['eref'].dereference()['colnames']
        if str(cols) != '0x0':
            return {('cols', cols.dereference())}
        else:
            return {('cols', 'List with 0 elements')}

@register_printer('SortGroupClause')
class SortGroupClausePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'tleSortGroupRef: %s' % (self.val['tleSortGroupRef'])

@register_printer('FromExpr')
class FromExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'FromExpr'
    
    def children(self):
        list = []
        add_list(list, self.val, 'fromlist')
        add_list(list, self.val, 'quals')
        return list

@register_printer('JoinExpr')
class JoinExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[jointype: %s, isNatural: %s, rtindex: %s]' % (self.val['jointype'], self.val['isNatural'], self.val['rtindex'])
    
    def children(self):
        list = []
        add_list(list, self.val, 'larg')
        add_list(list, self.val, 'rarg')
        add_list(list, self.val, 'usingClause')
        add_list(list, self.val, 'quals')
        add_list(list, self.val, 'alias')
        return list

@register_printer('RangeTblRef')
class RangeTblRefPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return 'RangeTblRef: %s' % str(self.val['rtindex'])

@register_printer('Integer')
class IntegerPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return self.val['ival']

@register_printer('Float')
class FloatPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return self.val['fval']

@register_printer('Boolean')
class BooleanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return self.val['boolval']

@register_printer('String')
class StringPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return getchars(self.val['sval'], False)

@register_printer('BitString')
class BitStringPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return getchars(self.val['bsval'], False)

@register_printer('BoolExpr')
class BoolExprPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        if rtes.rtes != None:
            list = cast(self.val['args'], 'List')
            len = int(list['length'])
            op = str(self.val['boolop'])
            expr = '('
            if op == 'NOT_EXPR':
                op += 'NOT '
            expr += str(cast(list_nth(list, 0, 'ptr'), 'Node').dereference())
            i = 1
            while i < len:
                if op == 'AND_EXPR':
                    expr += ' AND '
                elif op == 'OR_EXPR':
                    expr += ' OR '
                expr += str(cast(list_nth(list, i, 'ptr'), 'Node').dereference())
                i += 1

            expr += ')'
            return expr
        else:
            return 'boolop: %s' % self.val['boolop']
    
    def children(self):
        list = []
        if rtes.rtes == None:
            add_list(list, self.val, 'args')
        return list
    
@register_printer('OpExpr')
class OpExprPrinter:
    def __init__(self, val) -> None:
        self.val = val
# Filter: (((receive_time)::text >= '2023-01-15 00:00:00'::text) AND ((receive_time)::text >= '2023-06-28 00:00:00'::text) AND ((receiver_id)::text = '530201'::text))
    def to_string(self):
        if rtes.rtes != None:
            list = cast(self.val['args'], 'List')
            if int(list['length']) == 2:
                return '(%s %s %s)' % (
                    cast(list_nth(list, 0, 'ptr'), 'Node').dereference(),
                    pg_oper.get_oper(int(self.val['opno'])),
                    cast(list_nth(list, 1, 'ptr'), 'Node').dereference()
                )
            else:
                return '(%s %s)' % (
                   pg_oper.get_oper(int(self.val['opno'])),
                   cast(list_nth(list, 0, 'ptr'), 'Node').dereference()
                )
        else:
            return '[opno: %s, opfuncid: %s, opresulttype: %s, opretset %s, opcollid %s, inputcollid %s]' % (
                self.val['opno'],
                self.val['opfuncid'],
                self.val['opresulttype'],
                self.val['opretset'],
                self.val['opcollid'],
                self.val['inputcollid']
            )
    
    def children(self):
        list = []
        if rtes.rtes == None:
            add_list(list, self.val, 'args')
        return list

def format_type_extended(type, mod):

    return 'None'

@register_printer('RelabelType')
class RelabelTypePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        if rtes.rtes != None:
            return '(%s)::%s' % (
                self.val['arg'].dereference(),
                pg_type.get_type(int(self.val['resulttype']))
            )
        else:
            return 'RelabelType[resulttype: %s, resulttypmod: %s, resultcollid: %s, relabelformat: %s]' % (
                self.val['resulttype'],
                self.val['resulttypmod'],
                self.val['resultcollid'],
                self.val['relabelformat']
            )
    
    def children(self):
        list = []
        if rtes.rtes == None:
            add_list(list, self.val, 'arg')
        return list

def is_none(node):
    return str(node) == '0x0'

def list_nth(list, index, type):
    return list['elements'][index][type + '_value']

def get_rte_attribute_name(rte, index):
    if index == 0:
        return '*'

    if str(rte['alias']) != '0x0' and str(rte['alias']['colnames']) != '0x0' and index > 0 and index < int(cast(rte['alias']['colnames'], 'List')['length']):
        return cast(list_nth(cast(rte['alias']['colnames'], 'List'), index - 1, 'ptr'), 'Node').dereference()

    if index > 0 and index < int(cast(rte['eref']['colnames'], 'List')['length']):
        return cast(list_nth(cast(rte['eref']['colnames'], 'List'), index - 1, 'ptr'), 'Node').dereference()
    return 'None'

@register_printer('Var')
class VarPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        if rtes.rtes != None:
            if int(self.val['varno']) == -1:
                return 'INNER.?'
            elif int(self.val['varno']) == -2:
                return 'OUTER.?'
            elif int(self.val['varno']) == -3:
                return 'INDEX.?'
            elif int(self.val['varno']) == -4:
                return 'ROWID_VAR'
            else:
                node = cast(rtes.get_rte(int(self.val['varno']))['ptr_value'], 'RangeTblEntry')
                return '%s.%s' % (
                    getchars(node['eref']['aliasname'], False),
                    get_rte_attribute_name(node, int(self.val['varattno'])),
                )
        else:
            return '[varno: %s, varattno: %s, vartype: %s, vartypmod: %s, varcollid: %s, varlevelsup: %s, varnosyn: %s, varattnosyn: %s]' % (
            self.val['varno'],
            self.val['varattno'],
            self.val['vartype'],
            self.val['vartypmod'],
            self.val['varcollid'],
            self.val['varlevelsup'],
            self.val['varnosyn'],
            self.val['varattnosyn']
        )
    
    def display_hint(self):
        return 'array'

# TODO add more
def get_const_val(type:int, val:int):
    if type == 16:
        return (True, 'true' if val != 0 else 'false')
    elif type == 20 or type == 21 or type == 23 or type == 26 or type == 28 or type == 29:
        return (True, int(val))
    elif type == 25:
        v = gdb.parse_and_eval('(char*)' + str(val))
        if v[0] == 0x01:
            return (False, 'cant print now')
        elif (v[0] & 0x01) == 0x01:
            len = v[0] >> 1 & 0x7F
            # TODO
            return (True, 'xxx')
        else:
            v = gdb.parse_and_eval('(int32*)' + str(val))
            len = ((v[0] >> 2 ) & 0x3FFFFFFF) - 4
            v = gdb.parse_and_eval('(char*)' + str(val + 4))
            return (True, getchars(v, True, len))

    return (False, '')

@register_printer('Const')
class ConstPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        if bool(self.val['constisnull']) == True:
            return 'Null'
        else:
            # TODO: print constant pretty
            auto = get_const_val(int(self.val['consttype']), int(self.val['constvalue']))
            if auto[0] == True:
                return auto[1]
            else:
                return '[consttype: %s, consttypmod: %s, constcollid: %s, constlen: %s, constvalue: %s, constisnull: %s, constbyval: %s]' % (
                    self.val['consttype'],
                    self.val['consttypmod'],
                    self.val['constcollid'],
                    self.val['constlen'],
                    self.val['constvalue'],
                    self.val['constisnull'],
                    self.val['constbyval']
                )
    
    def display_hint(self):
        return 'array'

@register_printer('SubPlan')
class SubPlanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[startup_cost: %.2f, per_call_cost: %.2f, subLinkType: %s, plan_id: %s, plan_name: %s, firstColType: %s, firstColTypmod: %s, firstColCollation: %s, useHashTable: %s, unknownEqFalse: %s, parallel_safe: %s]' % (
            float(self.val['startup_cost']),
            float(self.val['per_call_cost']),
            self.val['subLinkType'],
            self.val['plan_id'],
            self.val['plan_name'],
            self.val['firstColType'],
            self.val['firstColTypmod'],
            self.val['firstColCollation'],
            self.val['useHashTable'],
            self.val['unknownEqFalse'],
            self.val['parallel_safe'],
        )
    
    def children(self):
        list = []
        add_list(list, self.val, 'testexpr')
        add_list(list, self.val, 'paramIds')
        add_list(list, self.val, 'setParam')
        add_list(list, self.val, 'parParam')
        add_list(list, self.val, 'args')
        return list

@register_printer('Param')
class ParamPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[paramkind: %s, paramid: %s, paramtype: %s, paramtypmod: %s, paramcollid: %s]' % (
            self.val['paramkind'],
            self.val['paramid'],
            self.val['paramtype'],
            self.val['paramtypmod'],
            self.val['paramcollid']
        )

@register_printer('Aggref')
class AggrefPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[aggfnoid: %s, aggtype: %s, aggcollid: %s, inputcollid: %s, aggtranstype: %s, aggstar: %s, aggvariadic: %s, aggkind: %s, agglevelsup: %s, aggsplit: %s]' % (
            self.val['aggfnoid'],
            self.val['aggtype'],
            self.val['aggcollid'],
            self.val['inputcollid'],
            self.val['aggtranstype'],
            self.val['aggstar'],
            self.val['aggvariadic'],
            self.val['aggkind'],
            self.val['agglevelsup'],
            self.val['aggsplit']
        )
    def children(self):
        list = []
        add_list(list, self.val, 'aggargtypes')
        add_list(list, self.val, 'aggdirectargs')
        add_list(list, self.val, 'args')
        add_list(list, self.val, 'aggorder')
        add_list(list, self.val, 'aggdistinct')
        add_list(list, self.val, 'aggfilter')
        return list

@register_printer('PathTarget')
class PathTargetPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[cost: (%.2f..%.2f), width: %s]' % (
            float(self.val['cost']['startup']),
            float(self.val['cost']['per_tuple']),
            self.val['width'],
        )
    def children(self):
        list = []
        add_list(list, self.val, 'exprs')
        add_list(list, self.val, 'sortgrouprefs')
        return list

@register_printer('PlannedStmt')
class PlannedStmtPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[commandType: %s, queryId: %s, hasReturning: %s, hasModifyingCTE: %s, canSetTag: %s, transientPlan: %s, dependsOnRole: %s, parallelModeNeeded: %s, jitFlags: %s]' % (
            self.val['commandType'],
            self.val['queryId'],
            self.val['hasReturning'],
            self.val['hasModifyingCTE'],
            self.val['canSetTag'],
            self.val['transientPlan'],
            self.val['dependsOnRole'],
            self.val['parallelModeNeeded'],
            self.val['jitFlags']
        )

    def children(self):
        list = []
        add_list(list, self.val, 'rtable')
        add_list(list, self.val, 'planTree')
        add_list(list, self.val, 'permInfos')
        add_list(list, self.val, 'resultRelations')
        add_list(list, self.val, 'appendRelations')
        add_list(list, self.val, 'subplans')
        add_list(list, self.val, 'rewindPlanIDs')
        add_list(list, self.val, 'rowMarks')
        add_list(list, self.val, 'relationOids')
        add_list(list, self.val, 'invalItems')
        add_list(list, self.val, 'paramExecTypes')
        add_list(list, self.val, 'utilityStmt')
        return list


@register_printer('Plan')
class PlanPrinter:
    '''
    print plan
    '''
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        type = get_node_type(self.val)
        return self.val.address.cast(gdb.lookup_type(type).pointer()).dereference()

@register_printer('Result')
class ResultPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        return plan_to_string('Result', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'resconstantqual')
        return list

@register_printer('ProjectSet')
class ProjectSetPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        return plan_to_string('ProjectSet', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        return list

@register_printer('ModifyTable')
class ModifyTablePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <operation: %s, canSetTag: %s, nominalRelation: %s, rootRelation: %s, partColsUpdated: %s, resultRelIndex: %s, rootResultRelIndex: %s, epqParam: %s, onConflictAction: %s, exclRelRTI: %s>' % (
            str(self.val['operation']),
            str(self.val['canSetTag']),
            str(self.val['nominalRelation']),
            str(self.val['rootRelation']),
            str(self.val['partColsUpdated']),
            str(self.val['resultRelIndex']),
            str(self.val['rootResultRelIndex']),
            str(self.val['epqParam']),
            str(self.val['onConflictAction']),
            str(self.val['exclRelRTI']),
        )
        return plan_to_string('ModifyTable', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'resultRelations')
        add_list(list, self.val, 'plans')
        add_list(list, self.val, 'withCheckOptionLists')
        add_list(list, self.val, 'returningLists')
        add_list(list, self.val, 'fdwPrivLists')
        add_list(list, self.val, 'fdwDirectModifyPlans')
        add_list(list, self.val, 'rowMarks')
        add_list(list, self.val, 'arbiterIndexes')
        add_list(list, self.val, 'onConflictSet')
        add_list(list, self.val, 'onConflictWhere')
        add_list(list, self.val, 'exclRelTlist')
        add_list(list, self.val, 'remote_plans')
        add_list(list, self.val, 'resultAttnos')
        add_list(list, self.val, 'param_new')
        add_list(list, self.val, 'param_old')
        return list

@register_printer('Append')
class AppendPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <first_partial_plan: %s>' % str(self.val['first_partial_plan'])
        return plan_to_string('Append', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'apprelids')
        add_list(list, self.val, 'appendplans')
        add_list(list, self.val, 'part_prune_info')
        return list

@register_printer('MergeAppend')
class MergeAppendPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <numCols: %s>' % str(self.val['numCols'])
        return plan_to_string('MergeAppend', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'apprelids')
        add_list(list, self.val, 'mergeplans')
        add_list(list, self.val, 'sortColIdx')
        add_list(list, self.val, 'sortOperators')
        add_list(list, self.val, 'collations')
        add_list(list, self.val, 'nullsFirst')
        add_list(list, self.val, 'part_prune_info')
        return list

@register_printer('RecursiveUnion')
class RecursiveUnionPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <wtParam: %s, numCols: %s, numGroups: %s>' % (
            str(self.val['wtParam']),
            str(self.val['numCols']),
            str(self.val['numGroups'])
        )
        return plan_to_string('RecursiveUnion', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'dupColIdx')
        add_list(list, self.val, 'dupOperators')
        add_list(list, self.val, 'dupCollations')
        return list

@register_printer('BitmapAnd')
class BitmapAndPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        return plan_to_string('BitmapAnd', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'bitmapplans')
        return list

@register_printer('BitmapOr')
class BitmapAndPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <isshared: %s>' % str(self.val['isshared'])
        return plan_to_string('BitmapOr', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'bitmapplans')
        return list

# TODO: scan plan family
@register_printer('SeqScan')
class SeqScanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        #  TODO select from database?
        if rtes.rtes != None:
            node = cast(rtes.get_rte(int(self.val['scan']['scanrelid']))['ptr_value'], 'RangeTblEntry')
            ext += ' on %s' % getchars(node['eref']['aliasname'], False)
        else:
            ext = ' <scanrelid: %s>' % str(self.val['scan']['scanrelid'])

        return plan_to_string('SeqScan', self.val['scan']['plan']) + ext

    def children(self):
        if rtes.rtes != None:
            return plan_children(self.val['scan']['plan'])
        else:
            return []

@register_printer('SubqueryScan')
class SubqueryScanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <scanrelid: %s, scanstatus: %s>' % (
            str(self.val['scan']['scanrelid']),
            self.val['scanstatus'],
        )
        return plan_to_string('SubqueryScan', self.val['scan']['plan']) + ext

    def children(self):
        list = []
        add_list(list, self.val, 'subplan')
        return list

@register_printer('RemoteQuery')
class RemoteQueryPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        return '[exec_direct_type: %s, combine_type: %s, read_only: %s, force_autocommit: %s, exec_type: %s, rq_params_internal: %s]' % (
            self.val['exec_direct_type'],
            self.val['combine_type'],
            self.val['read_only'],
            self.val['force_autocommit'],
            self.val['exec_type'],
            self.val['rq_params_internal'],
        )

    def children(self):
        list = []
        list.append(('scan', self.val['scan']))
        add_list(list, self.val, 'exec_nodes')
        add_list(list, self.val, 'reduce_expr')
        add_list(list, self.val, 'remote_query')
        add_list(list, self.val, 'base_tlist')
        add_list(list, self.val, 'coord_var_tlist')
        add_list(list, self.val, 'query_var_tlist')
        return list

# TODO: join plan family
@register_printer('Join')
class JoinPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <jointype: %s, inner_unique: %s>' % (str(self.val['jointype']), str(self.val['inner_unique']))
        return plan_to_string('Join', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'joinqual')
        return list

@register_printer('Material')
class MaterialPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        return plan_to_string('Material', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        return list

@register_printer('Sort')
class SortPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <numCols: %s>' % (
            str(self.val['numCols']),
        )
        return plan_to_string('Sort', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'sortColIdx')
        add_list(list, self.val, 'sortOperators')
        add_list(list, self.val, 'collations')
        add_list(list, self.val, 'nullsFirst')
        return list

@register_printer('Group')
class GroupPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <numCols: %s>' % (
            str(self.val['numCols']),
        )
        return plan_to_string('Group', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'grpColIdx')
        add_list(list, self.val, 'grpOperators')
        add_list(list, self.val, 'grpCollations')
        return list

@register_printer('Agg')
class AggPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <aggstrategy: %s, aggsplit: %s, numCols: %s, numGroups: %s, transitionSpace: %s>' % (
            str(self.val['aggstrategy']),
            str(self.val['aggsplit']),
            str(self.val['numCols']),
            str(self.val['numGroups']),
            str(self.val['transitionSpace']),
        )
        return plan_to_string('Agg', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'grpColIdx')
        add_list(list, self.val, 'grpOperators')
        add_list(list, self.val, 'grpCollations')
        add_list(list, self.val, 'aggParams')
        add_list(list, self.val, 'groupingSets')
        add_list(list, self.val, 'chain')
        return list

@register_printer('ClusterReduce')
class ClusterReducePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <special_node: %s, numCols: %s, reduce_flags: %s>' % (
            str(self.val['special_node']),
            str(self.val['numCols']),
            str(self.val['reduce_flags'])
        )
        return plan_to_string('ClusterReduce', self.val['plan']) + ext
    
    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'reduce')
        add_list(list, self.val, 'special_reduce')
        add_list(list, self.val, 'reduce_oids')
        add_list(list, self.val, 'sortColIdx')
        add_list(list, self.val, 'sortOperators')
        add_list(list, self.val, 'collations')
        return list


@register_printer('Unique')
class UniquePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <numCols: %s>' % (
            str(self.val['numCols'])
        )
        return plan_to_string('Unique', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'uniqColIdx')
        add_list(list, self.val, 'uniqOperators')
        add_list(list, self.val, 'uniqCollations')
        return list

@register_printer('Gather')
class GatherPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <num_workers: %s, rescan_param: %s, single_copy: %s>' % (
            str(self.val['num_workers']),
            str(self.val['rescan_param']),
            str(self.val['single_copy'])
        )
        return plan_to_string('Gather', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'initParam')
        return list

@register_printer('GatherMerge')
class GatherMergePrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <num_workers: %s, rescan_param: %s, numCols: %s>' % (
            str(self.val['num_workers']),
            str(self.val['rescan_param']),
            str(self.val['numCols'])
        )
        return plan_to_string('GatherMerge', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'sortColIdx')
        add_list(list, self.val, 'sortOperators')
        add_list(list, self.val, 'collations')
        add_list(list, self.val, 'nullsFirst')
        add_list(list, self.val, 'initParam')
        return list

@register_printer('Hash')
class HashPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <skewTable: %s, skewColumn: %s, skewInherit: %s, rows_total: %s>' % (
            str(self.val['skewTable']),
            str(self.val['skewColumn']),
            str(self.val['skewInherit']),
            str(self.val['rows_total'])
        )
        return plan_to_string('Hash', self.val['plan']) + ext

    def children(self):
        return plan_children(self.val['plan'])

@register_printer('SetOp')
class SetOpPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <cmd: %s, strategy: %s, numCols: %s, flagColIdx: %s, firstFlag: %s, numGroups: %s>' % (
            str(self.val['cmd']),
            str(self.val['strategy']),
            str(self.val['numCols']),
            str(self.val['flagColIdx']),
            str(self.val['firstFlag']),
            str(self.val['numGroups'])
        )
        return plan_to_string('SetOp', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'dupColIdx')
        add_list(list, self.val, 'dupOperators')
        add_list(list, self.val, 'dupCollations')
        return list

@register_printer('LockRows')
class LockRowsPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <epqParam: %s>' % (
            str(self.val['epqParam']),
        )
        return plan_to_string('LockRows', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'rowMarks')
        return list

@register_printer('Limit')
class LimitPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ' <limitOption: %s, uniqNumCols: %s>' % (
            str(self.val['limitOption']),
            str(self.val['uniqNumCols']),
        )
        return plan_to_string('Limit', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'limitOffset')
        add_list(list, self.val, 'limitCount')
        add_list(list, self.val, 'uniqColIdx')
        add_list(list, self.val, 'uniqOperators')
        add_list(list, self.val, 'uniqCollations')
        return list
    
@register_printer('ReduceScan')
class ReduceScanPrinter:
    def __init__(self, val) -> None:
        self.val = val

    def to_string(self):
        ext = ''
        return plan_to_string('ReduceScan', self.val['plan']) + ext

    def children(self):
        list = plan_children(self.val['plan'])
        add_list(list, self.val, 'param_hash_keys')
        add_list(list, self.val, 'scan_hash_keys')
        return list

gdb.printing.register_pretty_printer(
    gdb.current_objfile(),
    printer, True)

class printVerbose(gdb.Parameter):
    def __init__(self) -> None:
        super(printVerbose, self).__init__('pg_verbose', gdb.COMMAND_DATA, gdb.PARAM_BOOLEAN)
        self.value = False

    def get_set_string(self) -> str:
        return ''



printVerbose()

