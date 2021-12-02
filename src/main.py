from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ListSerializer

from .mapping import mappings
from .type_hinting_mapping import type_hinting_mapping


class Transpiler:
    mapping = mappings
    type_mapping = type_hinting_mapping

    def __init__(self, serializer, parents=None):
        if parents is None:
            parents = []

        self.serializer = serializer
        self.pre_append = ""
        self.post_append = ""
        self.parents = parents
        self._already_transpiled = []

    def generate_ts(self) -> str:
        fields = ";\n    ".join(self.get_fields_type())

        return f"""{self.pre_append}export interface I{self.get_serializer_name()} {{
    {fields};
}}{self.post_append}"""

    def get_fields_type(self) -> list[str]:
        types: list[str] = []

        for field_name, field_class in self.serializer._declared_fields.items():
            ts_type = self.get_field_type(field_name, field_class)
            types.append(ts_type)

        return types

    def get_general_serializer_type(self, field_name, field_class):
        transpiled = Transpiler(field_class, parents=[*self.parents, self])
        transpiled_name = transpiled.get_serializer_name()
        if transpiled_name not in self._already_transpiled:
            self.pre_append += f"{transpiled.generate_ts()}\n\n"
            self._already_transpiled.append(transpiled_name)

        return f"{field_name}{'' if field_class.required else '?'}: I{transpiled_name}"

    def get_list_serializer_type(self, field_name, field_class):
        return f"{self.get_field_type(field_name, field_class.child)}[]"

    def get_method_serializer_type(self, field_name, field_class: SerializerMethodField):
        if field_class.method_name:
            method_name = field_class.method_name
        else:
            method_name = "get_" + field_name

        ts_type = "unknown"
        try:
            method = getattr(self.serializer, method_name)
            if return_type := method.__annotations__.get("return"):
                ts_type = self.type_mapping.get(return_type.__name__, "unknown")
        except AttributeError:
            pass

        return f"{field_name}{'' if field_class.required else '?'}: {ts_type}"

    def get_field_type(self, field_name, field_class) -> str:
        if isinstance(field_class, ListSerializer) or isinstance(field_class, ListField):
            return self.get_list_serializer_type(field_name, field_class)

        if isinstance(field_class, SerializerMethodField):
            return self.get_method_serializer_type(field_name, field_class)

        for FieldClass, ts_type in mappings.items():
            if isinstance(field_class, FieldClass):
                allow_null = " | null" if field_class.allow_null else ""
                return f"{field_name}{'' if field_class.required else '?'}: {ts_type}{allow_null}"

        return f"{self.get_general_serializer_type(field_name, field_class)}"

    def get_serializer_name(self):
        parents_names = "__".join(map(lambda transpiler: transpiler.get_serializer_name(), self.parents))

        if hasattr(self.serializer, "__name__"):
            base_name = f"{self.serializer.__name__}"
        else:
            base_name = f"{self.serializer.__class__.__name__}"

        if parents_names:
            return f"{parents_names}__{base_name}"

        return base_name
