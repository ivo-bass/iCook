from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_regular_user():
    user = UserModel.objects.create_user(
        email='test@test.test',
        password='qwe987qwe987',
    )
    return user


def create_regular_active_user():
    user = create_regular_user()
    user.is_active = True
    return user
