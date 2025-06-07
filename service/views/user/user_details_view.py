from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.models import Users
from service.serializers import UserDetailSerializer
from service.utils import ResponseHandler, get_token_data


class UserDetailsView(APIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    
    def get(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get('user_id')

        try:
            user = self.queryset.get(id=user_id)
        except Users.DoesNotExist:
            return ResponseHandler(
                success=False,
                status=status.HTTP_404_NOT_FOUND,
                message=ExceptionMessages.USER_NOT_FOUND
            )
        
        serializer = self.serializer_class(user)
        return ResponseHandler(
            success=True,
            status=status.HTTP_200_OK,
            message=ResponseMessages.USER_DETAILS_FETCHED,
            data=serializer.data
        )
