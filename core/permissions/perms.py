from fastapi import Request


class BasePermission:
    def __init__(self, request: Request) -> None:
        self.request = request
    
    def has_permission(self) -> bool:
        return True

class IsAdmin(BasePermission):
    def has_permission(self) -> bool:
        user = getattr(self.request.state, 'user', None)
        if not user:
            return False
        print("User ------------------> ", user)
        return user.is_admin
