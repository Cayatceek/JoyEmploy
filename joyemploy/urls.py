from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('simple_pages.urls')), 
    path('employee/', include('employees.urls')),
    path('manage/',include('manage_panel.urls')),
    path('employee_detail/', include('employee_detail.urls')),
    path('news/', include('news.urls')), 
    path('taskboard/', include('taskboard.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
