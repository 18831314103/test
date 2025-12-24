/**
 * time: 2025-06-06
 * author: XJ
 * description: ids可以修改字段和table的关系
 */
interface keyForTableProps {
  OIM_EXPERIMENT_ACTION_TEMPLATE: string[];
  OIM_EXPERIMENT_PARA_TEMPLATE: string[];
  OIM_EXPERIMENT_PARA_RANGE: string[];
  OIM_EXPERIMENT_PARAVALUE_TEMPL: string[];
}

const keyForTable: keyForTableProps = {
  OIM_EXPERIMENT_ACTION_TEMPLATE: ['actionName', 'type'],
  OIM_EXPERIMENT_PARA_TEMPLATE: ['parameterName', 'optionalValues'],
  OIM_EXPERIMENT_PARA_RANGE: ['paraDesc'],
  OIM_EXPERIMENT_PARAVALUE_TEMPL: ['paraCode', 'paraDesc'],
};

export default keyForTable;
