from django.urls import include, path
from rest_framework import routers
from . import views


# router = routers.DefaultRouter()
# router.register(r'file', views.PhotoViewSet)
# router.register(r'defaulter', views.DefaulterViewSet)
# router.register(r'fir', views.FirViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    # path('hell/',views.hell),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('handle_upload/', views.handle_upload, name='handle_upload')

]