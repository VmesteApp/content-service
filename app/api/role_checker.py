from fastapi import Request, HTTPException


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, request: Request):
        if request.state.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=401, detail="Invalid role type")
