from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        if extra_data:
            name = extra_data.get('name') or extra_data.get('given_name')
            if name:
                user_field(user, 'full_name', name)
            avatar = extra_data.get('picture')
            if avatar:
                user_field(user, 'avatar', avatar)
        return user
