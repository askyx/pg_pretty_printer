Alias = [
  ('char*', 'aliasname'),
  ('List*', 'colnames'),
]

RangeVar = [
  ('char*', 'catalogname'),
  ('char*', 'schemaname'),
  ('char*', 'relname'),
  ('bool', 'inh'),
  ('char', 'relpersistence'),
  ('Alias*', 'alias'),
  ('int', 'location'),
]

TableFunc = [
  ('List*', 'ns_uris'),
  ('List*', 'ns_names'),
  ('Node*', 'docexpr'),
  ('Node*', 'rowexpr'),
  ('List*', 'colnames'),
  ('List*', 'coltypes'),
  ('List*', 'coltypmods'),
  ('List*', 'colcollations'),
  ('List*', 'colexprs'),
  ('List*', 'coldefexprs'),
  ('Bitmapset*', 'notnulls'),
  ('int', 'ordinalitycol'),
  ('int', 'location'),
]

IntoClause = [
  ('RangeVar*', 'rel'),
  ('List*', 'colNames'),
  ('char*', 'accessMethod'),
  ('List*', 'options'),
  ('OnCommitAction', 'onCommit'),
  ('char*', 'tableSpaceName'),
  ('Node*', 'viewQuery'),
  ('bool', 'skipData'),
]

Var = [
  ('int', 'varno'),
  ('AttrNumber', 'varattno'),
  ('Oid', 'vartype'),
  ('int32', 'vartypmod'),
  ('Oid', 'varcollid'),
  ('Index', 'varlevelsup'),
  ('Index', 'varnoold'),
  ('AttrNumber', 'varoattno'),
  ('int', 'location'),
]

Const = [
  ('Oid', 'consttype'),
  ('int32', 'consttypmod'),
  ('Oid', 'constcollid'),
  ('int', 'constlen'),
  ('Datum', 'constvalue'),
  ('bool', 'constisnull'),
  ('bool', 'constbyval'),
  ('int', 'location'),
]

Param = [
  ('ParamKind', 'paramkind'),
  ('int', 'paramid'),
  ('Oid', 'paramtype'),
  ('int32', 'paramtypmod'),
  ('Oid', 'paramcollid'),
  ('int', 'location'),
]

Aggref = [
  ('Oid', 'aggfnoid'),
  ('Oid', 'aggtype'),
  ('Oid', 'aggcollid'),
  ('Oid', 'inputcollid'),
  ('Oid', 'aggtranstype'),
  ('List*', 'aggargtypes'),
  ('List*', 'aggdirectargs'),
  ('List*', 'args'),
  ('List*', 'aggorder'),
  ('List*', 'aggdistinct'),
  ('Expr*', 'aggfilter'),
  ('bool', 'aggstar'),
  ('bool', 'aggvariadic'),
  ('char', 'aggkind'),
  ('Index', 'agglevelsup'),
  ('AggSplit', 'aggsplit'),
  ('int', 'agg_expr_id'),
  ('int', 'location'),
]

GroupingFunc = [
  ('List*', 'args'),
  ('List*', 'refs'),
  ('List*', 'cols'),
  ('Index', 'agglevelsup'),
  ('int', 'location'),
]

