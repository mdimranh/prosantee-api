from functools import wraps
from fastapi import HTTPException, Request
from typing import List, Union, Callable
from .registry import Permission
from inspect import signature, Parameter

def permissions(required_permissions: Union[Permission, List[Permission]]):
    """Decorator to check if the user has the required permissions.
    
    Args:
        required_permissions: Single permission or list of permissions required to access the endpoint
        
    Returns:
        Decorator function that checks permissions
        
    Raises:
        HTTPException: If user doesn't have required permissions
    """
    if isinstance(required_permissions, Permission):
        required_permissions = [required_permissions]

    def permission_dependency(request: Request):
        for perm in required_permissions:
            permission_object = perm.value
            if not permission_object(request).has_permission():
                raise HTTPException(
                    status_code=403, 
                    detail=f"User doesn't have required permission."
                )
        return True
    
    return permission_dependency