from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about', view=views.about, name='about'),
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),
    # path for registration
    path(route='registration', view=views.registration_request, name='registration'),
    # path for login
    path(route='login/<str:page>', view=views.login_request, name='login'),
    # path for logout
    path(route='logout/<str:page>', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view

    # path for testing
    path(route='test/', view=views.testNLU, name='test-NLU'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
