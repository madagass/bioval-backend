from rest_framework import generics
from .models import Log
from .serializers import LogSerializer
from apps.users.permissions import IsAdminGlobal


class LogListView(generics.ListAPIView):
    serializer_class = LogSerializer
    permission_classes = [IsAdminGlobal]

    def get_queryset(self):
        qs = Log.objects.all()
        user_id = self.request.query_params.get("user_id")
        if user_id:
            qs = qs.filter(user__id=user_id)
        return qs


class LogDetailView(generics.RetrieveAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAdminGlobal]