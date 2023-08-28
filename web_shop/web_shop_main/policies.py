
from rest_access_policy import AccessPolicy
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class StaffAccessPolicy(AccessPolicy):
    logger.info("Checking if staff 1")
    statements = [
    {
        "action": ["list", "retrieve", "create", "update", "partial_update", "delete"],
        "principal": "user",
        "effect": "allow",
        "condition": "is_staff"
    }
]
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
     
    
