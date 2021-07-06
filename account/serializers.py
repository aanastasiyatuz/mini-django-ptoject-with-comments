from rest_framework import serializers
from .models import MyUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        # модель, которую нужно сериализовать (перевести в json формат)
        model = MyUser
        # поля, которые нужно сериализовать
        fields = ('id','email', 'username','password', 'phone')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    # проверка на уникальность телефона
    def validate_phone(self, phone):
        if MyUser.objects.filter(phone=phone).exists():
            # ошибка для фронта
            raise serializers.ValidationError('user with same phone exists!')
        return phone

    # проверка на уникальность email
    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            # ошибка для фронта
            raise serializers.ValidationError('user with same email exists!')
        return email
    
    # в настройках есть уже встроенная проверка, но я чуть добавила
    def validate_password(self, password):
        if len(password)<8:
            raise serializers.ValidationError('password should not consist less than 8 symbols')
        if not password.isalnum():
            raise serializers.ValidationError('Password should consist only alpha and num')
        return password

    # перед отправкой в бд
    def create(self, validated_data):
        # мы обращаемся к модели юзера, менеджеру и полю создания обычного юзера
        user = MyUser.objects.create_user(
            # проверяем на валидность данные
            email = validated_data.get('email'),
            username = validated_data.get('username'), 
            password = validated_data.get('password'),
            phone = validated_data.get('phone'))
        return user

# просто сериализация модели юзера
class UserSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'
