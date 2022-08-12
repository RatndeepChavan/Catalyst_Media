from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', views.hm, name='hm'),
    path('signup/', views.sg, name='sg'),
    path('payment/', views.payment, name='payment'),
    path('out/', views.out, name='out'),
    path('enable/', views.enable, name='enable'),
    path('disable/', views.disable, name='disable'),
    path('add/', views.add, name='add'),
    path('remove/', views.remove, name='remove'),

    # API urls
    path('api/<v>/', views.api),
    # path('apienb/', views.apienb, name='apienb'),
    # path('apidis/', views.apidis, name='apidis'),
    # path('apibal/', views.apibal, name='apibal'),
    # path('apiadd/', views.apiadd, name='apiadd'),
    # path('apirmv/', views.apirmv, name='apirmv'),

    #jwt urls to autometically generate the tokens
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
