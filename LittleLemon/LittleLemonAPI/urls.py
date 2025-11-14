from django.urls import path
from . import views

urlpatterns = [
    #path('menu_items/',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu_items/<int:pk>/', views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    path('category/', views.CategoriesView.as_view()),
    path('menu_items/', views.MenuItemsView.as_view()),
]