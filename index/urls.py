from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', MainView.as_view(), name='index'),
	path('hag-more-info', HAGMoreInfoView.as_view(), name='hag_more_info'),
	path('votenow/', VoteNowView.as_view(), name='votenow'),
	path('vote/', VoteView.as_view(), name='vote'),
	path('about/', AboutView.as_view(), name='about'),
	path('theboard/', TheBoardView.as_view(), name='theboard'),
	path('theteam/', TheTeamView.as_view(), name='theteam'),
 	path('sponsorships/', SponsorshipsView.as_view(), name='sponsorships'),
	path('events/', EventsView.as_view(), name='events'),
	path('nominations/', NominationsView.as_view(), name='nominations'),
	path('nominate/', NominateView.as_view(), name='nominate'),
	# path('nominees-list/', NomineesListView.as_view(), name='nominees_list'),
	path('nomination-tips/', NominationTipsView.as_view(), name='nomination_tips'),
	path('nomination-rules/', NominationRulesView.as_view(), name='nomination_rules'),
	path('nomination-guidelines/', NominationGuidelinesView.as_view(), name='nomination_guidelines'),
	path('awards-process/', AwardsProcessView.as_view(), name='awards_process'),
	path('awards/', AwardsView.as_view(), name='awards'),
	# path('blog/', BlogView.as_view(), name='blog'),
	path('gallery/', GalleryView.as_view(), name='gallery'),
	path('contacts/', ContactsView.as_view(), name='contacts'),

	path('emailsubscription/', EmailSubscriptionView.as_view(), name='emailsubscription'),
	path('emailsubscription/thankyou', EmailSubscriptionThankYouView.as_view(), name='emailsubscription_thankyou'),
	path('emailunsubscription/thankyou', EmailUnSubscriptionThankYouView.as_view(), name='emailunsubscription_thankyou'),
	
	
	path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
 	path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
]