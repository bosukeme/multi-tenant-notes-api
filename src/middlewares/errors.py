from typing import Any, Callable
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class OrganizationNotFound(Exception):
    """Raised when an organization with the specified ID does not exist."""


class OrganizationAlreadyExists(Exception):
    """Raised when attempting to create an organization that already exists."""


class UserAlreadyExists(Exception):
    """Raised when attempting to create a user that already
    exists in the organization."""


class NoteNotFound(Exception):
    """Raised when a note with the specified ID cannot be found."""


class UnauthorizedAccess(Exception):
    """Raised when a user attempts to access a resource they are
    not authorized to access."""


class ForbiddenAction(Exception):
    """Raised when a user attempts an action they do not have
    permission for."""


class OrganizationOrUserNotFound(Exception):
    """Raised when either the organization or the user does not exist."""


class MissingHeaders(Exception):
    """Raised when required request headers (e.g., X-Org-ID or X-User-ID)
    are missing."""


class UserDoesNotBelongToOrganization(Exception):
    """Raised when a user does not belong to the organization
    they are trying to access."""


class InvalidRoleAccess(Exception):
    """Raised when a user with an invalid role tries to perform an action."""


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    """
    Factory function to create a FastAPI exception handler for a
    specific status code and response content.

    Args:
        status_code (int): HTTP status code to return.
        initial_detail (Any): JSON-serializable object to return as
        response content.

    Returns:
        Callable[[Request, Exception], JSONResponse]: A FastAPI exception
        handler function.
    """

    async def exception_handler(request: Request, exc: Exception):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def set_up_error_handlers(app: FastAPI):
    app.add_exception_handler(
        OrganizationNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Organization not found",
                            "error_code": "org_not_found"},
        ),
    )

    app.add_exception_handler(
        OrganizationAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "Organization already exists",
                "error_code": "org_exists"},
        ),
    )

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": ("User with email already exists in this"
                            "organization"),
                "error_code": "user_exists"},
        ),
    )

    app.add_exception_handler(
        NoteNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Note not found",
                            "error_code": "note_not_found"},
        ),
    )

    app.add_exception_handler(
        UnauthorizedAccess,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={"message": "Unauthorized access",
                            "error_code": "unauthorized"},
        ),
    )

    app.add_exception_handler(
        ForbiddenAction,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={"message": "Forbidden action",
                            "error_code": "forbidden"},
        ),
    )

    app.add_exception_handler(
        OrganizationOrUserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Organization or user not found",
                            "error_code": "org_or_user_not_found"},
        ),
    )

    app.add_exception_handler(
        MissingHeaders,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Missing required X-Org-ID and X-User-ID  headers",
                "error_code": "missing_headers"},
        ),
    )

    app.add_exception_handler(
        UserDoesNotBelongToOrganization,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User does not belong to this organization",
                "error_code": "invalid_org"},
        ),
    )

    app.add_exception_handler(
        InvalidRoleAccess,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Invalid role for this action",
                "error_code": "invalid_role"},
        ),
    )
