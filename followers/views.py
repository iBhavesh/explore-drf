from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Followers
from .serializers import FollowerSerializer
from user import models, serializers

# Create your views here.


@api_view()
@authentication_classes([])
@permission_classes([])
def get_followers(request, pk):
    # user = serializers.UserSerializer(models.User.objects.get(pk=pk))
    # return Response(user.data, status=HTTP_200_OK)

    followers = FollowerSerializer(
        Followers.objects.filter(follower=pk), many=True)
    return Response(followers.data, status=HTTP_200_OK)
