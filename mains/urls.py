from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index,name="home"),
    path('askquestions/', views.askquestions,name="askquestions"),
    path('myquestions/', views.showmyquestions,name="myquestions"),
    path('admin/', views.index,name="home2"),
    path('askquestions2/', views.askquestions2,name="askquestions2"),
    path('myquestions2/', views.showmyquestions,name="myquestions2"),
    path('reviewmanager/<str:sid>', views.reviewmanager,name="reviewmanager"),
    path('reviewemployee/<str:sid>', views.reviewemployee,name="reviewemployee"),
    path('sharethoughts/', views.reviewmanager,name="sharethoughts"),
    path('solveissues/<str:sid>', views.solveissues,name="solveissues"),
    path('askquestions/addq/', views.addq, name="addquestion"),
    path('askquestions2/addq2/', views.addq2, name="addquestion2"),
    path('myquestions/romyquestions/<int:fid>', views.romyquestions,name="romyquestions"),
    path('myquestions2/romyquestions/<int:fid>', views.romyquestions,name="romyquestions2"),
    path('reviewemployee/rcreviewemployee/<int:fid>', views.rcreviewemployee,name="rcreviewemployee"),
    path('solveissues/repsolveissues/<int:fid>', views.repsolveissues,name="repsolveissues"),
    path('reviewemployee/rcreviewemployee/Admin_accept/<int:fid>', views.admin_accept,name="admin_accept"),
    path('reviewemployee/rcreviewemployee/Admin_reject/<int:fid>', views.admin_reject,name="admin_reject"),
    path('solveissues/repsolveissues/manageraccept/<int:fid>', views.manageraccept,name="manageraccept"),
    path('solveissues/repsolveissues/managercancel/<int:fid>', views.managercancel,name="managercancel"),
    path('reviewmanager/rcreviewemployee/<int:fid>', views.repsolveissues,name="rcreviewemployee"),
    path('reviewmanager/rcreviewemployee/publish/<int:fid>', views.publish,name="publish"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('admin/search/', views.search, name='search'),

]   