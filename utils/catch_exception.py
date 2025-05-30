from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .api_response_handler import APIResponse
from jose import JWTError
from fastapi import HTTPException


def catch_exception(view_func):
    @wraps(view_func)
    async def wrapper(*args, **kwargs):
        try:
            return await view_func(*args, **kwargs)
        except IntegrityError as e:
            return APIResponse.HTTP_409_CONFLICT(message=f"Integrity error: {str(e)}")
        except (NoResultFound,) as e:
            return APIResponse.HTTP_404_NOT_FOUND(message=f"Object not found: {str(e)}")
        except MultipleResultsFound as e:
            return APIResponse.HTTP_404_NOT_FOUND(message=f"Multiple objects found: {str(e)}")
        except JWTError as e:
            return APIResponse.HTTP_401_UNAUTHORIZED(message=f"Invalid token: {str(e)}")
        except ValueError as e:
            return APIResponse.HTTP_401_UNAUTHORIZED(message=f"Invalid token: {str(e)}")
        except HTTPException as e:
            return APIResponse.HTTP_401_UNAUTHORIZED(message=f"Invalid token: {str(e)}")
        except Exception as e:
            return APIResponse.HTTP_500_INTERNAL_SERVER_ERROR(message=f"Internal server error: {str(e)}")
    return wrapper
