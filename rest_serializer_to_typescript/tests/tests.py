from rest_framework import serializers

from rest_serializer_to_typescript import Transpiler


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False)
    age = serializers.IntegerField()
    birth_year = serializers.IntegerField(required=False)


class UsersSerializer(serializers.Serializer):
    users = UserSerializer(many=True)


def test_user_serializer():
    expected_result = """export interface IUserSerializer {
    first_name: string;
    last_name?: string;
    age: number;
    birth_year?: number;
}"""

    assert Transpiler(UserSerializer).generate_ts() == expected_result


def test_users_serializer():
    expected_result = """export interface IUsersSerializer__UserSerializer {
    first_name: string;
    last_name?: string;
    age: number;
    birth_year?: number;
}

export interface IUsersSerializer {
    users: IUsersSerializer__UserSerializer[];
}"""

    assert Transpiler(UsersSerializer).generate_ts() == expected_result


class FooSerializer(serializers.Serializer):
    some_field = serializers.ListField(child=serializers.IntegerField())
    another_field = serializers.CharField()
    null_field = serializers.CharField(allow_null=True)


class BarSerializer(serializers.Serializer):
    foo = FooSerializer()
    foos = FooSerializer(many=True)
    bar_field = serializers.CharField()


def test_get_ts():
    expected = """export interface IBarSerializer__FooSerializer {
    some_field: number[];
    another_field: string;
    null_field: string | null;
}

export interface IBarSerializer {
    foo: IBarSerializer__FooSerializer;
    foos: IBarSerializer__FooSerializer[];
    bar_field: string;
}"""

    assert Transpiler(BarSerializer).generate_ts() == expected


class CustomSerializer(serializers.Serializer):
    value_1 = serializers.SerializerMethodField()
    value_2 = serializers.SerializerMethodField()
    value_3 = serializers.SerializerMethodField()
    value_4 = serializers.SerializerMethodField()

    def get_value_2(self) -> str:
        ...

    def get_value_3(self) -> int:
        ...

    def get_value_4(self):
        ...


def test_serializer_method():
    expected = """export interface ICustomSerializer {
    value_1?: unknown;
    value_2?: string;
    value_3?: number;
    value_4?: unknown;
}"""

    assert Transpiler(CustomSerializer).generate_ts() ==expected
