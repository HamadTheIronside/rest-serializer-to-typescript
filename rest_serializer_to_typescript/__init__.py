from .main import Transpiler
from .schema_generator import SerializerMetadataTypeGenerator
from .mapping import mappings
from .type_hinting_mapping import type_hinting_mapping

default_app_config = "rest_serializer_to_typescript.apps.RestSerializerToTypescriptConfig"
