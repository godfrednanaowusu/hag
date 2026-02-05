from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [    
	path('superadmin/', login_required(AccountView.as_view()), name='superadmin'),
	path('superadmin/schemes', login_required(AccountSchemesView.as_view()), name='superadmin_schemes'),
	path('superadmin/schemes-excel', login_required(AccountSchemesExcelView.as_view()), name='superadmin_schemes_excel'),
	path('superadmin/categories', login_required(AccountCategoriesView.as_view()), name='superadmin_categories'),
	path('superadmin/categories-excel', login_required(AccountCategoriesExcelView.as_view()), name='superadmin_categories_excel'),
	path('superadmin/nominations', login_required(AccountNominationsView.as_view()), name='superadmin_nominations'),
	path('superadmin/nominations-excel', login_required(AccountNominationsExcelView.as_view()), name='superadmin_nominations_excel'),
	path('superadmin/votes', login_required(AccountVotesView.as_view()), name='superadmin_votes'),
	path('superadmin/votes-excel', login_required(AccountVotesExcelView.as_view()), name='superadmin_votes_excel'),
	path('superadmin/payments', login_required(AccountPaymentsView.as_view()), name='superadmin_payments'),
	path('superadmin/payments-excel', login_required(AccountPaymentsExcelView.as_view()), name='superadmin_payments_excel'),
	path('superadmin/messaging', login_required(AccountMessagingView.as_view()), name='superadmin_messaging'),
	path('superadmin/blog/', login_required(BlogView.as_view()), name='superadmin_blog'),   
    path('superadmin/blog-detail', login_required(BlogDetailView.as_view()), name='superadmin_blog_detail'), 
	path('superadmin/messaging/sms', login_required(AccountMessagingSMSView.as_view()), name='superadmin_messaging_sms'),
	path('superadmin/messaging/emails', login_required(AccountMessagingEmailsView.as_view()), name='superadmin_messaging_emails'),
	path('superadmin/messaging/settings', login_required(AccountMessagingSettingsView.as_view()), name='superadmin_messaging_settings'),
	path('superadmin/profile', login_required(AccountProfileView.as_view()), name='superadmin_profile'),
	
	# path('register/', RegisterView.as_view(), name='register'),
	# path('register_confirm/', RegisterConfirmView.as_view(), name='registerconfirm'),	
	path('adminlogin/', LoginView.as_view(), name='adminlogin'),
	# path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
	# path('resetpassword_confirm/', ResetPasswordConfirmView.as_view(), name='resetpasswordconfirm'),	
	# path('resetpassword_thanks/', TemplateView.as_view(template_name='resetpassword_thanks.html')),
    path('adminlogout/', LogoutView.as_view(), name='adminlogout'),
]