WindowFunc = [
  ('Oid', 'winfnoid'),
  ('Oid', 'wintype'),
  ('Oid', 'wincollid'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('Expr*', 'aggfilter'),
  ('Index', 'winref'),
  ('bool', 'winstar'),
  ('bool', 'winagg'),
  ('int', 'location'),
]

SubscriptingRef = [
  ('Oid', 'refcontainertype'),
  ('Oid', 'refelemtype'),
  ('Oid', 'refrestype'),
  ('int32', 'reftypmod'),
  ('Oid', 'refcollid'),
  ('List*', 'refupperindexpr'),
  ('List*', 'reflowerindexpr'),
  ('Expr*', 'refexpr'),
  ('Expr*', 'refassgnexpr'),
]

FuncExpr = [
  ('Oid', 'funcid'),
  ('Oid', 'funcresulttype'),
  ('bool', 'funcretset'),
  ('bool', 'funcvariadic'),
  ('CoercionForm', 'funcformat'),
  ('Oid', 'funccollid'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

NamedArgExpr = [
  ('Expr*', 'arg'),
  ('char*', 'name'),
  ('int', 'argnumber'),
  ('int', 'location'),
]

OpExpr = [
  ('Oid', 'opno'),
  ('Oid', 'opfuncid'),
  ('Oid', 'opresulttype'),
  ('bool', 'opretset'),
  ('Oid', 'opcollid'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

DistinctExpr = [
  ('Oid', 'opno'),
  ('Oid', 'opfuncid'),
  ('Oid', 'opresulttype'),
  ('bool', 'opretset'),
  ('Oid', 'opcollid'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

NullIfExpr = [
  ('Oid', 'opno'),
  ('Oid', 'opfuncid'),
  ('Oid', 'opresulttype'),
  ('bool', 'opretset'),
  ('Oid', 'opcollid'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

ScalarArrayOpExpr = [
  ('Oid', 'opno'),
  ('Oid', 'opfuncid'),
  ('Oid', 'hashfuncid'),
  ('Oid', 'negfuncid'),
  ('bool', 'useOr'),
  ('Oid', 'inputcollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

BoolExpr = [
  ('BoolExprType', 'boolop'),
  ('List*', 'args'),
  ('int', 'location'),
]

SubLink = [
  ('SubLinkType', 'subLinkType'),
  ('int', 'subLinkId'),
  ('Node*', 'testexpr'),
  ('List*', 'operName'),
  ('Node*', 'subselect'),
  ('int', 'location'),
]

SubPlan = [
  ('SubLinkType', 'subLinkType'),
  ('Node*', 'testexpr'),
  ('List*', 'paramIds'),
  ('int', 'plan_id'),
  ('char*', 'plan_name'),
  ('Oid', 'firstColType'),
  ('int32', 'firstColTypmod'),
  ('Oid', 'firstColCollation'),
  ('bool', 'useHashTable'),
  ('bool', 'unknownEqFalse'),
  ('bool', 'parallel_safe'),
  ('List*', 'setParam'),
  ('List*', 'parParam'),
  ('List*', 'args'),
  ('Cost', 'startup_cost'),
  ('Cost', 'per_call_cost'),
]

AlternativeSubPlan = [
  ('List*', 'subplans'),
]

FieldSelect = [
  ('Expr*', 'arg'),
  ('AttrNumber', 'fieldnum'),
  ('Oid', 'resulttype'),
  ('int32', 'resulttypmod'),
  ('Oid', 'resultcollid'),
]

FieldStore = [
  ('Expr*', 'arg'),
  ('List*', 'newvals'),
  ('List*', 'fieldnums'),
  ('Oid', 'resulttype'),
]

RelabelType = [
  ('Expr*', 'arg'),
  ('Oid', 'resulttype'),
  ('int32', 'resulttypmod'),
  ('Oid', 'resultcollid'),
  ('CoercionForm', 'relabelformat'),
  ('int', 'location'),
]

CoerceViaIO = [
  ('Expr*', 'arg'),
  ('Oid', 'resulttype'),
  ('Oid', 'resultcollid'),
  ('CoercionForm', 'coerceformat'),
  ('int', 'location'),
]

ArrayCoerceExpr = [
  ('Expr*', 'arg'),
  ('Expr*', 'elemexpr'),
  ('Oid', 'resulttype'),
  ('int32', 'resulttypmod'),
  ('Oid', 'resultcollid'),
  ('CoercionForm', 'coerceformat'),
  ('int', 'location'),
]

ConvertRowtypeExpr = [
  ('Expr*', 'arg'),
  ('Oid', 'resulttype'),
  ('CoercionForm', 'convertformat'),
  ('int', 'location'),
]

CollateExpr = [
  ('Expr*', 'arg'),
  ('Oid', 'collOid'),
  ('int', 'location'),
]

CaseExpr = [
  ('Oid', 'casetype'),
  ('Oid', 'casecollid'),
  ('Expr*', 'arg'),
  ('List*', 'args'),
  ('Expr*', 'defresult'),
  ('int', 'location'),
]

CaseWhen = [
  ('Expr*', 'expr'),
  ('Expr*', 'result'),
  ('int', 'location'),
]

CaseTestExpr = [
  ('Oid', 'typeId'),
  ('int32', 'typeMod'),
  ('Oid', 'collation'),
]

ArrayExpr = [
  ('Oid', 'array_typeid'),
  ('Oid', 'array_collid'),
  ('Oid', 'element_typeid'),
  ('List*', 'elements'),
  ('bool', 'multidims'),
  ('int', 'location'),
]

RowExpr = [
  ('List*', 'args'),
  ('Oid', 'row_typeid'),
  ('CoercionForm', 'row_format'),
  ('List*', 'colnames'),
  ('int', 'location'),
]

RowCompareExpr = [
  ('RowCompareType', 'rctype'),
  ('List*', 'opnos'),
  ('List*', 'opfamilies'),
  ('List*', 'inputcollids'),
  ('List*', 'largs'),
  ('List*', 'rargs'),
]

CoalesceExpr = [
  ('Oid', 'coalescetype'),
  ('Oid', 'coalescecollid'),
  ('List*', 'args'),
  ('int', 'location'),
]

MinMaxExpr = [
  ('Oid', 'minmaxtype'),
  ('Oid', 'minmaxcollid'),
  ('Oid', 'inputcollid'),
  ('MinMaxOp', 'op'),
  ('List*', 'args'),
  ('int', 'location'),
]

SQLValueFunction = [
  ('SQLValueFunctionOp', 'op'),
  ('Oid', 'type'),
  ('int32', 'typmod'),
  ('int', 'location'),
]

XmlExpr = [
  ('XmlExprOp', 'op'),
  ('char*', 'name'),
  ('List*', 'named_args'),
  ('List*', 'arg_names'),
  ('List*', 'args'),
  ('XmlOptionType', 'xmloption'),
  ('bool', 'indent'),
  ('Oid', 'type'),
  ('int32', 'typmod'),
  ('int', 'location'),
]

JsonFormat = [
  ('JsonFormatType', 'format_type'),
  ('JsonEncoding', 'encoding'),
  ('int', 'location'),
]

JsonReturning = [
  ('JsonFormat*', 'format'),
  ('Oid', 'typid'),
  ('int32', 'typmod'),
]

JsonValueExpr = [
  ('Expr*', 'raw_expr'),
  ('Expr*', 'formatted_expr'),
  ('JsonFormat*', 'format'),
]

JsonConstructorExpr = [
  ('JsonConstructorType', 'type'),
  ('List*', 'args'),
  ('Expr*', 'func'),
  ('Expr*', 'coercion'),
  ('JsonReturning*', 'returning'),
  ('bool', 'absent_on_null'),
  ('bool', 'unique'),
  ('int', 'location'),
]

JsonIsPredicate = [
  ('Node*', 'expr'),
  ('JsonFormat*', 'format'),
  ('JsonValueType', 'item_type'),
  ('bool', 'unique_keys'),
  ('int', 'location'),
]

NullTest = [
  ('Expr*', 'arg'),
  ('NullTestType', 'nulltesttype'),
  ('bool', 'argisrow'),
  ('int', 'location'),
]

BooleanTest = [
  ('Expr*', 'arg'),
  ('BoolTestType', 'booltesttype'),
  ('int', 'location'),
]

CoerceToDomain = [
  ('Expr*', 'arg'),
  ('Oid', 'resulttype'),
  ('int32', 'resulttypmod'),
  ('Oid', 'resultcollid'),
  ('CoercionForm', 'coercionformat'),
  ('int', 'location'),
]

CoerceToDomainValue = [
  ('Oid', 'typeId'),
  ('int32', 'typeMod'),
  ('Oid', 'collation'),
  ('int', 'location'),
]

SetToDefault = [
  ('Oid', 'typeId'),
  ('int32', 'typeMod'),
  ('Oid', 'collation'),
  ('int', 'location'),
]

CurrentOfExpr = [
  ('Index', 'cvarno'),
  ('char*', 'cursor_name'),
  ('int', 'cursor_param'),
]

NextValueExpr = [
  ('Oid', 'seqid'),
  ('Oid', 'typeId'),
]

InferenceElem = [
  ('Node*', 'expr'),
  ('Oid', 'infercollid'),
  ('Oid', 'inferopclass'),
]

TargetEntry = [
  ('Expr*', 'expr'),
  ('AttrNumber', 'resno'),
  ('char*', 'resname'),
  ('Index', 'ressortgroupref'),
  ('Oid', 'resorigtbl'),
  ('AttrNumber', 'resorigcol'),
  ('bool', 'resjunk'),
]

RangeTblRef = [
  ('int', 'rtindex'),
]

JoinExpr = [
  ('JoinType', 'jointype'),
  ('bool', 'isNatural'),
  ('Node*', 'larg'),
  ('Node*', 'rarg'),
  ('List*', 'usingClause'),
  ('Node*', 'quals'),
  ('Alias*', 'alias'),
  ('int', 'rtindex'),
]

FromExpr = [
  ('List*', 'fromlist'),
  ('Node*', 'quals'),
]

OnConflictExpr = [
  ('OnConflictAction', 'action'),
  ('List*', 'arbiterElems'),
  ('Node*', 'arbiterWhere'),
  ('Oid', 'constraint'),
  ('List*', 'onConflictSet'),
  ('Node*', 'onConflictWhere'),
  ('int', 'exclRelIndex'),
  ('List*', 'exclRelTlist'),
]

Query = [
  ('CmdType', 'commandType'),
  ('QuerySource', 'querySource'),
  ('uint64', 'queryId'),
  ('bool', 'canSetTag'),
  ('Node*', 'utilityStmt'),
  ('int', 'resultRelation'),
  ('bool', 'hasAggs'),
  ('bool', 'hasWindowFuncs'),
  ('bool', 'hasTargetSRFs'),
  ('bool', 'hasDynamicFunctions'),
  ('bool', 'hasFuncsWithExecRestrictions'),
  ('bool', 'hasSubLinks'),
  ('bool', 'hasDistinctOn'),
  ('bool', 'hasRecursive'),
  ('bool', 'hasModifyingCTE'),
  ('bool', 'hasForUpdate'),
  ('bool', 'hasRowSecurity'),
  ('bool', 'canOptSelectLockingClause'),
  ('List*', 'cteList'),
  ('List*', 'rtable'),
  ('FromExpr*', 'jointree'),
  ('List*', 'targetList'),
  ('OverridingKind', 'override'),
  ('OnConflictExpr*', 'onConflict'),
  ('List*', 'returningList'),
  ('List*', 'groupClause'),
  ('List*', 'groupingSets'),
  ('Node*', 'havingQual'),
  ('List*', 'windowClause'),
  ('List*', 'distinctClause'),
  ('List*', 'sortClause'),
  ('List*', 'scatterClause'),
  ('bool', 'isTableValueSelect'),
  ('Node*', 'limitOffset'),
  ('Node*', 'limitCount'),
  ('List*', 'rowMarks'),
  ('Node*', 'setOperations'),
  ('List*', 'constraintDeps'),
  ('List*', 'withCheckOptions'),
  ('struct GpPolicy*', 'intoPolicy'),
  ('ParentStmtType', 'parentStmtType'),
  ('int', 'stmt_location'),
  ('int', 'stmt_len'),
  ('bool', 'expandMatViews'),
]

TypeName = [
  ('List*', 'names'),
  ('Oid', 'typeOid'),
  ('bool', 'setof'),
  ('bool', 'pct_type'),
  ('List*', 'typmods'),
  ('int32', 'typemod'),
  ('List*', 'arrayBounds'),
  ('int', 'location'),
]

ColumnRef = [
  ('List*', 'fields'),
  ('int', 'location'),
]

ParamRef = [
  ('int', 'number'),
  ('int', 'location'),
]

A_Expr = [
  ('A_Expr_Kind', 'kind'),
  ('List*', 'name'),
  ('Node*', 'lexpr'),
  ('Node*', 'rexpr'),
  ('int', 'location'),
]

A_Const = [
  ('union ValUnion', 'val'),
  ('bool', 'isnull'),
  ('int', 'location'),
]

TypeCast = [
  ('Node*', 'arg'),
  ('TypeName*', 'typeName'),
  ('int', 'location'),
]

CollateClause = [
  ('Node*', 'arg'),
  ('List*', 'collname'),
  ('int', 'location'),
]

RoleSpec = [
  ('RoleSpecType', 'roletype'),
  ('char*', 'rolename'),
  ('int', 'location'),
]

FuncCall = [
  ('List*', 'funcname'),
  ('List*', 'args'),
  ('List*', 'agg_order'),
  ('Node*', 'agg_filter'),
  ('struct WindowDef*', 'over'),
  ('bool', 'agg_within_group'),
  ('bool', 'agg_star'),
  ('bool', 'agg_distinct'),
  ('bool', 'func_variadic'),
  ('CoercionForm', 'funcformat'),
  ('int', 'location'),
]

A_Star = [
]

A_Indices = [
  ('bool', 'is_slice'),
  ('Node*', 'lidx'),
  ('Node*', 'uidx'),
]

A_Indirection = [
  ('Node*', 'arg'),
  ('List*', 'indirection'),
]

A_ArrayExpr = [
  ('List*', 'elements'),
  ('int', 'location'),
]

ResTarget = [
  ('char*', 'name'),
  ('List*', 'indirection'),
  ('Node*', 'val'),
  ('int', 'location'),
]

MultiAssignRef = [
  ('Node*', 'source'),
  ('int', 'colno'),
  ('int', 'ncolumns'),
]

SortBy = [
  ('Node*', 'node'),
  ('SortByDir', 'sortby_dir'),
  ('SortByNulls', 'sortby_nulls'),
  ('List*', 'useOp'),
  ('int', 'location'),
]

WindowDef = [
  ('char*', 'name'),
  ('char*', 'refname'),
  ('List*', 'partitionClause'),
  ('List*', 'orderClause'),
  ('int', 'frameOptions'),
  ('Node*', 'startOffset'),
  ('Node*', 'endOffset'),
  ('int', 'location'),
]

RangeSubselect = [
  ('bool', 'lateral'),
  ('Node*', 'subquery'),
  ('Alias*', 'alias'),
]

RangeFunction = [
  ('bool', 'lateral'),
  ('bool', 'ordinality'),
  ('bool', 'is_rowsfrom'),
  ('List*', 'functions'),
  ('Alias*', 'alias'),
  ('List*', 'coldeflist'),
]

RangeTableFunc = [
  ('bool', 'lateral'),
  ('Node*', 'docexpr'),
  ('Node*', 'rowexpr'),
  ('List*', 'namespaces'),
  ('List*', 'columns'),
  ('Alias*', 'alias'),
  ('int', 'location'),
]

RangeTableFuncCol = [
  ('char*', 'colname'),
  ('TypeName*', 'typeName'),
  ('bool', 'for_ordinality'),
  ('bool', 'is_not_null'),
  ('Node*', 'colexpr'),
  ('Node*', 'coldefexpr'),
  ('int', 'location'),
]

RangeTableSample = [
  ('Node*', 'relation'),
  ('List*', 'method'),
  ('List*', 'args'),
  ('Node*', 'repeatable'),
  ('int', 'location'),
]

ColumnDef = [
  ('char*', 'colname'),
  ('TypeName*', 'typeName'),
  ('char*', 'compression'),
  ('int', 'inhcount'),
  ('bool', 'is_local'),
  ('bool', 'is_not_null'),
  ('bool', 'is_from_type'),
  ('char', 'storage'),
  ('char*', 'storage_name'),
  ('Node*', 'raw_default'),
  ('Node*', 'cooked_default'),
  ('char', 'identity'),
  ('RangeVar*', 'identitySequence'),
  ('char', 'generated'),
  ('CollateClause*', 'collClause'),
  ('Oid', 'collOid'),
  ('List*', 'constraints'),
  ('List*', 'fdwoptions'),
  ('int', 'location'),
]

TableLikeClause = [
  ('RangeVar*', 'relation'),
  ('bits32', 'options'),
  ('Oid', 'relationOid'),
]

IndexElem = [
  ('char*', 'name'),
  ('Node*', 'expr'),
  ('char*', 'indexcolname'),
  ('List*', 'collation'),
  ('List*', 'opclass'),
  ('List*', 'opclassopts'),
  ('SortByDir', 'ordering'),
  ('SortByNulls', 'nulls_ordering'),
]

DefElem = [
  ('char*', 'defnamespace'),
  ('char*', 'defname'),
  ('Node*', 'arg'),
  ('DefElemAction', 'defaction'),
  ('int', 'location'),
]

LockingClause = [
  ('List*', 'lockedRels'),
  ('LockClauseStrength', 'strength'),
  ('LockWaitPolicy', 'waitPolicy'),
]

XmlSerialize = [
  ('XmlOptionType', 'xmloption'),
  ('Node*', 'expr'),
  ('TypeName*', 'typeName'),
  ('bool', 'indent'),
  ('int', 'location'),
]

PartitionElem = [
  ('char*', 'name'),
  ('Node*', 'expr'),
  ('List*', 'collation'),
  ('List*', 'opclass'),
  ('int', 'location'),
]

PartitionSpec = [
  ('PartitionStrategy', 'strategy'),
  ('List*', 'partParams'),
  ('int', 'location'),
]

PartitionBoundSpec = [
  ('char', 'strategy'),
  ('bool', 'is_default'),
  ('int', 'modulus'),
  ('int', 'remainder'),
  ('List*', 'listdatums'),
  ('List*', 'lowerdatums'),
  ('List*', 'upperdatums'),
  ('int', 'location'),
]

PartitionRangeDatum = [
  ('PartitionRangeDatumKind', 'kind'),
  ('Node*', 'value'),
  ('int', 'location'),
]

PartitionCmd = [
  ('RangeVar*', 'name'),
  ('PartitionBoundSpec*', 'bound'),
  ('bool', 'concurrent'),
]

RangeTblEntry = [
  ('RTEKind', 'rtekind'),
  ('Oid', 'relid'),
  ('char', 'relkind'),
  ('int', 'rellockmode'),
  ('struct TableSampleClause*', 'tablesample'),
  ('Query*', 'subquery'),
  ('bool', 'security_barrier'),
  ('struct PlannerInfo*', 'subquery_root'),
  ('List*', 'subquery_rtable'),
  ('List*', 'subquery_pathkeys'),
  ('JoinType', 'jointype'),
  ('List*', 'joinaliasvars'),
  ('List*', 'functions'),
  ('bool', 'funcordinality'),
  ('TableFunc*', 'tablefunc'),
  ('List*', 'values_lists'),
  ('char*', 'ctename'),
  ('Index', 'ctelevelsup'),
  ('bool', 'self_reference'),
  ('List*', 'coltypes'),
  ('List*', 'coltypmods'),
  ('List*', 'colcollations'),
  ('char*', 'enrname'),
  ('Cardinality', 'enrtuples'),
  ('bool', 'forceDistRandom'),
  ('Alias*', 'alias'),
  ('Alias*', 'eref'),
  ('bool', 'lateral'),
  ('bool', 'inh'),
  ('bool', 'inFromCl'),
  ('AclMode', 'requiredPerms'),
  ('Oid', 'checkAsUser'),
  ('Bitmapset*', 'selectedCols'),
  ('Bitmapset*', 'insertedCols'),
  ('Bitmapset*', 'updatedCols'),
  ('Bitmapset*', 'extraUpdatedCols'),
  ('List*', 'securityQuals'),
]

RTEPermissionInfo = [
  ('Oid', 'relid'),
  ('bool', 'inh'),
  ('AclMode', 'requiredPerms'),
  ('Oid', 'checkAsUser'),
  ('Bitmapset*', 'selectedCols'),
  ('Bitmapset*', 'insertedCols'),
  ('Bitmapset*', 'updatedCols'),
]

RangeTblFunction = [
  ('Node*', 'funcexpr'),
  ('int', 'funccolcount'),
  ('List*', 'funccolnames'),
  ('List*', 'funccoltypes'),
  ('List*', 'funccoltypmods'),
  ('List*', 'funccolcollations'),
  ('Bitmapset*', 'funcparams'),
]

TableSampleClause = [
  ('Oid', 'tsmhandler'),
  ('List*', 'args'),
  ('Expr*', 'repeatable'),
]

WithCheckOption = [
  ('WCOKind', 'kind'),
  ('char*', 'relname'),
  ('char*', 'polname'),
  ('Node*', 'qual'),
  ('bool', 'cascaded'),
]

SortGroupClause = [
  ('Index', 'tleSortGroupRef'),
  ('Oid', 'eqop'),
  ('Oid', 'sortop'),
  ('bool', 'nulls_first'),
  ('bool', 'hashable'),
]

GroupingSet = [
  ('GroupingSetKind', 'kind'),
  ('List*', 'content'),
  ('int', 'location'),
]

WindowClause = [
  ('char*', 'name'),
  ('char*', 'refname'),
  ('List*', 'partitionClause'),
  ('List*', 'orderClause'),
  ('int', 'frameOptions'),
  ('Node*', 'startOffset'),
  ('Node*', 'endOffset'),
  ('List*', 'runCondition'),
  ('Oid', 'startInRangeFunc'),
  ('Oid', 'endInRangeFunc'),
  ('Oid', 'inRangeColl'),
  ('bool', 'inRangeAsc'),
  ('bool', 'inRangeNullsFirst'),
  ('Index', 'winref'),
  ('bool', 'copiedOrder'),
]

RowMarkClause = [
  ('Index', 'rti'),
  ('LockClauseStrength', 'strength'),
  ('LockWaitPolicy', 'waitPolicy'),
  ('bool', 'pushedDown'),
]

WithClause = [
  ('List*', 'ctes'),
  ('bool', 'recursive'),
  ('int', 'location'),
]

InferClause = [
  ('List*', 'indexElems'),
  ('Node*', 'whereClause'),
  ('char*', 'conname'),
  ('int', 'location'),
]

OnConflictClause = [
  ('OnConflictAction', 'action'),
  ('InferClause*', 'infer'),
  ('List*', 'targetList'),
  ('Node*', 'whereClause'),
  ('int', 'location'),
]

CTESearchClause = [
  ('List*', 'search_col_list'),
  ('bool', 'search_breadth_first'),
  ('char*', 'search_seq_column'),
  ('int', 'location'),
]

CTECycleClause = [
  ('List*', 'cycle_col_list'),
  ('char*', 'cycle_mark_column'),
  ('Node*', 'cycle_mark_value'),
  ('Node*', 'cycle_mark_default'),
  ('char*', 'cycle_path_column'),
  ('int', 'location'),
  ('Oid', 'cycle_mark_type'),
  ('int', 'cycle_mark_typmod'),
  ('Oid', 'cycle_mark_collation'),
  ('Oid', 'cycle_mark_neop'),
]

CommonTableExpr = [
  ('char*', 'ctename'),
  ('List*', 'aliascolnames'),
  ('CTEMaterialize', 'ctematerialized'),
  ('Node*', 'ctequery'),
  ('CTESearchClause*', 'search_clause'),
  ('CTECycleClause*', 'cycle_clause'),
  ('int', 'location'),
  ('bool', 'cterecursive'),
  ('int', 'cterefcount'),
  ('List*', 'ctecolnames'),
  ('List*', 'ctecoltypes'),
  ('List*', 'ctecoltypmods'),
  ('List*', 'ctecolcollations'),
]

MergeWhenClause = [
  ('bool', 'matched'),
  ('CmdType', 'commandType'),
  ('OverridingKind', 'override'),
  ('Node*', 'condition'),
  ('List*', 'targetList'),
  ('List*', 'values'),
]

MergeAction = [
  ('bool', 'matched'),
  ('CmdType', 'commandType'),
  ('OverridingKind', 'override'),
  ('Node*', 'qual'),
  ('List*', 'targetList'),
  ('List*', 'updateColnos'),
]

TriggerTransition = [
  ('char*', 'name'),
  ('bool', 'isNew'),
  ('bool', 'isTable'),
]

JsonOutput = [
  ('TypeName*', 'typeName'),
  ('JsonReturning*', 'returning'),
]

JsonKeyValue = [
  ('Expr*', 'key'),
  ('JsonValueExpr*', 'value'),
]

JsonObjectConstructor = [
  ('List*', 'exprs'),
  ('JsonOutput*', 'output'),
  ('bool', 'absent_on_null'),
  ('bool', 'unique'),
  ('int', 'location'),
]

JsonArrayConstructor = [
  ('List*', 'exprs'),
  ('JsonOutput*', 'output'),
  ('bool', 'absent_on_null'),
  ('int', 'location'),
]

JsonArrayQueryConstructor = [
  ('Node*', 'query'),
  ('JsonOutput*', 'output'),
  ('JsonFormat*', 'format'),
  ('bool', 'absent_on_null'),
  ('int', 'location'),
]

JsonAggConstructor = [
  ('JsonOutput*', 'output'),
  ('Node*', 'agg_filter'),
  ('List*', 'agg_order'),
  ('struct WindowDef*', 'over'),
  ('int', 'location'),
]

JsonObjectAgg = [
  ('JsonAggConstructor*', 'constructor'),
  ('JsonKeyValue*', 'arg'),
  ('bool', 'absent_on_null'),
  ('bool', 'unique'),
]

JsonArrayAgg = [
  ('JsonAggConstructor*', 'constructor'),
  ('JsonValueExpr*', 'arg'),
  ('bool', 'absent_on_null'),
]

RawStmt = [
  ('Node*', 'stmt'),
  ('int', 'stmt_location'),
  ('int', 'stmt_len'),
]

InsertStmt = [
  ('RangeVar*', 'relation'),
  ('List*', 'cols'),
  ('Node*', 'selectStmt'),
  ('OnConflictClause*', 'onConflictClause'),
  ('List*', 'returningList'),
  ('WithClause*', 'withClause'),
  ('OverridingKind', 'override'),
]

DeleteStmt = [
  ('RangeVar*', 'relation'),
  ('List*', 'usingClause'),
  ('Node*', 'whereClause'),
  ('List*', 'returningList'),
  ('WithClause*', 'withClause'),
]

UpdateStmt = [
  ('RangeVar*', 'relation'),
  ('List*', 'targetList'),
  ('Node*', 'whereClause'),
  ('List*', 'fromClause'),
  ('List*', 'returningList'),
  ('WithClause*', 'withClause'),
]

MergeStmt = [
  ('RangeVar*', 'relation'),
  ('Node*', 'sourceRelation'),
  ('Node*', 'joinCondition'),
  ('List*', 'mergeWhenClauses'),
  ('WithClause*', 'withClause'),
]

SelectStmt = [
  ('List*', 'distinctClause'),
  ('IntoClause*', 'intoClause'),
  ('List*', 'targetList'),
  ('List*', 'fromClause'),
  ('Node*', 'whereClause'),
  ('List*', 'groupClause'),
  ('Node*', 'havingClause'),
  ('List*', 'windowClause'),
  ('List*', 'scatterClause'),
  ('List*', 'valuesLists'),
  ('List*', 'sortClause'),
  ('Node*', 'limitOffset'),
  ('Node*', 'limitCount'),
  ('List*', 'lockingClause'),
  ('WithClause*', 'withClause'),
  ('SetOperation', 'op'),
  ('bool', 'all'),
  ('bool', 'disableLockingOptimization'),
  ('struct SelectStmt*', 'larg'),
  ('struct SelectStmt*', 'rarg'),
]

SetOperationStmt = [
  ('SetOperation', 'op'),
  ('bool', 'all'),
  ('Node*', 'larg'),
  ('Node*', 'rarg'),
  ('List*', 'colTypes'),
  ('List*', 'colTypmods'),
  ('List*', 'colCollations'),
  ('List*', 'groupClauses'),
]

ReturnStmt = [
  ('Node*', 'returnval'),
]

PLAssignStmt = [
  ('char*', 'name'),
  ('List*', 'indirection'),
  ('int', 'nnames'),
  ('SelectStmt*', 'val'),
  ('int', 'location'),
]

CreateSchemaStmt = [
  ('char*', 'schemaname'),
  ('RoleSpec*', 'authrole'),
  ('List*', 'schemaElts'),
  ('bool', 'if_not_exists'),
]

AlterTableStmt = [
  ('RangeVar*', 'relation'),
  ('List*', 'cmds'),
  ('ObjectType', 'objtype'),
  ('bool', 'missing_ok'),
]

ReplicaIdentityStmt = [
  ('char', 'identity_type'),
  ('char*', 'name'),
]

AlterTableCmd = [
  ('AlterTableType', 'subtype'),
  ('char*', 'name'),
  ('int16', 'num'),
  ('RoleSpec*', 'newowner'),
  ('Node*', 'def'),
  ('DropBehavior', 'behavior'),
  ('bool', 'missing_ok'),
  ('bool', 'recurse'),
]

AlterCollationStmt = [
  ('List*', 'collname'),
]

AlterDomainStmt = [
  ('char', 'subtype'),
  ('List*', 'typeName'),
  ('char*', 'name'),
  ('Node*', 'def'),
  ('DropBehavior', 'behavior'),
  ('bool', 'missing_ok'),
]

GrantStmt = [
  ('bool', 'is_grant'),
  ('GrantTargetType', 'targtype'),
  ('ObjectType', 'objtype'),
  ('List*', 'objects'),
  ('List*', 'privileges'),
  ('List*', 'grantees'),
  ('bool', 'grant_option'),
  ('RoleSpec*', 'grantor'),
  ('DropBehavior', 'behavior'),
]

ObjectWithArgs = [
  ('List*', 'objname'),
  ('List*', 'objargs'),
  ('List*', 'objfuncargs'),
  ('bool', 'args_unspecified'),
]

AccessPriv = [
  ('char*', 'priv_name'),
  ('List*', 'cols'),
]

GrantRoleStmt = [
  ('List*', 'granted_roles'),
  ('List*', 'grantee_roles'),
  ('bool', 'is_grant'),
  ('List*', 'opt'),
  ('RoleSpec*', 'grantor'),
  ('DropBehavior', 'behavior'),
]

AlterDefaultPrivilegesStmt = [
  ('List*', 'options'),
  ('GrantStmt*', 'action'),
]

CopyStmt = [
  ('RangeVar*', 'relation'),
  ('Node*', 'query'),
  ('List*', 'attlist'),
  ('bool', 'is_from'),
  ('bool', 'is_program'),
  ('char*', 'filename'),
  ('List*', 'options'),
  ('Node*', 'whereClause'),
]

VariableSetStmt = [
  ('VariableSetKind', 'kind'),
  ('char*', 'name'),
  ('List*', 'args'),
  ('bool', 'is_local'),
]

VariableShowStmt = [
  ('char*', 'name'),
]

CreateStmt = [
  ('RangeVar*', 'relation'),
  ('List*', 'tableElts'),
  ('List*', 'inhRelations'),
  ('PartitionBoundSpec*', 'partbound'),
  ('PartitionSpec*', 'partspec'),
  ('TypeName*', 'ofTypename'),
  ('List*', 'constraints'),
  ('List*', 'options'),
  ('OnCommitAction', 'oncommit'),
  ('char*', 'tablespacename'),
  ('char*', 'accessMethod'),
  ('bool', 'if_not_exists'),
]

Constraint = [
  ('ConstrType', 'contype'),
  ('char*', 'conname'),
  ('bool', 'deferrable'),
  ('bool', 'initdeferred'),
  ('int', 'location'),
  ('bool', 'is_no_inherit'),
  ('Node*', 'raw_expr'),
  ('char*', 'cooked_expr'),
  ('char', 'generated_when'),
  ('bool', 'nulls_not_distinct'),
  ('List*', 'keys'),
  ('List*', 'including'),
  ('List*', 'exclusions'),
  ('List*', 'options'),
  ('char*', 'indexname'),
  ('char*', 'indexspace'),
  ('bool', 'reset_default_tblspc'),
  ('char*', 'access_method'),
  ('Node*', 'where_clause'),
  ('RangeVar*', 'pktable'),
  ('List*', 'fk_attrs'),
  ('List*', 'pk_attrs'),
  ('char', 'fk_matchtype'),
  ('char', 'fk_upd_action'),
  ('char', 'fk_del_action'),
  ('List*', 'fk_del_set_cols'),
  ('List*', 'old_conpfeqop'),
  ('Oid', 'old_pktable_oid'),
  ('bool', 'skip_validation'),
  ('bool', 'initially_valid'),
]

CreateTableSpaceStmt = [
  ('char*', 'tablespacename'),
  ('RoleSpec*', 'owner'),
  ('char*', 'location'),
  ('List*', 'options'),
]

DropTableSpaceStmt = [
  ('char*', 'tablespacename'),
  ('bool', 'missing_ok'),
]

AlterTableSpaceOptionsStmt = [
  ('char*', 'tablespacename'),
  ('List*', 'options'),
  ('bool', 'isReset'),
]

AlterTableMoveAllStmt = [
  ('char*', 'orig_tablespacename'),
  ('ObjectType', 'objtype'),
  ('List*', 'roles'),
  ('char*', 'new_tablespacename'),
  ('bool', 'nowait'),
]

CreateExtensionStmt = [
  ('char*', 'extname'),
  ('bool', 'if_not_exists'),
  ('List*', 'options'),
]

AlterExtensionStmt = [
  ('char*', 'extname'),
  ('List*', 'options'),
]

AlterExtensionContentsStmt = [
  ('char*', 'extname'),
  ('int', 'action'),
  ('ObjectType', 'objtype'),
  ('Node*', 'object'),
]

CreateFdwStmt = [
  ('char*', 'fdwname'),
  ('List*', 'func_options'),
  ('List*', 'options'),
]

AlterFdwStmt = [
  ('char*', 'fdwname'),
  ('List*', 'func_options'),
  ('List*', 'options'),
]

CreateForeignServerStmt = [
  ('char*', 'servername'),
  ('char*', 'servertype'),
  ('char*', 'version'),
  ('char*', 'fdwname'),
  ('bool', 'if_not_exists'),
  ('List*', 'options'),
]

AlterForeignServerStmt = [
  ('char*', 'servername'),
  ('char*', 'version'),
  ('List*', 'options'),
  ('bool', 'has_version'),
]

CreateForeignTableStmt = [
  ('CreateStmt', 'base'),
  ('char*', 'servername'),
  ('List*', 'options'),
]

CreateUserMappingStmt = [
  ('RoleSpec*', 'user'),
  ('char*', 'servername'),
  ('bool', 'if_not_exists'),
  ('List*', 'options'),
]

AlterUserMappingStmt = [
  ('RoleSpec*', 'user'),
  ('char*', 'servername'),
  ('List*', 'options'),
]

DropUserMappingStmt = [
  ('RoleSpec*', 'user'),
  ('char*', 'servername'),
  ('bool', 'missing_ok'),
]

ImportForeignSchemaStmt = [
  ('char*', 'server_name'),
  ('char*', 'remote_schema'),
  ('char*', 'local_schema'),
  ('ImportForeignSchemaType', 'list_type'),
  ('List*', 'table_list'),
  ('List*', 'options'),
]

CreatePolicyStmt = [
  ('char*', 'policy_name'),
  ('RangeVar*', 'table'),
  ('char*', 'cmd_name'),
  ('bool', 'permissive'),
  ('List*', 'roles'),
  ('Node*', 'qual'),
  ('Node*', 'with_check'),
]

AlterPolicyStmt = [
  ('char*', 'policy_name'),
  ('RangeVar*', 'table'),
  ('List*', 'roles'),
  ('Node*', 'qual'),
  ('Node*', 'with_check'),
]

CreateAmStmt = [
  ('char*', 'amname'),
  ('List*', 'handler_name'),
  ('char', 'amtype'),
]

CreateTrigStmt = [
  ('bool', 'replace'),
  ('bool', 'isconstraint'),
  ('char*', 'trigname'),
  ('RangeVar*', 'relation'),
  ('List*', 'funcname'),
  ('List*', 'args'),
  ('bool', 'row'),
  ('int16', 'timing'),
  ('int16', 'events'),
  ('List*', 'columns'),
  ('Node*', 'whenClause'),
  ('List*', 'transitionRels'),
  ('bool', 'deferrable'),
  ('bool', 'initdeferred'),
  ('RangeVar*', 'constrrel'),
]

CreateEventTrigStmt = [
  ('char*', 'trigname'),
  ('char*', 'eventname'),
  ('List*', 'whenclause'),
  ('List*', 'funcname'),
]

AlterEventTrigStmt = [
  ('char*', 'trigname'),
  ('char', 'tgenabled'),
]

CreatePLangStmt = [
  ('bool', 'replace'),
  ('char*', 'plname'),
  ('List*', 'plhandler'),
  ('List*', 'plinline'),
  ('List*', 'plvalidator'),
  ('bool', 'pltrusted'),
]

CreateRoleStmt = [
  ('RoleStmtType', 'stmt_type'),
  ('char*', 'role'),
  ('List*', 'options'),
]

AlterRoleStmt = [
  ('RoleSpec*', 'role'),
  ('List*', 'options'),
  ('int', 'action'),
]

AlterRoleSetStmt = [
  ('RoleSpec*', 'role'),
  ('char*', 'database'),
  ('VariableSetStmt*', 'setstmt'),
]

DropRoleStmt = [
  ('List*', 'roles'),
  ('bool', 'missing_ok'),
]

CreateSeqStmt = [
  ('RangeVar*', 'sequence'),
  ('List*', 'options'),
  ('Oid', 'ownerId'),
  ('bool', 'for_identity'),
  ('bool', 'if_not_exists'),
]

AlterSeqStmt = [
  ('RangeVar*', 'sequence'),
  ('List*', 'options'),
  ('bool', 'for_identity'),
  ('bool', 'missing_ok'),
]

DefineStmt = [
  ('ObjectType', 'kind'),
  ('bool', 'oldstyle'),
  ('List*', 'defnames'),
  ('List*', 'args'),
  ('List*', 'definition'),
  ('bool', 'if_not_exists'),
  ('bool', 'replace'),
]

CreateDomainStmt = [
  ('List*', 'domainname'),
  ('TypeName*', 'typeName'),
  ('CollateClause*', 'collClause'),
  ('List*', 'constraints'),
]

CreateOpClassStmt = [
  ('List*', 'opclassname'),
  ('List*', 'opfamilyname'),
  ('char*', 'amname'),
  ('TypeName*', 'datatype'),
  ('List*', 'items'),
  ('bool', 'isDefault'),
]

CreateOpClassItem = [
  ('int', 'itemtype'),
  ('ObjectWithArgs*', 'name'),
  ('int', 'number'),
  ('List*', 'order_family'),
  ('List*', 'class_args'),
  ('TypeName*', 'storedtype'),
]

CreateOpFamilyStmt = [
  ('List*', 'opfamilyname'),
  ('char*', 'amname'),
]

AlterOpFamilyStmt = [
  ('List*', 'opfamilyname'),
  ('char*', 'amname'),
  ('bool', 'isDrop'),
  ('List*', 'items'),
]

DropStmt = [
  ('List*', 'objects'),
  ('ObjectType', 'removeType'),
  ('DropBehavior', 'behavior'),
  ('bool', 'missing_ok'),
  ('bool', 'concurrent'),
]

TruncateStmt = [
  ('List*', 'relations'),
  ('bool', 'restart_seqs'),
  ('DropBehavior', 'behavior'),
]

CommentStmt = [
  ('ObjectType', 'objtype'),
  ('Node*', 'object'),
  ('char*', 'comment'),
]

SecLabelStmt = [
  ('ObjectType', 'objtype'),
  ('Node*', 'object'),
  ('char*', 'provider'),
  ('char*', 'label'),
]

DeclareCursorStmt = [
  ('char*', 'portalname'),
  ('int', 'options'),
  ('Node*', 'query'),
]

ClosePortalStmt = [
  ('char*', 'portalname'),
]

FetchStmt = [
  ('FetchDirection', 'direction'),
  ('long', 'howMany'),
  ('char*', 'portalname'),
  ('bool', 'ismove'),
]

IndexStmt = [
  ('char*', 'idxname'),
  ('RangeVar*', 'relation'),
  ('char*', 'accessMethod'),
  ('char*', 'tableSpace'),
  ('List*', 'indexParams'),
  ('List*', 'indexIncludingParams'),
  ('List*', 'options'),
  ('Node*', 'whereClause'),
  ('List*', 'excludeOpNames'),
  ('char*', 'idxcomment'),
  ('Oid', 'indexOid'),
  ('RelFileNumber', 'oldNumber'),
  ('SubTransactionId', 'oldCreateSubid'),
  ('SubTransactionId', 'oldFirstRelfilelocatorSubid'),
  ('bool', 'unique'),
  ('bool', 'nulls_not_distinct'),
  ('bool', 'primary'),
  ('bool', 'isconstraint'),
  ('bool', 'deferrable'),
  ('bool', 'initdeferred'),
  ('bool', 'transformed'),
  ('bool', 'concurrent'),
  ('bool', 'if_not_exists'),
  ('bool', 'reset_default_tblspc'),
]

CreateStatsStmt = [
  ('List*', 'defnames'),
  ('List*', 'stat_types'),
  ('List*', 'exprs'),
  ('List*', 'relations'),
  ('char*', 'stxcomment'),
  ('bool', 'transformed'),
  ('bool', 'if_not_exists'),
]

StatsElem = [
  ('char*', 'name'),
  ('Node*', 'expr'),
]

AlterStatsStmt = [
  ('List*', 'defnames'),
  ('int', 'stxstattarget'),
  ('bool', 'missing_ok'),
]

CreateFunctionStmt = [
  ('bool', 'is_procedure'),
  ('bool', 'replace'),
  ('List*', 'funcname'),
  ('List*', 'parameters'),
  ('TypeName*', 'returnType'),
  ('List*', 'options'),
  ('Node*', 'sql_body'),
]

FunctionParameter = [
  ('char*', 'name'),
  ('TypeName*', 'argType'),
  ('FunctionParameterMode', 'mode'),
  ('Node*', 'defexpr'),
]

AlterFunctionStmt = [
  ('ObjectType', 'objtype'),
  ('ObjectWithArgs*', 'func'),
  ('List*', 'actions'),
]

DoStmt = [
  ('List*', 'args'),
]

CallStmt = [
  ('FuncCall*', 'funccall'),
  ('FuncExpr*', 'funcexpr'),
  ('List*', 'outargs'),
]

RenameStmt = [
  ('ObjectType', 'renameType'),
  ('ObjectType', 'relationType'),
  ('RangeVar*', 'relation'),
  ('Node*', 'object'),
  ('char*', 'subname'),
  ('char*', 'newname'),
  ('DropBehavior', 'behavior'),
  ('bool', 'missing_ok'),
]

AlterObjectDependsStmt = [
  ('ObjectType', 'objectType'),
  ('RangeVar*', 'relation'),
  ('Node*', 'object'),
  ('String*', 'extname'),
  ('bool', 'remove'),
]

AlterObjectSchemaStmt = [
  ('ObjectType', 'objectType'),
  ('RangeVar*', 'relation'),
  ('Node*', 'object'),
  ('char*', 'newschema'),
  ('bool', 'missing_ok'),
]

AlterOwnerStmt = [
  ('ObjectType', 'objectType'),
  ('RangeVar*', 'relation'),
  ('Node*', 'object'),
  ('RoleSpec*', 'newowner'),
]

AlterOperatorStmt = [
  ('ObjectWithArgs*', 'opername'),
  ('List*', 'options'),
]

AlterTypeStmt = [
  ('List*', 'typeName'),
  ('List*', 'options'),
]

RuleStmt = [
  ('RangeVar*', 'relation'),
  ('char*', 'rulename'),
  ('Node*', 'whereClause'),
  ('CmdType', 'event'),
  ('bool', 'instead'),
  ('List*', 'actions'),
  ('bool', 'replace'),
]

NotifyStmt = [
  ('char*', 'conditionname'),
  ('char*', 'payload'),
]

ListenStmt = [
  ('char*', 'conditionname'),
]

UnlistenStmt = [
  ('char*', 'conditionname'),
]

TransactionStmt = [
  ('TransactionStmtKind', 'kind'),
  ('List*', 'options'),
  ('char*', 'savepoint_name'),
  ('char*', 'gid'),
  ('bool', 'chain'),
]

CompositeTypeStmt = [
  ('RangeVar*', 'typevar'),
  ('List*', 'coldeflist'),
]

CreateEnumStmt = [
  ('List*', 'typeName'),
  ('List*', 'vals'),
]

CreateRangeStmt = [
  ('List*', 'typeName'),
  ('List*', 'params'),
]

AlterEnumStmt = [
  ('List*', 'typeName'),
  ('char*', 'oldVal'),
  ('char*', 'newVal'),
  ('char*', 'newValNeighbor'),
  ('bool', 'newValIsAfter'),
  ('bool', 'skipIfNewValExists'),
]

ViewStmt = [
  ('RangeVar*', 'view'),
  ('List*', 'aliases'),
  ('Node*', 'query'),
  ('bool', 'replace'),
  ('List*', 'options'),
  ('ViewCheckOption', 'withCheckOption'),
]

LoadStmt = [
  ('char*', 'filename'),
]

CreatedbStmt = [
  ('char*', 'dbname'),
  ('List*', 'options'),
]

AlterDatabaseStmt = [
  ('char*', 'dbname'),
  ('List*', 'options'),
]

AlterDatabaseRefreshCollStmt = [
  ('char*', 'dbname'),
]

AlterDatabaseSetStmt = [
  ('char*', 'dbname'),
  ('VariableSetStmt*', 'setstmt'),
]

DropdbStmt = [
  ('char*', 'dbname'),
  ('bool', 'missing_ok'),
  ('List*', 'options'),
]

AlterSystemStmt = [
  ('VariableSetStmt*', 'setstmt'),
]

ClusterStmt = [
  ('RangeVar*', 'relation'),
  ('char*', 'indexname'),
  ('List*', 'params'),
]

VacuumStmt = [
  ('List*', 'options'),
  ('List*', 'rels'),
  ('bool', 'is_vacuumcmd'),
]

VacuumRelation = [
  ('RangeVar*', 'relation'),
  ('Oid', 'oid'),
  ('List*', 'va_cols'),
]

ExplainStmt = [
  ('Node*', 'query'),
  ('List*', 'options'),
]

CreateTableAsStmt = [
  ('Node*', 'query'),
  ('IntoClause*', 'into'),
  ('ObjectType', 'objtype'),
  ('bool', 'is_select_into'),
  ('bool', 'if_not_exists'),
]

RefreshMatViewStmt = [
  ('bool', 'concurrent'),
  ('bool', 'skipData'),
  ('RangeVar*', 'relation'),
]

CheckPointStmt = [
]

DiscardStmt = [
  ('DiscardMode', 'target'),
]

LockStmt = [
  ('List*', 'relations'),
  ('int', 'mode'),
  ('bool', 'nowait'),
]

ConstraintsSetStmt = [
  ('List*', 'constraints'),
  ('bool', 'deferred'),
]

ReindexStmt = [
  ('ReindexObjectType', 'kind'),
  ('RangeVar*', 'relation'),
  ('char*', 'name'),
  ('List*', 'params'),
]

CreateConversionStmt = [
  ('List*', 'conversion_name'),
  ('char*', 'for_encoding_name'),
  ('char*', 'to_encoding_name'),
  ('List*', 'func_name'),
  ('bool', 'def'),
]

CreateCastStmt = [
  ('TypeName*', 'sourcetype'),
  ('TypeName*', 'targettype'),
  ('ObjectWithArgs*', 'func'),
  ('CoercionContext', 'context'),
  ('bool', 'inout'),
]

CreateTransformStmt = [
  ('bool', 'replace'),
  ('TypeName*', 'type_name'),
  ('char*', 'lang'),
  ('ObjectWithArgs*', 'fromsql'),
  ('ObjectWithArgs*', 'tosql'),
]

PrepareStmt = [
  ('char*', 'name'),
  ('List*', 'argtypes'),
  ('Node*', 'query'),
]

ExecuteStmt = [
  ('char*', 'name'),
  ('List*', 'params'),
]

DeallocateStmt = [
  ('char*', 'name'),
]

DropOwnedStmt = [
  ('List*', 'roles'),
  ('DropBehavior', 'behavior'),
]

ReassignOwnedStmt = [
  ('List*', 'roles'),
  ('RoleSpec*', 'newrole'),
]

AlterTSDictionaryStmt = [
  ('List*', 'dictname'),
  ('List*', 'options'),
]

AlterTSConfigurationStmt = [
  ('AlterTSConfigType', 'kind'),
  ('List*', 'cfgname'),
  ('List*', 'tokentype'),
  ('List*', 'dicts'),
  ('bool', 'override'),
  ('bool', 'replace'),
  ('bool', 'missing_ok'),
]

PublicationTable = [
  ('RangeVar*', 'relation'),
  ('Node*', 'whereClause'),
  ('List*', 'columns'),
]

PublicationObjSpec = [
  ('PublicationObjSpecType', 'pubobjtype'),
  ('char*', 'name'),
  ('PublicationTable*', 'pubtable'),
  ('int', 'location'),
]

CreatePublicationStmt = [
  ('char*', 'pubname'),
  ('List*', 'options'),
  ('List*', 'pubobjects'),
  ('bool', 'for_all_tables'),
]

AlterPublicationStmt = [
  ('char*', 'pubname'),
  ('List*', 'options'),
  ('List*', 'pubobjects'),
  ('bool', 'for_all_tables'),
  ('AlterPublicationAction', 'action'),
]

CreateSubscriptionStmt = [
  ('char*', 'subname'),
  ('char*', 'conninfo'),
  ('List*', 'publication'),
  ('List*', 'options'),
]

AlterSubscriptionStmt = [
  ('AlterSubscriptionType', 'kind'),
  ('char*', 'subname'),
  ('char*', 'conninfo'),
  ('List*', 'publication'),
  ('List*', 'options'),
]

DropSubscriptionStmt = [
  ('char*', 'subname'),
  ('bool', 'missing_ok'),
  ('DropBehavior', 'behavior'),
]

PlannerGlobal = [
  ('ParamListInfo', 'boundParams'),
  ('List*', 'subplans'),
  ('List*', 'subroots'),
  ('Bitmapset*', 'rewindPlanIDs'),
  ('List*', 'finalrtable'),
  ('List*', 'finalrteperminfos'),
  ('List*', 'finalrowmarks'),
  ('List*', 'resultRelations'),
  ('List*', 'appendRelations'),
  ('List*', 'relationOids'),
  ('List*', 'invalItems'),
  ('List*', 'paramExecTypes'),
  ('Index', 'lastPHId'),
  ('Index', 'lastRowMarkId'),
  ('int', 'lastPlanNodeId'),
  ('bool', 'transientPlan'),
  ('bool', 'dependsOnRole'),
  ('bool', 'parallelModeOK'),
  ('bool', 'parallelModeNeeded'),
  ('char', 'maxParallelHazard'),
  ('PartitionDirectory', 'partition_directory'),
]

PlannerInfo = [
  ('Query*', 'parse'),
  ('PlannerGlobal*', 'glob'),
  ('Index', 'query_level'),
  ('PlannerInfo*', 'parent_root'),
  ('List*', 'plan_params'),
  ('Bitmapset*', 'outer_params'),
  ('struct RelOptInfo**', 'simple_rel_array'),
  ('int', 'simple_rel_array_size'),
  ('RangeTblEntry**', 'simple_rte_array'),
  ('struct AppendRelInfo**', 'append_rel_array'),
  ('Relids', 'all_baserels'),
  ('Relids', 'outer_join_rels'),
  ('Relids', 'all_query_rels'),
  ('List*', 'join_rel_list'),
  ('struct HTAB*', 'join_rel_hash'),
  ('List**', 'join_rel_level'),
  ('int', 'join_cur_level'),
  ('List*', 'init_plans'),
  ('List*', 'cte_plan_ids'),
  ('List*', 'multiexpr_params'),
  ('List*', 'join_domains'),
  ('List*', 'eq_classes'),
  ('bool', 'ec_merging_done'),
  ('List*', 'canon_pathkeys'),
  ('List*', 'left_join_clauses'),
  ('List*', 'right_join_clauses'),
  ('List*', 'full_join_clauses'),
  ('List*', 'join_info_list'),
  ('int', 'last_rinfo_serial'),
  ('Relids', 'all_result_relids'),
  ('Relids', 'leaf_result_relids'),
  ('List*', 'append_rel_list'),
  ('List*', 'row_identity_vars'),
  ('List*', 'rowMarks'),
  ('List*', 'placeholder_list'),
  ('struct PlaceHolderInfo**', 'placeholder_array'),
  ('int', 'placeholder_array_size'),
  ('List*', 'fkey_list'),
  ('List*', 'query_pathkeys'),
  ('List*', 'group_pathkeys'),
  ('int', 'num_groupby_pathkeys'),
  ('List*', 'window_pathkeys'),
  ('List*', 'distinct_pathkeys'),
  ('List*', 'sort_pathkeys'),
  ('List*', 'part_schemes'),
  ('List*', 'initial_rels'),
  ('List*[UPPERREL_FINAL + 1]', 'upper_rels'),
  ('struct PathTarget*[UPPERREL_FINAL + 1]', 'upper_targets'),
  ('List*', 'processed_groupClause'),
  ('List*', 'processed_distinctClause'),
  ('List*', 'processed_tlist'),
  ('List*', 'update_colnos'),
  ('AttrNumber*', 'grouping_map'),
  ('List*', 'minmax_aggs'),
  ('Cardinality', 'total_table_pages'),
  ('Selectivity', 'tuple_fraction'),
  ('Cardinality', 'limit_tuples'),
  ('Index', 'qual_security_level'),
  ('bool', 'hasJoinRTEs'),
  ('bool', 'hasLateralRTEs'),
  ('bool', 'hasHavingQual'),
  ('bool', 'hasPseudoConstantQuals'),
  ('bool', 'hasAlternativeSubPlans'),
  ('bool', 'placeholdersFrozen'),
  ('bool', 'hasRecursion'),
  ('List*', 'agginfos'),
  ('List*', 'aggtransinfos'),
  ('int', 'numOrderedAggs'),
  ('bool', 'hasNonPartialAggs'),
  ('bool', 'hasNonSerialAggs'),
  ('int', 'wt_param_id'),
  ('struct Path*', 'non_recursive_path'),
  ('Relids', 'curOuterRels'),
  ('List*', 'curOuterParams'),
  ('bool*', 'isAltSubplan'),
  ('bool*', 'isUsedSubplan'),
  ('void*', 'join_search_private'),
  ('bool', 'partColsUpdated'),
]

RelOptInfo = [
  ('RelOptKind', 'reloptkind'),
  ('Relids', 'relids'),
  ('Cardinality', 'rows'),
  ('bool', 'consider_startup'),
  ('bool', 'consider_param_startup'),
  ('bool', 'consider_parallel'),
  ('struct PathTarget*', 'reltarget'),
  ('List*', 'pathlist'),
  ('List*', 'ppilist'),
  ('List*', 'partial_pathlist'),
  ('struct Path*', 'cheapest_startup_path'),
  ('struct Path*', 'cheapest_total_path'),
  ('struct Path*', 'cheapest_unique_path'),
  ('List*', 'cheapest_parameterized_paths'),
  ('Relids', 'direct_lateral_relids'),
  ('Relids', 'lateral_relids'),
  ('Index', 'relid'),
  ('Oid', 'reltablespace'),
  ('RTEKind', 'rtekind'),
  ('AttrNumber', 'min_attr'),
  ('AttrNumber', 'max_attr'),
  ('Relids*', 'attr_needed'),
  ('int32*', 'attr_widths'),
  ('Relids', 'nulling_relids'),
  ('List*', 'lateral_vars'),
  ('Relids', 'lateral_referencers'),
  ('List*', 'indexlist'),
  ('List*', 'statlist'),
  ('BlockNumber', 'pages'),
  ('Cardinality', 'tuples'),
  ('double', 'allvisfrac'),
  ('Bitmapset*', 'eclass_indexes'),
  ('PlannerInfo*', 'subroot'),
  ('List*', 'subplan_params'),
  ('int', 'rel_parallel_workers'),
  ('uint32', 'amflags'),
  ('Oid', 'serverid'),
  ('Oid', 'userid'),
  ('bool', 'useridiscurrent'),
  ('struct FdwRoutine*', 'fdwroutine'),
  ('void*', 'fdw_private'),
  ('List*', 'unique_for_rels'),
  ('List*', 'non_unique_for_rels'),
  ('List*', 'baserestrictinfo'),
  ('QualCost', 'baserestrictcost'),
  ('Index', 'baserestrict_min_security'),
  ('List*', 'joininfo'),
  ('bool', 'has_eclass_joins'),
  ('bool', 'consider_partitionwise_join'),
  ('struct RelOptInfo*', 'parent'),
  ('struct RelOptInfo*', 'top_parent'),
  ('Relids', 'top_parent_relids'),
  ('PartitionScheme', 'part_scheme'),
  ('int', 'nparts'),
  ('struct PartitionBoundInfoData*', 'boundinfo'),
  ('bool', 'partbounds_merged'),
  ('List*', 'partition_qual'),
  ('struct RelOptInfo**', 'part_rels'),
  ('Bitmapset*', 'live_parts'),
  ('Relids', 'all_partrels'),
  ('List**', 'partexprs'),
  ('List**', 'nullable_partexprs'),
]

IndexOptInfo = [
  ('Oid', 'indexoid'),
  ('Oid', 'reltablespace'),
  ('RelOptInfo*', 'rel'),
  ('BlockNumber', 'pages'),
  ('Cardinality', 'tuples'),
  ('int', 'tree_height'),
  ('int', 'ncolumns'),
  ('int', 'nkeycolumns'),
  ('int*', 'indexkeys'),
  ('Oid*', 'indexcollations'),
  ('Oid*', 'opfamily'),
  ('Oid*', 'opcintype'),
  ('Oid*', 'sortopfamily'),
  ('bool*', 'reverse_sort'),
  ('bool*', 'nulls_first'),
  ('bytea**', 'opclassoptions'),
  ('bool*', 'canreturn'),
  ('Oid', 'relam'),
  ('List*', 'indexprs'),
  ('List*', 'indpred'),
  ('List*', 'indextlist'),
  ('List*', 'indrestrictinfo'),
  ('bool', 'predOK'),
  ('bool', 'unique'),
  ('bool', 'immediate'),
  ('bool', 'hypothetical'),
  ('bool', 'amcanorderbyop'),
  ('bool', 'amoptionalkey'),
  ('bool', 'amsearcharray'),
  ('bool', 'amsearchnulls'),
  ('bool', 'amhasgettuple'),
  ('bool', 'amhasgetbitmap'),
  ('bool', 'amcanparallel'),
  ('bool', 'amcanmarkpos'),
  ('function pointer', 'amcostestimate'),
]

ForeignKeyOptInfo = [
  ('Index', 'con_relid'),
  ('Index', 'ref_relid'),
  ('int', 'nkeys'),
  ('AttrNumber[INDEX_MAX_KEYS]', 'conkey'),
  ('AttrNumber[INDEX_MAX_KEYS]', 'confkey'),
  ('Oid[INDEX_MAX_KEYS]', 'conpfeqop'),
  ('int', 'nmatched_ec'),
  ('int', 'nconst_ec'),
  ('int', 'nmatched_rcols'),
  ('int', 'nmatched_ri'),
  ('struct EquivalenceClass*[INDEX_MAX_KEYS]', 'eclass'),
  ('struct EquivalenceMember*[INDEX_MAX_KEYS]', 'fk_eclass_member'),
  ('List*[INDEX_MAX_KEYS]', 'rinfos'),
]

StatisticExtInfo = [
  ('Oid', 'statOid'),
  ('bool', 'inherit'),
  ('RelOptInfo*', 'rel'),
  ('char', 'kind'),
  ('Bitmapset*', 'keys'),
  ('List*', 'exprs'),
]

JoinDomain = [
  ('Relids', 'jd_relids'),
]

EquivalenceClass = [
  ('List*', 'ec_opfamilies'),
  ('Oid', 'ec_collation'),
  ('List*', 'ec_members'),
  ('List*', 'ec_sources'),
  ('List*', 'ec_derives'),
  ('Relids', 'ec_relids'),
  ('bool', 'ec_has_const'),
  ('bool', 'ec_has_volatile'),
  ('bool', 'ec_broken'),
  ('Index', 'ec_sortref'),
  ('Index', 'ec_min_security'),
  ('Index', 'ec_max_security'),
  ('struct EquivalenceClass*', 'ec_merged'),
]

EquivalenceMember = [
  ('Expr*', 'em_expr'),
  ('Relids', 'em_relids'),
  ('Relids', 'em_nullable_relids'),
  ('bool', 'em_is_const'),
  ('bool', 'em_is_child'),
  ('Oid', 'em_datatype'),
]

PathKey = [
  ('EquivalenceClass*', 'pk_eclass'),
  ('Oid', 'pk_opfamily'),
  ('int', 'pk_strategy'),
  ('bool', 'pk_nulls_first'),
]

PathTarget = [
  ('List*', 'exprs'),
  ('Index*', 'sortgrouprefs'),
  ('QualCost', 'cost'),
  ('int', 'width'),
]

ParamPathInfo = [
  ('Relids', 'ppi_req_outer'),
  ('Cardinality', 'ppi_rows'),
  ('List*', 'ppi_clauses'),
  ('Bitmapset*', 'ppi_serials'),
]

IndexPath = [
  ('Path', 'path'),
  ('IndexOptInfo*', 'indexinfo'),
  ('List*', 'indexclauses'),
  ('List*', 'indexorderbys'),
  ('List*', 'indexorderbycols'),
  ('ScanDirection', 'indexscandir'),
  ('Cost', 'indextotalcost'),
  ('Selectivity', 'indexselectivity'),
]

IndexClause = [
  ('struct RestrictInfo*', 'rinfo'),
  ('List*', 'indexquals'),
  ('bool', 'lossy'),
  ('AttrNumber', 'indexcol'),
  ('List*', 'indexcols'),
]

BitmapHeapPath = [
  ('Path', 'path'),
  ('Path*', 'bitmapqual'),
]

BitmapAndPath = [
  ('Path', 'path'),
  ('List*', 'bitmapquals'),
  ('Selectivity', 'bitmapselectivity'),
]

BitmapOrPath = [
  ('Path', 'path'),
  ('List*', 'bitmapquals'),
  ('Selectivity', 'bitmapselectivity'),
]

TidPath = [
  ('Path', 'path'),
  ('List*', 'tidquals'),
]

SubqueryScanPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
]

ForeignPath = [
  ('Path', 'path'),
  ('Path*', 'fdw_outerpath'),
  ('List*', 'fdw_private'),
]

CustomPath = [
  ('Path', 'path'),
  ('uint32', 'flags'),
  ('List*', 'custom_paths'),
  ('List*', 'custom_private'),
  ('struct CustomPathMethods*', 'methods'),
]

AppendPath = [
  ('Path', 'path'),
  ('List*', 'subpaths'),
  ('int', 'first_partial_path'),
  ('Cardinality', 'limit_tuples'),
]

MergeAppendPath = [
  ('Path', 'path'),
  ('List*', 'subpaths'),
  ('Cardinality', 'limit_tuples'),
]

GroupResultPath = [
  ('Path', 'path'),
  ('List*', 'quals'),
]

MaterialPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
]

UniquePath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('UniquePathMethod', 'umethod'),
  ('List*', 'in_operators'),
  ('List*', 'uniq_exprs'),
]

GatherPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('bool', 'single_copy'),
  ('int', 'num_workers'),
]

GatherMergePath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('int', 'num_workers'),
]

JoinPath = [
  ('Path', 'path'),
  ('JoinType', 'jointype'),
  ('bool', 'inner_unique'),
  ('Path*', 'outerjoinpath'),
  ('Path*', 'innerjoinpath'),
  ('List*', 'joinrestrictinfo'),
]

MergePath = [
  ('JoinPath', 'jpath'),
  ('List*', 'path_mergeclauses'),
  ('List*', 'outersortkeys'),
  ('List*', 'innersortkeys'),
  ('bool', 'skip_mark_restore'),
  ('bool', 'materialize_inner'),
]

HashPath = [
  ('JoinPath', 'jpath'),
  ('List*', 'path_hashclauses'),
  ('int', 'num_batches'),
  ('Cardinality', 'inner_rows_total'),
]

ProjectionPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('bool', 'dummypp'),
]

ProjectSetPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
]

SortPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
]

IncrementalSortPath = [
  ('SortPath', 'spath'),
  ('int', 'nPresortedCols'),
]

GroupPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('List*', 'groupClause'),
  ('List*', 'qual'),
]

UpperUniquePath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('int', 'numkeys'),
]

AggPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('AggStrategy', 'aggstrategy'),
  ('AggSplit', 'aggsplit'),
  ('Cardinality', 'numGroups'),
  ('List*', 'groupClause'),
  ('List*', 'qual'),
  ('bool', 'streaming'),
]

