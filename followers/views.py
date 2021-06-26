from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from user.serializers import UserProfileSerializer
from user.models import User
from .serializers import FollowRequestSerializer
from .models import FollowRequest, Followers

# Create your views here.


@api_view()
@authentication_classes([])
@permission_classes([])
def get_following(request, pk):
    user = UserProfileSerializer(User.objects.get(pk=pk))
    return Response(user.data.get('follows'), status=status.HTTP_200_OK)


@api_view()
@authentication_classes([])
@permission_classes([])
def get_follower(request, pk):
    user = UserProfileSerializer(User.objects.get(pk=pk))
    return Response(user.data.get('followed_by'), status=status.HTTP_200_OK)


@api_view(['POST'])
def accept_follower(request, follower_id):
    try:
        follower = User.objects.get(pk=follower_id)
        follow_request = FollowRequest.objects.get(
            request_from=follower_id, request_to=request.user.id)
        user = User.objects.get(pk=request.user.id)
        follower.follows.add(user)
        follow_request.delete()
        return Response({
            'status': "Follow request accepted"
        }, status=status.HTTP_201_CREATED)
    except FollowRequest.DoesNotExist:
        return Response({
            'status': "No such follow request exists!"
        }, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({
            'status': "Follower does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    except:  # pylint: disable=bare-except
        return Response({
            'status': "Something Went Wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def reject_follow_request(request, follower_id):
    try:
        follow_request = FollowRequest.objects.get(
            request_from=follower_id, request_to=request.user.id)
        follow_request.delete()
        return Response({
            'status': "Follow request rejected"
        }, status=status.HTTP_201_CREATED)
    except FollowRequest.DoesNotExist:
        return Response({
            'status': "No such follow request exists!"
        }, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({
            'status': "Follower does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    except:  # pylint: disable=bare-except
        return Response({
            'status': "Something Went Wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


class SendFollowRequest(CreateAPIView):
    serializer_class = FollowRequestSerializer


class RemoveFollower(APIView):
    def delete(self, request, format=None):  # pylint: disable=redefined-builtin,unused-argument
        print(request.data)
        try:
            follower = Followers.objects.get(
                follower=request.data.get('follower_id'), following=request.user.id)
            follower.delete()
            user = Followers.objects.filter(
                following=request.data.get('follower_id'), follower=request.user.id)
            if user.exists():
                user[0].delete()
        except:  # pylint: disable=bare-except
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "successful"}, status=status.HTTP_202_ACCEPTED)


class UnFollow(APIView):
    def delete(self, request, format=None):  # pylint: disable=redefined-builtin,unused-argument
        print(request.data)
        try:
            user = Followers.objects.get(
                following=request.data.get('following_id'), follower=request.user.id)
            user.delete()
        except Followers.DoesNotExist:
            return Response({"error": "User doesn't follow the "}, status=status.HTTP_400_BAD_REQUEST)
        except:  # pylint: disable=bare-except
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Unfollowed"}, status=status.HTTP_202_ACCEPTED)
