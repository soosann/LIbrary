from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin,name='login'),
    path('signup/',views.signup, name ='signup'),
    path('category/',views.category,name='category'),
    path('books/',views.books,name='books'),
    path('logout/',views.mylogout,name='logout'),
    path('students/',views.students,name='students'),
    path('borrows/',views.borrow,name='borrows'),
    path('returns/',views.returning,name='returns'),

]