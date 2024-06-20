from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, FriendRequestSerializer
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from .models import FriendRequest
from datetime import timedelta
from django.db import transaction
from rest_framework import viewsets

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


# class UserSearchAPIView(APIView):
class UserSearchViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({'error': 'Keyword query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email=keyword))

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSerializer(page, many=True)
        else:
            serializer = UserSerializer(users, many=True)

        return Response(serializer.data)
    

# Add the Urls
class FriendRequestView(APIView):

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        request_status = request.data.get('request_status', FriendRequest.RequestChoices.PENDING)

        if request_status not in FriendRequest.RequestChoices.values:
            return Response({'error': 'Invalid request status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            to_user = User.objects.get(username=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the users are not sending more than 3 requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count()
        
        if recent_requests_count >= 3:
            return Response({'error': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction to ensure atomicity
        with transaction.atomic():
            friend_request, created = FriendRequest.objects.get_or_create(
                from_user=from_user,
                to_user=to_user
            )
            if not created and friend_request.request_status == FriendRequest.RequestChoices.PENDING:
                FriendRequest.objects.filter(id=friend_request.id).update(request_status=request_status)
                import pdb;pdb.set_trace()
                return Response({'message': 'Friend request {}'.format(request_status)}, status=status.HTTP_200_OK)

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


# Add the Urls
class FriendRequestPendingList(APIView):
    def get(self, request):
        from_user = request.user
        friend_requests = FriendRequest.objects.filter(to_user__username=from_user.username, request_status=FriendRequest.RequestChoices.PENDING)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Add the Urls
class FriendsListView(APIView):
    def get(self, request):
        from_user = request.user
        friends = FriendRequest.objects.filter(from_user=from_user, request_status=FriendRequest.RequestChoices.ACCEPTED)
        serializer = FriendRequestSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