GroupingSetData = [
  ('List*', 'set'),
  ('Cardinality', 'numGroups'),
]

RollupData = [
  ('List*', 'groupClause'),
  ('List*', 'gsets'),
  ('List*', 'gsets_data'),
  ('Cardinality', 'numGroups'),
  ('bool', 'hashable'),
  ('bool', 'is_hashed'),
]

GroupingSetsPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('AggStrategy', 'aggstrategy'),
  ('AggSplit', 'aggsplit'),
  ('List*', 'rollups'),
  ('List*', 'qual'),
]

MinMaxAggPath = [
  ('Path', 'path'),
  ('List*', 'mmaggregates'),
  ('List*', 'quals'),
]

WindowAggPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('WindowClause*', 'winclause'),
  ('List*', 'qual'),
  ('bool', 'topwindow'),
]

SetOpPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('SetOpCmd', 'cmd'),
  ('SetOpStrategy', 'strategy'),
  ('List*', 'distinctList'),
  ('AttrNumber', 'flagColIdx'),
  ('int', 'firstFlag'),
  ('Cardinality', 'numGroups'),
]

RecursiveUnionPath = [
  ('Path', 'path'),
  ('Path*', 'leftpath'),
  ('Path*', 'rightpath'),
  ('List*', 'distinctList'),
  ('int', 'wtParam'),
  ('Cardinality', 'numGroups'),
]

LockRowsPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('List*', 'rowMarks'),
  ('int', 'epqParam'),
]

ModifyTablePath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('CmdType', 'operation'),
  ('bool', 'canSetTag'),
  ('Index', 'nominalRelation'),
  ('Index', 'rootRelation'),
  ('bool', 'partColsUpdated'),
  ('List*', 'resultRelations'),
  ('List*', 'updateColnosLists'),
  ('List*', 'withCheckOptionLists'),
  ('List*', 'returningLists'),
  ('List*', 'rowMarks'),
  ('OnConflictExpr*', 'onconflict'),
  ('int', 'epqParam'),
  ('List*', 'mergeActionLists'),
]

LimitPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('Node*', 'limitOffset'),
  ('Node*', 'limitCount'),
]

CdbMotionPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('bool', 'is_explicit_motion'),
  ('GpPolicy*', 'policy'),
]

AppendOnlyPath = [
  ('Path', 'path'),
]

AOCSPath = [
  ('Path', 'path'),
]

PartitionSelectorPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('int', 'paramid'),
  ('struct PartitionPruneInfo*', 'part_prune_info'),
]

CtePath = [
  ('Path', 'path'),
  ('Path*', 'subpath;'),
]

TableFunctionScanPath = [
  ('Path', 'path'),
  ('Path*', 'subpath;'),
]

