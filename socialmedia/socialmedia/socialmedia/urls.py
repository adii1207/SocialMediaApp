from django.urls import path, include
# from weatherReportApp.views import CustomTokenObtainPairView

medaiaAppUrls = include("media_app.urls")

urlpatterns = [
    # path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('media-app/', medaiaAppUrls),
]
