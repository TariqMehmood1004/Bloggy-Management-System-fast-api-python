from functools import wraps
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from fastapi import Request, status
from .api_response_handler import APIResponse

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
        except Exception as e:
            return APIResponse.HTTP_500_INTERNAL_SERVER_ERROR(message=f"Internal server error: {str(e)}")
    return wrapper
