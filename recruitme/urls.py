from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path

from recruitme_app import views
from recruitme_app.views import RegistrationView, WorkerRegistrationView, LoginView, JobRegistrationView, \
    JobListView, JobDetail, SearchJobView, SearchCvView, SkillsRegistrationView, RequirementsRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', JobListView.as_view(), name='home'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('worker_profile/', WorkerRegistrationView.as_view(), name='worker_profile'),
    path('job_registration/', JobRegistrationView.as_view(), name='job_registration'),
    path('job_detail/<int:id>/requirements/', RequirementsRegistrationView.as_view(), name='requirements'),
    path('job_detail/<int:id>/requirements/<rname>/delete_requirement/', views.delete_requirement, name='delete_requirement'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('job_detail/<int:id>/', JobDetail.as_view(), name='job_detail'),
    path('job_detail/<int:id>/delete/', views.delete, name='delete'),
    path('application/<int:id>/', views.apply_view, name='application'),
    path('application/<int:id>/response/', views.response, name='response'),
    path('search_job/', SearchJobView.as_view(), name='search_job'),
    path('search_cv/', SearchCvView.as_view(), name='search_cv'),
    path('worker_profile/skills/', SkillsRegistrationView.as_view(), name='skills'),
    path('worker_profile/skills/<tagname>/delete_skill/', views.delete_skill, name='delete_skill'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