TupleSplitPath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('List*', 'groupClause'),
  ('List*', 'dqa_expr_lst'),
]

SplitUpdatePath = [
  ('Path', 'path'),
  ('Path*', 'subpath'),
  ('Index', 'resultRelation'),
]

RestrictInfo = [
  ('Expr*', 'clause'),
  ('bool', 'is_pushed_down'),
  ('bool', 'outerjoin_delayed'),
  ('bool', 'can_join'),
  ('bool', 'pseudoconstant'),
  ('bool', 'leakproof'),
  ('Index', 'security_level'),
  ('bool', 'contain_outer_query_references'),
  ('Relids', 'clause_relids'),
  ('Relids', 'required_relids'),
  ('Relids', 'outer_relids'),
  ('Relids', 'nullable_relids'),
  ('Relids', 'left_relids'),
  ('Relids', 'right_relids'),
  ('Expr*', 'orclause'),
  ('EquivalenceClass*', 'parent_ec'),
  ('QualCost', 'eval_cost'),
  ('Selectivity', 'norm_selec'),
  ('Selectivity', 'outer_selec'),
  ('List*', 'mergeopfamilies'),
  ('EquivalenceClass*', 'left_ec'),
  ('EquivalenceClass*', 'right_ec'),
  ('EquivalenceMember*', 'left_em'),
  ('EquivalenceMember*', 'right_em'),
  # MergeScanSelCache   not a Node
  # ('List*', 'scansel_cache'),
  ('bool', 'outer_is_left'),
  ('Oid', 'hashjoinoperator'),
  ('Selectivity', 'left_bucketsize'),
  ('Selectivity', 'right_bucketsize'),
  ('Selectivity', 'left_mcvfreq'),
  ('Selectivity', 'right_mcvfreq'),
]

PlaceHolderVar = [
  ('Expr*', 'phexpr'),
  ('Relids', 'phrels'),
  ('Relids', 'phnullingrels'),
  ('Index', 'phid'),
  ('Index', 'phlevelsup'),
]

SpecialJoinInfo = [
  ('Relids', 'min_lefthand'),
  ('Relids', 'min_righthand'),
  ('Relids', 'syn_lefthand'),
  ('Relids', 'syn_righthand'),
  ('JoinType', 'jointype'),
  ('Index', 'ojrelid'),
  ('Relids', 'commute_above_l'),
  ('Relids', 'commute_above_r'),
  ('Relids', 'commute_below_l'),
  ('Relids', 'commute_below_r'),
  ('bool', 'lhs_strict'),
  ('bool', 'semi_can_btree'),
  ('bool', 'semi_can_hash'),
  ('List*', 'semi_operators'),
  ('List*', 'semi_rhs_exprs'),
]

OuterJoinClauseInfo = [
  ('RestrictInfo*', 'rinfo'),
  ('SpecialJoinInfo*', 'sjinfo'),
]

AppendRelInfo = [
  ('Index', 'parent_relid'),
  ('Index', 'child_relid'),
  ('Oid', 'parent_reltype'),
  ('Oid', 'child_reltype'),
  ('List*', 'translated_vars'),
  ('int', 'num_child_cols'),
  ('AttrNumber*', 'parent_colnos'),
  ('Oid', 'parent_reloid'),
]

