from rest_framework.routers import DefaultRouter

from apps.crm.views import (
    AddressViewSet,
    ContactViewSet,
    DocumentViewSet,
    ObservationViewSet,
    RelationshipHistoryViewSet,
    TaskViewSet,
)

router = DefaultRouter()
router.register("contacts", ContactViewSet, basename="contact")
router.register("addresses", AddressViewSet, basename="address")
router.register("documents", DocumentViewSet, basename="document")
router.register("tasks", TaskViewSet, basename="task")
router.register("relationship-history", RelationshipHistoryViewSet, basename="relationship-history")
router.register("observations", ObservationViewSet, basename="observation")

urlpatterns = router.urls
