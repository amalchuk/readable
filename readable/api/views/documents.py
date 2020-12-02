from rest_framework.generics import CreateAPIView

from readable.api.serializers.documents import DocumentCreateSerializer
from readable.models import Staff

__all__ = ["document_create_view"]


class DocumentCreateAPIView(CreateAPIView):
    serializer_class = DocumentCreateSerializer

    def perform_create(self, serializer: DocumentCreateSerializer) -> None:
        uploaded_by: Staff = self.request.user.staff
        serializer.save(uploaded_by=uploaded_by)


document_create_view = DocumentCreateAPIView.as_view()
