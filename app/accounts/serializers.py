from rest_framework import serializers

from .models import Author, User


class AuthorRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)
    password_2 = serializers.CharField(max_length=20, write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        if not data['telegram_chat_id'].isdigit():
            raise serializers.ValidationError('В телеграм ID должны быть только цифры')

        if data['password'].isdigit():
            raise serializers.ValidationError('В пароле должны быть буквы')

        if data['password'].isalpha():
            raise serializers.ValidationError('В пароле должны быть цифры')

        if len(data['password']) < 8:
            raise serializers.ValidationError('Пароль слишком короткий')

        if data['password'] != data['password_2']:
            raise serializers.ValidationError('Пароли должны совпадать')
        return data

    def create(self, validated_data):
        try:
            user = User(username=validated_data['username'],
                        email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удалось создать пользователя. {e}')
        else:
            author = Author.objects.create(
                telegram_chat_id=validated_data['telegram_chat_id'],
                user=user,
            )
            return author

