from django.conf import settings

settings.configure()

from rest_framework import serializers

from rest_serializer_to_typescript import SerializerMetadataTypeGenerator
from rest_serializer_to_typescript.metadata import APIMetadata


def test_serializer_schema_with_single_string_field():
    class MySerializer(serializers.Serializer):
        some_field = serializers.CharField()

    metadata = APIMetadata()

    expected = """export declare module IMySerializerSchema {
    export interface some_field {
        type: "string";
        required: boolean;
        read_only: boolean;
        label: string;
        initial: string;
        field_name: "some_field";
        write_only: boolean;
    }
}"""

    assert SerializerMetadataTypeGenerator(MySerializer(), metadata=metadata).generate_schema() == expected


def test_user_serializer():
    metadata = APIMetadata()

    class UserSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField(required=False)
        age = serializers.IntegerField()
        birth_year = serializers.IntegerField(required=False)

    expected_result = """export declare module IUserSerializerSchema {
    export interface first_name {
        type: "string";
        required: boolean;
        read_only: boolean;
        label: string;
        initial: string;
        field_name: "first_name";
        write_only: boolean;
    }

    export interface last_name {
        type: "string";
        required: boolean;
        read_only: boolean;
        label: string;
        initial: string;
        field_name: "last_name";
        write_only: boolean;
    }

    export interface age {
        type: "integer";
        required: boolean;
        read_only: boolean;
        label: string;
        initial: unknown;
        field_name: "age";
        write_only: boolean;
    }

    export interface birth_year {
        type: "integer";
        required: boolean;
        read_only: boolean;
        label: string;
        initial: unknown;
        field_name: "birth_year";
        write_only: boolean;
    }
}"""

    assert SerializerMetadataTypeGenerator(UserSerializer(), metadata=metadata).generate_schema() == expected_result


def test_users_serializer():
    metadata = APIMetadata()

    class UserSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField(required=False)
        age = serializers.IntegerField()
        birth_year = serializers.IntegerField(required=False)

    class UsersSerializer(serializers.Serializer):
        users = UserSerializer(many=True)

    expected_result = """export declare module IUsersSerializerSchema {
    export declare module IUserSerializerSchema {
        export interface first_name {
            type: "string";
            required: boolean;
            read_only: boolean;
            label: string;
            initial: string;
            field_name: "first_name";
            write_only: boolean;
        }

        export interface last_name {
            type: "string";
            required: boolean;
            read_only: boolean;
            label: string;
            initial: string;
            field_name: "last_name";
            write_only: boolean;
        }

        export interface age {
            type: "integer";
            required: boolean;
            read_only: boolean;
            label: string;
            initial: unknown;
            field_name: "age";
            write_only: boolean;
        }

        export interface birth_year {
            type: "integer";
            required: boolean;
            read_only: boolean;
            label: string;
            initial: unknown;
            field_name: "birth_year";
            write_only: boolean;
        }
    }

    export interface users {
        type: "field";
        required: boolean;
        read_only: boolean;
        label: string;
        child: IUserSerializerSchema[];
        initial: unknown;
        field_name: "users";
        write_only: boolean;
    }
}"""

    assert SerializerMetadataTypeGenerator(UsersSerializer(), metadata=metadata).generate_schema() == expected_result

#
# def test_get_ts():
#     class FooSerializer(serializers.Serializer):
#         some_field = serializers.ListField(child=serializers.IntegerField())
#         another_field = serializers.CharField()
#         null_field = serializers.CharField(allow_null=True)
#
#     class BarSerializer(serializers.Serializer):
#         foo = FooSerializer()
#         foos = FooSerializer(many=True)
#         bar_field = serializers.CharField()
#
#     expected = """export interface IBarSerializer__FooSerializer {
#     __is_modal: false;
#     some_field: number[];
#     another_field: string;
#     null_field: string | null;
# }
#
# export interface IBarSerializer {
#     __is_modal: false;
#     foo: IBarSerializer__FooSerializer;
#     foos: IBarSerializer__FooSerializer[];
#     bar_field: string;
# }"""
#
#     assert Transpiler(BarSerializer()).generate_ts() == expected
#
#
# def test_serializer_method():
#     class CustomSerializer(serializers.Serializer):
#         value_1 = serializers.SerializerMethodField()
#         value_2 = serializers.SerializerMethodField()
#         value_3 = serializers.SerializerMethodField()
#         value_4 = serializers.SerializerMethodField()
#
#         def get_value_2(self) -> str:
#             ...
#
#         def get_value_3(self) -> int:
#             ...
#
#         def get_value_4(self):
#             ...
#
#     expected = """export interface ICustomSerializer {
#     __is_modal: false;
#     value_1?: unknown;
#     value_2?: string;
#     value_3?: number;
#     value_4?: unknown;
# }"""
#
#     assert Transpiler(CustomSerializer()).generate_ts() == expected
