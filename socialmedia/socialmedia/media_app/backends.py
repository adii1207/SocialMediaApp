from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
            

class CaseInsensitiveEmailAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__iexact=username)  # case-insensitive email
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None