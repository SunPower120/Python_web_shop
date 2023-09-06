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

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
