from rest_framework import generics, status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer, 
    FriendRequestSerializer, 
    FriendRequestSerializerDisplay,
    RespondFriendRequestSerializer)
from . models import User, FriendRequestModel
from django.db.models import Q
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  # Define this serializer to match your needs
    pagination_class = UserSearchPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            if '@' in query:
                # Search by email
                return User.objects.filter(email=query)
            else:
                # Search by name
                return User.objects.filter(username__icontains=query)
        return User.objects.none()
    

class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequestModel.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def create(self, request, *args, **kwargs):
        from_user = request.user
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequestModel.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()

        if recent_requests_count >= 3:
            return Response({"detail": "You cannot send more than 3 friend requests within a minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return super().create(request, *args, **kwargs)


class RespondFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequestModel.objects.all()
    serializer_class = RespondFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class ListFriendsView(generics.ListAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get the IDs of friends based on accepted friend requests
        friends_ids = FriendRequestModel.objects.filter(status='accepted').filter(
            Q(from_user=user) | Q(to_user=user)
        ).values_list('from_user', 'to_user')

        # Flatten the list of IDs and remove duplicates
        friends_ids = set(sum(friends_ids, ()))
        print(friends_ids)
        # Exclude the current user from the list of friends
        friends_ids.discard(user.id)

        # Get the User objects for the list of friend IDs
        return User.objects.filter(id__in=friends_ids)

# class ListPendingFriendRequestsView(generics.ListAPIView):
#     serializer_class = FriendRequestSerializerDisplay
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return FriendRequestModel.objects.filter(to_user=user, status='pending')


class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializerDisplay
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequestModel.objects.filter(
            Q(to_user=user) | Q(from_user=user), 
            status='pending'
        )