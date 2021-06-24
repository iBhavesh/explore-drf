from followers.serializers import FollowRequestSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from user.serializers import UserSerializer
from user.models import User
from followers.models import FollowRequest

# Create your views here.


@api_view()
@authentication_classes([])
@permission_classes([])
def get_followers(request, pk):
    user = UserSerializer(User.objects.get(pk=pk))
    return Response(user.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def accept_follower(request, pk):
    try:
        print(pk)
        print(request.user.id)
        follower = User.objects.get(pk=pk)
        follow_request = FollowRequest.objects.get(
            request_from=pk, request_to=request.user.id)
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
            'status': "User does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)
    except:  # pylint: disable=bare-except
        return Response({
            'status': "Something Went Wrong"
        }, status=status.HTTP_400_BAD_REQUEST)


class SendFollowRequest(CreateAPIView):
    serializer_class = FollowRequestSerializer
