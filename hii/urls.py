from django.urls import path
from hii import views

urlpatterns = [
    path("", views.index, name="hii"),
    path("shop/", views.shop, name="shop"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("product/<int:pk>/", views.product, name="product"),

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),

    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
]