from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_regular_user():
    user = UserModel.objects.create_user(
        email='test@test.test',
    )
    user.set_password = 'qwe987qwe987'
    user.save()
    return user


def create_regular_active_user():
    user = create_regular_user()
    user.is_active = True
    user.save()
    return user
