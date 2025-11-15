from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #path('menu_items/',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu_items/<int:pk>/', views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('category/', views.CategoriesView.as_view()),
    path('menu_items/', views.MenuItemsView.as_view()),
    path('secret/',views.secret),
    path('api_token_auth/', obtain_auth_token),
    path('manager_view/', views.manager_view),
    #path('roles/', views.roles),
    path('throttle_check/', views.throttle_check),
    path('throttle_check_auth/', views.throttle_check_auth),
    #path('me/', views.me),
    path('manager_view/', views.manager_view),
    path('groups/manager/users/', views.managers),
    path('ratings/', views.RatingsView.as_view()),

]