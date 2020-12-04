from typing import Any

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

__all__ = ["empty_view"]


@api_view(["GET", "HEAD"])
@permission_classes([AllowAny])
def empty_view(request: Request, *args: Any, **kwargs: Any) -> Response:
    return Response(status=HTTP_204_NO_CONTENT)
