from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from notifications.models import Notifications
from notifications.serializers import NotificationSerializer


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notifications.objects.filter(owner=self.request.user.id)
        return queryset


class NotificationRead(APIView):
    def put(self, request, pk):
        try:
            notification = Notifications.objects.get(id=pk)
            notification.read = True
            notification.save()
            return Response("Modified", status=HTTP_200_OK)
        except Notifications.DoesNotExist:
            return Response("Notification not found", status=HTTP_400_BAD_REQUEST)
        except:  # pylint: disable=bare-except
            return Response("Something went wrong", status=HTTP_400_BAD_REQUEST)
