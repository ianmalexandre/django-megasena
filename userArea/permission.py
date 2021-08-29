from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import (
    JWTTokenUserAuthentication
)
class AdminOrItself(BasePermission, JWTTokenUserAuthentication):
    
    def has_permission(self, request, view, pk=None):
        _, tokenData = self.authenticate(request)
        userId = str(tokenData['user_id'])
        pk = view.kwargs.get('pk')
        print(f'pk = {pk}, userId = {userId}')
        if (pk == userId):
            return True

        return False