RowIdentityVarInfo = [
  ('Var*', 'rowidvar'),
  ('int32', 'rowidwidth'),
  ('char*', 'rowidname'),
  ('Relids', 'rowidrels'),
]

PlaceHolderInfo = [
  ('Index', 'phid'),
  ('PlaceHolderVar*', 'ph_var'),
  ('Relids', 'ph_eval_at'),
  ('Relids', 'ph_lateral'),
  ('Relids', 'ph_needed'),
  ('int32', 'ph_width'),
]

MinMaxAggInfo = [
  ('Oid', 'aggfnoid'),
  ('Oid', 'aggsortop'),
  ('Expr*', 'target'),
  ('PlannerInfo*', 'subroot'),
  ('Path*', 'path'),
  ('Cost', 'pathcost'),
  ('Param*', 'param'),
]

PlannerParamItem = [
  ('Node*', 'item'),
  ('int', 'paramId'),
]

AggInfo = [
  ('List*', 'aggrefs'),
  ('int', 'transno'),
  ('bool', 'shareable'),
  ('Oid', 'finalfn_oid'),
]

AggTransInfo = [
  ('List*', 'args'),
  ('Expr*', 'aggfilter'),
  ('Oid', 'transfn_oid'),
  ('Oid', 'serialfn_oid'),
  ('Oid', 'deserialfn_oid'),
  ('Oid', 'combinefn_oid'),
  ('Oid', 'aggtranstype'),
  ('int32', 'aggtranstypmod'),
  ('int', 'transtypeLen'),
  ('bool', 'transtypeByVal'),
  ('int32', 'aggtransspace'),
  ('Datum', 'initValue'),
  ('bool', 'initValueIsNull'),
]

PlannedStmt = [
  ('CmdType', 'commandType'),
  ('PlanGenerator', 'planGen'),
  ('uint64', 'queryId'),
  ('bool', 'hasReturning'),
  ('bool', 'hasModifyingCTE'),
  ('bool', 'canSetTag'),
  ('bool', 'transientPlan'),
  ('bool', 'oneoffPlan'),
  ('Oid', 'simplyUpdatableRel'),
  ('bool', 'dependsOnRole'),
  ('bool', 'parallelModeNeeded'),
  ('int', 'jitFlags'),
  ('struct Plan*', 'planTree'),
  ('int', 'numSlices'),
  ('struct PlanSlice*', 'slices'),
  ('List*', 'rtable'),
  ('List*', 'resultRelations'),
  ('List*', 'rootResultRelations'),
  ('List*', 'subplans'),
  ('int*', 'subplan_sliceIds'),
  ('Bitmapset*', 'rewindPlanIDs'),
  ('List*', 'rowMarks'),
  ('List*', 'relationOids'),
  ('List*', 'invalItems'),
  ('List*', 'paramExecTypes'),
  ('Node*', 'utilityStmt'),
  ('int', 'stmt_location'),
  ('int', 'stmt_len'),
  ('struct GpPolicy*', 'intoPolicy'),
  ('uint64', 'query_mem'),
  ('IntoClause*', 'intoClause'),
  ('CopyIntoClause*', 'copyIntoClause'),
  ('RefreshClause*', 'refreshClause'),
  ('int8', 'metricsQueryType'),
]

Result = [
  ('Plan', 'plan'),
  ('Node*', 'resconstantqual'),
]

ProjectSet = [
  ('Plan', 'plan'),
]

ModifyTable = [
  ('Plan', 'plan'),
  ('CmdType', 'operation'),
  ('bool', 'canSetTag'),
  ('Index', 'nominalRelation'),
  ('Index', 'rootRelation'),
  ('bool', 'partColsUpdated'),
  ('List*', 'resultRelations'),
  ('List*', 'updateColnosLists'),
  ('List*', 'withCheckOptionLists'),
  ('List*', 'returningLists'),
  ('List*', 'fdwPrivLists'),
  ('Bitmapset*', 'fdwDirectModifyPlans'),
  ('List*', 'rowMarks'),
  ('int', 'epqParam'),
  ('OnConflictAction', 'onConflictAction'),
  ('List*', 'arbiterIndexes'),
  ('List*', 'onConflictSet'),
  ('List*', 'onConflictCols'),
  ('Node*', 'onConflictWhere'),
  ('Index', 'exclRelRTI'),
  ('List*', 'exclRelTlist'),
  ('List*', 'mergeActionLists'),
]

Append = [
  ('Plan', 'plan'),
  ('Bitmapset*', 'apprelids'),
  ('List*', 'appendplans'),
  ('int', 'nasyncplans'),
  ('int', 'first_partial_plan'),
  ('struct PartitionPruneInfo*', 'part_prune_info'),
]

MergeAppend = [
  ('Plan', 'plan'),
  ('Bitmapset*', 'apprelids'),
  ('List*', 'mergeplans'),
  ('int', 'numCols'),
  ('AttrNumber*', 'sortColIdx'),
  ('Oid*', 'sortOperators'),
  ('Oid*', 'collations'),
  ('bool*', 'nullsFirst'),
  ('struct PartitionPruneInfo*', 'part_prune_info'),
]

RecursiveUnion = [
  ('Plan', 'plan'),
  ('int', 'wtParam'),
  ('int', 'numCols'),
  ('AttrNumber*', 'dupColIdx'),
  ('Oid*', 'dupOperators'),
  ('Oid*', 'dupCollations'),
  ('long', 'numGroups'),
]

BitmapAnd = [
  ('Plan', 'plan'),
  ('List*', 'bitmapplans'),
]

BitmapOr = [
  ('Plan', 'plan'),
  ('bool', 'isshared'),
  ('List*', 'bitmapplans'),
]

Scan = [
  ('Plan', 'plan'),
  ('Index', 'scanrelid'),
]

SeqScan = [
  ('Scan', 'scan'),
]

SampleScan = [
  ('Scan', 'scan'),
  ('struct TableSampleClause*', 'tablesample'),
]

IndexScan = [
  ('Scan', 'scan'),
  ('Oid', 'indexid'),
  ('List*', 'indexqual'),
  ('List*', 'indexqualorig'),
  ('List*', 'indexorderby'),
  ('List*', 'indexorderbyorig'),
  ('List*', 'indexorderbyops'),
  ('ScanDirection', 'indexorderdir'),
]

