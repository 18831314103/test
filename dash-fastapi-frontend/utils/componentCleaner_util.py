import math
from dash.development.base_component import Component

class ComponentCleaner:
    """
    清洗 Dash 组件树中的非法字段，确保其能被前端序列化。
    """

    @staticmethod
    def clean(component):
        return ComponentCleaner._clean_component(component)

    @staticmethod
    def _clean_component(component, path="root"):
        try:
            if isinstance(component, Component):
                cleaned_props = {}

                for prop_name in component._prop_names:
                    try:
                        prop_value = getattr(component, prop_name)
                        current_path = f"{path}.{component.__class__.__name__}.{prop_name}"

                        if isinstance(prop_value, float) and (math.isnan(prop_value) or math.isinf(prop_value)):
                            print(f"[清除] 非法 float 值: {current_path} = {prop_value}")
                            continue

                        elif isinstance(prop_value, (list, tuple, set)):
                            cleaned_list = []
                            for i, v in enumerate(prop_value):
                                if v is None:
                                    continue
                                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                                    print(f"[清除] 非法 float 数组值: {current_path}[{i}] = {v}")
                                    continue
                                cleaned_list.append(ComponentCleaner._clean_component(v, f"{current_path}[{i}]"))
                            prop_value = cleaned_list

                        elif isinstance(prop_value, dict):
                            new_dict = {}
                            for k, v in prop_value.items():
                                if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
                                    print(f"[清除] 非法 dict 值: {current_path}['{k}'] = {v}")
                                    continue
                                new_dict[k] = ComponentCleaner._clean_component(v, f"{current_path}['{k}']")
                            prop_value = new_dict

                        elif isinstance(prop_value, Component):
                            prop_value = ComponentCleaner._clean_component(prop_value, current_path)

                        cleaned_props[prop_name] = prop_value

                    except Exception as e:
                        # print(f"[跳过] 无法访问属性 {prop_name} at {path}: {e}")
                        continue

                return component.__class__(**cleaned_props)

            elif isinstance(component, (list, tuple, set)):
                return [
                    ComponentCleaner._clean_component(item, f"{path}[{i}]")
                    for i, item in enumerate(component)
                    if item is not None
                ]

            elif isinstance(component, dict):
                return {
                    k: ComponentCleaner._clean_component(v, f"{path}['{k}']")
                    for k, v in component.items()
                    if v is not None and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))
                }

            else:
                return component
        except Exception as e:
            print(f"[清理失败] 路径 {path} 上发生错误: {e}")
            return None
