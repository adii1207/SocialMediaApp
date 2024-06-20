from django.urls import path
from .views import SignupView, LoginView, UserSearchViewSet, FriendRequestView, FriendsListView, FriendRequestPendingList

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/search/', UserSearchViewSet.as_view({'get': 'list'}), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends'),
    path('pending-requests/', FriendRequestPendingList.as_view(), name='friends'),
]