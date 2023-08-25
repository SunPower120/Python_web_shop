
from rest_access_policy import AccessPolicy


class StaffAccessPolicy(AccessPolicy):
    statements = [
    {
        "action": ["list", "retrieve", "create", "update", "partial_update", "delete"],
        "principal": "user",
        "effect": "allow",
        "condition": "is_staff"
    }
]
    def is_staff(self, request, view, action) -> bool:
         return request.user.is_staff
