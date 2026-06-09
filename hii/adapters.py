from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        print("=== PRE SOCIAL LOGIN ===")
        print("USER:", sociallogin.user)
        print("EMAIL:", sociallogin.user.email)

    def save_user(self, request, sociallogin, form=None):
        print("=== SAVE USER START ===")
        print("SOCIAL USER:", sociallogin.user)
        print("EMAIL:", sociallogin.user.email)

        user = super().save_user(request, sociallogin, form=form)

        print("=== SAVE USER SUCCESS ===")
        print("CREATED USER:", user)

        return user