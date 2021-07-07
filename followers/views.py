from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from user.serializers import UserProfileSerializer
from user.models import User
from .models import Followers
from .serializers import FollowerSerializer

# Create your views here.


@api_view()
def get_following(request, pk):
    try:
        user = UserProfileSerializer(
            User.objects.filter(followed_by=pk, follower__is_accepted=True), many=True)
        return Response(user.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)


@api_view()
def get_follower(request, pk):
    try:
        user = UserProfileSerializer(User.objects.filter(
            follows=pk, following__is_accepted=True), many=True)
        return Response(user.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)


@api_view(['POST'])
def accept_follower(request, follower_id):
    try:
        follower = Followers.objects.get(follower=follower_id,
                                         following=request.user.id)
        follower.is_accepted = True
        follower.save()
        return Response({
            'status': "Follow request accepted"
        }, status=status.HTTP_201_CREATED)
    except Followers.DoesNotExist:
        return Response({
            'status': "Follow request does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    except:  # pylint: disable=bare-except
        return Response({
            'status': "Something Went Wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def reject_follow_request(request, follower_id):
    try:
        follower = Followers.objects.get(follower=follower_id,
                                         following=request.user.id)
        follower.delete()
        return Response({
            'status': "Follow request rejected"
        }, status=status.HTTP_200_OK)
    except Followers.DoesNotExist:
        return Response({
            'status': "Follow request does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    except:  # pylint: disable=bare-except
        return Response({
            'status': "Something Went Wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


class SendFollowRequest(CreateAPIView):
    serializer_class = FollowerSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'follower': request.user.id,
            'following': kwargs['pk']
        }
        target_user = User.objects.filter(pk=kwargs['pk'],
                                          followed_by=request.user.id)
        if target_user.exists():
            if target_user.filter(follower__is_accepted=False).exists():
                return Response(
                    {"error": "User has already sent the follow request to this user"},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "User already follows this user"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RemoveFollower(APIView):
    def delete(self, request, pk):
        try:
            follower = Followers.objects.get(
                follower=pk, following=request.user.id, is_accepted=True)
            follower.delete()
            user = Followers.objects.filter(
                following=pk, follower=request.user.id, is_accepted=True)
            if user.exists():
                user[0].delete()
        except Followers.DoesNotExist:
            return Response({"error": "Follower does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:  # pylint: disable=bare-except
            return Response({"error": "Something Went Wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Removed Successfully"},
                        status=status.HTTP_200_OK)


class UnFollow(APIView):
    def delete(self, request, pk):
        try:
            user = Followers.objects.get(
                following=pk, follower=request.user.id, is_accepted=True)
            user.delete()
        except Followers.DoesNotExist:
            return Response({"error": "User doesn't follow the "},
                            status=status.HTTP_400_BAD_REQUEST)
        except:  # pylint: disable=bare-except
            return Response({"error": "Something Went Wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)


class FollowRequests(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(follows=self.request.user.id,
                                   following__is_accepted=False)
