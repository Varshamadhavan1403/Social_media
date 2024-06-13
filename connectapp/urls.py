from django.urls import path
from .views import (RegisterView, 
                    CustomTokenObtainPairView, 
                    UserSearchView, 
                    SendFriendRequestView, 
                    RespondFriendRequestView, 
                    ListFriendsView,
                    ListPendingFriendRequestsView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/<int:pk>/', RespondFriendRequestView.as_view(), name='respond_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),
]
