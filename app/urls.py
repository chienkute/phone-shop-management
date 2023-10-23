from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search.html', views.search, name='search'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('category.html', views.category, name='category'),
    path('detail/<slug:id>/', views.detail, name='detail'),
    path('place-order/',views.place_order,name='place-order'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('history/',views.history,name='history'),

]
