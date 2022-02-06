from typing import Union

from rest_framework.serializers import ListSerializer

from rest_serializer_to_typescript import Transpiler
from .type_hinting_mapping import type_hinting_mapping

INDENT = 4


class SerializerMetadataTypeGenerator:
    keep_value_fields = ["type", "field_name"]

    def __init__(self, serializer, metadata, indent=1):
        self.indent = indent
        self.metadata = metadata
        self.serializer = serializer

    def generate_fields_types(self, name, data):
        fields = []

        for field_name, value in data.items():
            if field_name in self.keep_value_fields:
                ts_value = f'"{value}"'
            else:
                ts_value = type_hinting_mapping.get(type(value).__name__, "unknown")

                if type_hinting_mapping.get(type(value).__name__) is None:
                    print(f"NOTE: {type(value).__name__} is not registered in type_hinting_mapping")

            if field_name == "child":
                sub_serializer = self.serializer.fields[name]

                ts_value = SerializerMetadataTypeGenerator(
                    serializer=self.serializer.fields[name].child,
                    metadata=self.metadata
                ).get_namespace_name()

                if isinstance(sub_serializer, ListSerializer) and sub_serializer.many:
                    ts_value += "[]"

            fields.append(f"{field_name}: {ts_value};")

        return fields

    def generate_field_interface(self, name, data: dict[str, Union[bool, str]]):
        joined_fields = f"\n{' ' * (INDENT * (1 + self.indent))}".join(self.generate_fields_types(name, data))

        pre = ""
        if "child" in data:
            sub_serializer = self.serializer.fields[name].child

            pre = SerializerMetadataTypeGenerator(
                serializer=sub_serializer,
                metadata=self.metadata,
                indent=self.indent + 1
            ).generate_schema()
            pre += f"\n\n{' ' * (INDENT * self.indent)}"

        return f"""{pre}export interface {name} {{
{' ' * (INDENT * (1 + self.indent))}{joined_fields}
{' ' * (INDENT * self.indent)}}}"""

    def generate_schema(self):
        if self.metadata is None:
            raise Exception("Please provide rest framework metadata class")

        fields = self.metadata.get_serializer_info(self.serializer)

        fields_interfaces = f"\n\n{' ' * (INDENT * self.indent)}".join([
            self.generate_field_interface(field_name, field_data)
            for field_name, field_data in
            fields.items()
        ])

        namespace = f"""export declare module {self.get_namespace_name()} {{
{' ' * (INDENT * self.indent)}{fields_interfaces}
{' ' * (INDENT * (self.indent - 1))}}}"""
        return namespace

    def get_namespace_name(self):
        serializer_name = Transpiler(self.serializer).get_serializer_name()
        return f"I{serializer_name}Schema"