IndexOnlyScan = [
  ('Scan', 'scan'),
  ('Oid', 'indexid'),
  ('List*', 'indexqual'),
  ('List*', 'recheckqual'),
  ('List*', 'indexorderby'),
  ('List*', 'indextlist'),
  ('ScanDirection', 'indexorderdir'),
]

BitmapIndexScan = [
  ('Scan', 'scan'),
  ('Oid', 'indexid'),
  ('bool', 'isshared'),
  ('List*', 'indexqual'),
  ('List*', 'indexqualorig'),
]

BitmapHeapScan = [
  ('Scan', 'scan'),
  ('List*', 'bitmapqualorig'),
]

TidScan = [
  ('Scan', 'scan'),
  ('List*', 'tidquals'),
]

TidRangeScan = [
  ('Scan', 'scan'),
  ('List*', 'tidrangequals'),
]

SubqueryScan = [
  ('Scan', 'scan'),
  ('Plan*', 'subplan'),
  ('SubqueryScanStatus', 'scanstatus'),
]

FunctionScan = [
  ('Scan', 'scan'),
  ('List*', 'functions'),
  ('bool', 'funcordinality'),
]

ValuesScan = [
  ('Scan', 'scan'),
  ('List*', 'values_lists'),
]

TableFuncScan = [
  ('Scan', 'scan'),
  ('TableFunc*', 'tablefunc'),
]

CteScan = [
  ('Scan', 'scan'),
  ('int', 'ctePlanId'),
  ('int', 'cteParam'),
]

NamedTuplestoreScan = [
  ('Scan', 'scan'),
  ('char*', 'enrname'),
]

WorkTableScan = [
  ('Scan', 'scan'),
  ('int', 'wtParam'),
]

ForeignScan = [
  ('Scan', 'scan'),
  ('CmdType', 'operation'),
  ('Index', 'resultRelation'),
  ('Oid', 'checkAsUser'),
  ('Oid', 'fs_server'),
  ('List*', 'fdw_exprs'),
  ('List*', 'fdw_private'),
  ('List*', 'fdw_scan_tlist'),
  ('List*', 'fdw_recheck_quals'),
  ('Bitmapset*', 'fs_relids'),
  ('Bitmapset*', 'fs_base_relids'),
  ('bool', 'fsSystemCol'),
]

CustomScan = [
  ('Scan', 'scan'),
  ('uint32', 'flags'),
  ('List*', 'custom_plans'),
  ('List*', 'custom_exprs'),
  ('List*', 'custom_private'),
  ('List*', 'custom_scan_tlist'),
  ('Bitmapset*', 'custom_relids'),
  ('struct CustomScanMethods*', 'methods'),
]

NestLoop = [
  ('Join', 'join'),
  ('List*', 'nestParams'),
  ('bool', 'shared_outer'),
  ('bool', 'singleton_outer'),
]

NestLoopParam = [
  ('int', 'paramno'),
  ('Var*', 'paramval'),
]

MergeJoin = [
  ('Join', 'join'),
  ('bool', 'skip_mark_restore'),
  ('List*', 'mergeclauses'),
  ('Oid*', 'mergeFamilies'),
  ('Oid*', 'mergeCollations'),
  ('int*', 'mergeStrategies'),
  ('bool*', 'mergeNullsFirst'),
  ('bool', 'unique_outer'),
]

HashJoin = [
  ('Join', 'join'),
  ('List*', 'hashclauses'),
  ('List*', 'hashoperators'),
  ('List*', 'hashcollations'),
  ('List*', 'hashkeys'),
]

Material = [
  ('Plan', 'plan'),
]

Memoize = [
  ('Plan', 'plan'),
  ('int', 'numKeys'),
  ('Oid*', 'hashOperators'),
  ('Oid*', 'collations'),
  ('List*', 'param_exprs'),
  ('bool', 'singlerow'),
  ('bool', 'binary_mode'),
  ('uint32', 'est_entries'),
  ('Bitmapset*', 'keyparamids'),
]

Sort = [
  ('Plan', 'plan'),
  ('int', 'numCols'),
  ('AttrNumber*', 'sortColIdx'),
  ('Oid*', 'sortOperators'),
  ('Oid*', 'collations'),
  ('bool*', 'nullsFirst'),
]

IncrementalSort = [
  ('Sort', 'sort'),
  ('int', 'nPresortedCols'),
]

Group = [
  ('Plan', 'plan'),
  ('int', 'numCols'),
  ('AttrNumber*', 'grpColIdx'),
  ('Oid*', 'grpOperators'),
  ('Oid*', 'grpCollations'),
]

Agg = [
  ('Plan', 'plan'),
  ('AggStrategy', 'aggstrategy'),
  ('AggSplit', 'aggsplit'),
  ('int', 'numCols'),
  ('AttrNumber*', 'grpColIdx'),
  ('Oid*', 'grpOperators'),
  ('Oid*', 'grpCollations'),
  ('long', 'numGroups'),
  ('Bitmapset*', 'aggParams'),
  ('List*', 'groupingSets'),
  ('List*', 'chain'),
  ('bool', 'streaming'),
  ('Index', 'agg_expr_id'),
]

WindowAgg = [
  ('Plan', 'plan'),
  ('Index', 'winref'),
  ('int', 'partNumCols'),
  ('AttrNumber*', 'partColIdx'),
  ('Oid*', 'partOperators'),
  ('Oid*', 'partCollations'),
  ('int', 'ordNumCols'),
  ('AttrNumber*', 'ordColIdx'),
  ('Oid*', 'ordOperators'),
  ('Oid*', 'ordCollations'),
  ('int', 'frameOptions'),
  ('Node*', 'startOffset'),
  ('Node*', 'endOffset'),
  ('List*', 'runCondition'),
  ('List*', 'runConditionOrig'),
  ('Oid', 'startInRangeFunc'),
  ('Oid', 'endInRangeFunc'),
  ('Oid', 'inRangeColl'),
  ('bool', 'inRangeAsc'),
  ('bool', 'inRangeNullsFirst'),
  ('bool', 'topWindow'),
]

Unique = [
  ('Plan', 'plan'),
  ('int', 'numCols'),
  ('AttrNumber*', 'uniqColIdx'),
  ('Oid*', 'uniqOperators'),
  ('Oid*', 'uniqCollations'),
]

Gather = [
  ('Plan', 'plan'),
  ('int', 'num_workers'),
  ('int', 'rescan_param'),
  ('bool', 'single_copy'),
  ('bool', 'invisible'),
  ('Bitmapset*', 'initParam'),
]

GatherMerge = [
  ('Plan', 'plan'),
  ('int', 'num_workers'),
  ('int', 'rescan_param'),
  ('int', 'numCols'),
  ('AttrNumber*', 'sortColIdx'),
  ('Oid*', 'sortOperators'),
  ('Oid*', 'collations'),
  ('bool*', 'nullsFirst'),
  ('Bitmapset*', 'initParam'),
]

Hash = [
  ('Plan', 'plan'),
  ('List*', 'hashkeys'),
  ('Oid', 'skewTable'),
  ('AttrNumber', 'skewColumn'),
  ('bool', 'skewInherit'),
  ('Cardinality', 'rows_total'),
]

SetOp = [
  ('Plan', 'plan'),
  ('SetOpCmd', 'cmd'),
  ('SetOpStrategy', 'strategy'),
  ('int', 'numCols'),
  ('AttrNumber*', 'dupColIdx'),
  ('Oid*', 'dupOperators'),
  ('Oid*', 'dupCollations'),
  ('AttrNumber', 'flagColIdx'),
  ('int', 'firstFlag'),
  ('long', 'numGroups'),
]

LockRows = [
  ('Plan', 'plan'),
  ('List*', 'rowMarks'),
  ('int', 'epqParam'),
]

Limit = [
  ('Plan', 'plan'),
  ('Node*', 'limitOffset'),
  ('Node*', 'limitCount'),
]

Motion = [
  ('Plan', 'plan'),
  ('MotionType',  'motionType'),
  ('bool', 'sendSorted'),
  ('int', 'motionID'),
  ('List*', 'hashExprs'),
  ('Oid*', 'hashFuncs'),
  ('int', 'numHashSegments'),
  ('AttrNumber', 'segidColIdx'),
  ('int', 'numSortCols'),
  ('AttrNumber*', 'sortColIdx'),
  ('Oid*', 'sortOperators'),
  ('Oid*', 'collations'),
  ('bool*', 'nullsFirst'),
  ('PlanSlice*', 'senderSliceInfo'),
]

PlanRowMark = [
  ('Index', 'rti'),
  ('Index', 'prti'),
  ('Index', 'rowmarkId'),
  ('RowMarkType', 'markType'),
  ('int', 'allMarkTypes'),
  ('LockClauseStrength', 'strength'),
  ('LockWaitPolicy', 'waitPolicy'),
  ('bool', 'isParent'),
]

PartitionPruneInfo = [
  ('List*', 'prune_infos'),
  ('Bitmapset*', 'other_subplans'),
]

PartitionedRelPruneInfo = [
  ('Index', 'rtindex'),
  ('Bitmapset*', 'present_parts'),
  ('int', 'nparts'),
  ('int*', 'subplan_map'),
  ('int*', 'subpart_map'),
  ('Oid*', 'relid_map'),
  ('List*', 'initial_pruning_steps'),
  ('List*', 'exec_pruning_steps'),
  ('Bitmapset*', 'execparamids'),
]

PartitionPruneStep = [
  ('int', 'step_id'),
]

PartitionPruneStepOp = [
  ('int', 'step.step_id'),
  ('StrategyNumber', 'opstrategy'),
  ('List*', 'exprs'),
  ('List*', 'cmpfns'),
  ('Bitmapset*', 'nullkeys'),
]

PartitionPruneStepCombine = [
  ('int', 'step.step_id'),
  ('PartitionPruneCombineOp', 'combineOp'),
  ('List*', 'source_stepids'),
]

PlanInvalItem = [
  ('int', 'cacheId'),
  ('uint32', 'hashValue'),
]

ExtensibleNode = [
  ('char*', 'extnodename'),
]

ForeignKeyCacheInfo = [
  ('Oid', 'conoid'),
  ('Oid', 'conrelid'),
  ('Oid', 'confrelid'),
  ('int', 'nkeys'),
  ('AttrNumber[INDEX_MAX_KEYS]', 'conkey'),
  ('AttrNumber[INDEX_MAX_KEYS]', 'confkey'),
  ('Oid[INDEX_MAX_KEYS]', 'conpfeqop'),
]

Flow = [
  ('NodeTag', 'type'),
  ('FlowType', 'flotype'),
  ('CdbLocusType', 'locustype'),
  ('int', 'segindex'),
  ('int', 'numsegments'),
]

PlanSlice = [
  ('int', 'sliceIndex'),
  ('int', 'parentIndex'),
  ('GangType', 'gangType'),
  ('int', 'numsegments'),
  ('int', 'segindex'),
  ('DirectDispatchInfo', 'directDispatch'),
]

DirectDispatchInfo = [
  ('bool', 'isDirectDispatch'),
  ('List*', 'contentIds'),
  ('bool', 'haveProcessedAnyCalculations'),
]

CdbPathLocus = [
  ('CdbLocusType', 'locustype'),
  ('List*', 'distkey'),
  ('int', 'numsegments'),
]

GpPolicy = [
  ('GpPolicyType', 'ptype'),
  ('int', 'numsegments'),
  ('int', 'nattrs'),
  ('AttrNumber*', 'attrs'),
  ('Oid*', 'opclasses'),
]

DistributionKey = [
  ('List*', 'dk_eclasses'),
  ('Oid', 'dk_opfamily'),
]