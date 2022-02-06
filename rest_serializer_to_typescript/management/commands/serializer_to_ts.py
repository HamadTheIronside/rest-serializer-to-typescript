import importlib
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand
from rest_framework.serializers import BaseSerializer, SerializerMetaclass

from rest_serializer_to_typescript import Transpiler

DEFAULT_SETTINGS = {
    "META_DATA": "rest_framework.metadata.SimpleMetadata",
    "SERIALIZERS": {}
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        final_settings = {
            **DEFAULT_SETTINGS,
            **getattr(settings, "REST_SERIALIZERS_TO_TYPESCRIPT", {})
        }

        target_serializers: dict[str, str] = final_settings.get("SERIALIZERS")
        if not target_serializers:
            return

        for serializer_module, export_target in target_serializers.items():
            print(f"Exporting {serializer_module} to {export_target}: Started")

            target_path = export_target.split("/")
            path_without_file = target_path[:-1]

            Path("/".join(path_without_file)).mkdir(parents=True, exist_ok=True)

            modules = importlib.import_module(serializer_module)

            serializers = list(
                filter(
                    lambda serializer_class: issubclass(serializer_class, BaseSerializer),
                    filter(
                        lambda unknown: type(unknown) == SerializerMetaclass,
                        map(
                            lambda attr: getattr(modules, attr),
                            dir(modules)
                        )
                    )
                )
            )

            typescript = ""
            for serializer in serializers:
                typescript += f"{Transpiler(serializer()).generate_ts()}\n\n"

            with open(export_target, "w") as file:
                file.write(typescript)

            print(f"Exporting {serializer_module} to {export_target}: Finished")
