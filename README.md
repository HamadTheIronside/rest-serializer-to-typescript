# Rest Serializer to TypeScript

It's an app to convert a serializer to a typescript interface

## How to install?

    pip install rest-serializer-to-typescript

## How to use it?

1. Add `rest_serializer_to_typescript` to INSTALLED_APPS
2. Add the following data to your `settings.py` file

```python
REST_SERIALIZERS_TO_TYPESCRIPT = {
    "SERIALIZERS": {
        "your_serializer_1_path": "output_1_address",
        "your_serializer_2_path": "output_2_address",
    }
}
```

For example:

```python
REST_SERIALIZERS_TO_TYPESCRIPT = {
    "SERIALIZERS": {
        "myapp.serializers": "types/myapp_types.ts",
        "custom_app.serializers": "types/custom_app_types.ts",
    }
}
```
