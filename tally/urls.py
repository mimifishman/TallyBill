from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'), 
    path('password', views.password_update, name='password'), 
    path('bill_header_new', views.bill_header, name='bill_header'), 
    path('bill_header_update/<int:bill_id>', views.bill_header_update, name='bill_header_update'),  
    path('bill/<int:bill_id>', views.bill_view, name='bill'), 
    path('bill_view_json/<int:bill_id>', views.bill_view_json, name='bill_view_json'),  
    path('line_json/<int:bill_id>', views.line_json, name='line_json'), 
    path('edit_line_json/<int:line_id>', views.line_edit_json, name='line_edit_json'), 
    path('my_bills', views.my_bills, name='my_bills'), 
    path('bill_users_json/<int:bill_id>', views.bill_users_json, name='bill_users_json'),
    path('edit_user_json/<int:user_id>', views.user_edit_json, name='user_edit_json'),
    path('add_line_user/<int:line_id>', views.add_line_user_json, name='add_line_user_json'),
    path('bill_totals/<int:bill_id>', views.bill_totals, name='bill_totals'),
    # path('import/<int:bill_id>', views.import_bill, name='import'),  
    # path('UploadFile', views.UploadFile, name='UploadFile'),  
]  

