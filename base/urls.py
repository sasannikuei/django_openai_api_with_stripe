from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    test_func,
    TableGenerator,
    UserProfileView,
    PaymentListView,
    CreatePaymentIntentView,
                    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('', test_func, name='test-func'),
    path('api/table/', TableGenerator.as_view(), name='generate-table'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("payment-list/", PaymentListView.as_view(), name="payment-list"),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    # path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('profile/update/', views.updateUserProfile, name="users-profile-update"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
