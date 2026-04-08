from rest_framework import viewsets


class CompanyScopedModelViewSet(viewsets.ModelViewSet):
    company_field = "company"

    def get_queryset(self):
        queryset = super().get_queryset()
        company = getattr(self.request, "company", None)
        if company is None:
            return queryset.none()
        return queryset.filter(**{self.company_field: company})

    def perform_create(self, serializer):
        serializer.save(**{self.company_field: self.request.company})
