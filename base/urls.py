from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
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
    path('api/table/', TableGenerator.as_view(), name='generate-table'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("payment-list/", PaymentListView.as_view(), name="payment-list"),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
