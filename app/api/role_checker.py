from fastapi.responses import JSONResponse
from fastapi import  Request, Depends


class RoleChecker:
  def __init__(self, allowed_roles):
    self.allowed_roles = allowed_roles

  def __call__(self, request: Request):
    if request.state.role in self.allowed_roles:
      return True
    raise JSONResponse(
        status_code=401, 
        content="Invalid roly type")