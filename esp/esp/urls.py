__author__    = "Individual contributors (see AUTHORS file)"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "AGPL v.3"
__copyright__ = """
This file is part of the ESP Web Site
Copyright (c) 2007 by the individual contributors
  (see AUTHORS file)

The ESP Web Site is free software; you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Contact information:
MIT Educational Studies Program
  84 Massachusetts Ave W20-467, Cambridge, MA 02139
  Phone: 617-253-4882
  Email: esp-webmasters@mit.edu
Learning Unlimited, Inc.
  527 Franklin St, Cambridge, MA 02139
  Phone: 617-379-0178
  Email: web-team@lists.learningu.org
"""
import os
from django.conf.urls.defaults import patterns, include, handler500, handler404
from django.contrib import admin
from esp.admin import admin_site, autodiscover
from django.conf import settings
from django.views.generic.base import RedirectView

from esp.section_data import section_redirect_keys, section_prefix_keys

autodiscover(admin_site)

# Override error pages
handler404 = 'esp.web.util.main.error404'
handler500 = 'esp.web.util.main.error500'

# Static media
urlpatterns = patterns('django.views.static',
                       (r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^admin/media/(?P<path>.*)$', 'serve', {'document_root': os.path.join(settings.PROJECT_ROOT, 'admin/media/')}),
                       )

# Admin stuff
urlpatterns += patterns('',
                        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                        (r'^admin/ajax_qsd/?', 'esp.qsd.views.ajax_qsd'),
                        (r'^admin/ajax_autocomplete/?', 'esp.db.views.ajax_autocomplete'),
                        (r'^admin/ajax_children/?', 'esp.datatree.views.ajax_children'),
                        (r'^admin/', include(admin_site.urls)),
                        (r'^accounts/login/$', 'esp.users.views.login_checked',),
                        #(r'^learn/Junction/2007_Spring/catalog/?$',RedirectView.as_view(url='/learn/Junction/2007_Summer/catalog/')),
                        (r'^(?P<subsection>(learn|teach|program|help|manage|onsite))/?$',RedirectView.as_view(url='/%(subsection)s/index.html')),
                        )
urlpatterns += patterns('',
                        (r'^admin', RedirectView.as_view(url='/admin/')),
                        )

#   Short term views
urlpatterns += patterns('',
                        (r'^', include('esp.shortterm.urls')),
                        )

# program stuff
urlpatterns += patterns('',
                        (r'^',  include('esp.program.urls')), 
                        )

urlpatterns += patterns('esp.web.views.bio',

                        # bios
                        (r'^(?P<tl>teach|learn)/teachers/(?P<last>[-A-Za-z0-9_ \.]+)/(?P<first>[-A-Za-z_ \.]+)(?P<usernum>[0-9]*)/bio\.html$', 'bio'),
                        (r'^(?P<tl>teach|learn)/teachers/(?P<username>[^/]+)/bio\.html$', 'bio'),
                        (r'^myesp/teacherbio/?$', 'bio_edit'),
                        (r'^(?P<tl>teach|learn)/teachers/(?P<last>[-A-Za-z0-9_ ]+)/(?P<first>[-A-Za-z_ ]+)(?P<usernum>[0-9]*)/bio\.edit\.html/?(.*)$', 'bio_edit'),
                        (r'^(?P<tl>teach|learn)/teachers/(?P<username>[^/]+)/bio\.edit\.html/?(.*)$', 'bio_edit'),
                        )

urlpatterns += patterns('',
                        (r'^myesp/', include('esp.users.urls'),)
                        )

urlpatterns += patterns('',
                        (r'^cache/', include('esp.cache.urls'),)
                        )

urlpatterns += patterns('esp.qsd.views',
                        (r'^(?P<subsection>(learn|teach|programs|manage|onsite))/(?P<url>.*)\.html$', 'qsd'),
                        (r'^(?P<url>.*)\.html$', 'qsd'),
                        )

#urlpatterns += patterns('',
#                        (r'^(?P<subsection>(learn|teach|programs|manage|onsite))/?$', RedirectView.as_view(url='/%(subsection)s/index.html')),
#                        )

# other apps
urlpatterns += patterns('',
#                        (r'^alumni/', include('esp.membership.alumni_urls')),
#                        (r'^membership/', include('esp.membership.urls')),
                        (r'^',  include('esp.miniblog.urls')),
                        (r'^',  include('esp.survey.urls')),
                        )

urlpatterns += patterns('esp.web.views.json',

     # JSON
                        (r'json/teachers/$', 'teacher_lookup'))

# QSD Media
# aseering 8/14/2007: This ought to be able to be written in a simpler way...
urlpatterns += patterns('esp.web.views.main',
                        (r'^$', 'home'),

    # Possibly overspecific, possibly too general.
                        (r'^(?P<subsection>(learn|teach|program|help))/(?P<url>.*)/qsdmedia/(?P<filename>[^/]+\.[^/]{1,4})$', 'redirect',
                         { 'section_redirect_keys': section_redirect_keys, 'renderer': 'esp.qsdmedia.views.qsdmedia', 'section_prefix_keys': section_prefix_keys }),
                        (r'^(?P<subsection>(learn|teach|program|help))/qsdmedia/(?P<filename>[^/]+\.[^/]{1,4})$', 'redirect',
                         { 'section_redirect_keys': section_redirect_keys, 'renderer': 'esp.qsdmedia.views.qsdmedia', 'section_prefix_keys': section_prefix_keys, 'url': ''}),
                        (r'^(?P<url>.*)/qsdmedia/(?P<filename>[^/]+\.[^/]{1,4})$', 'redirect',
                         { 'section_redirect_keys': section_redirect_keys, 'renderer': 'esp.qsdmedia.views.qsdmedia' }),
                        (r'^qsdmedia/(?P<filename>[^/]+\.[^/]{1,4})$', 'redirect',
                         { 'section_redirect_keys': section_redirect_keys, 'renderer': 'esp.qsdmedia.views.qsdmedia', 'url': '' }),

    # aseering - Is it worth consolidating these?  Two entries for the single "contact us! widget
    # Contact Us! pages
                        (r'^contact/contact/?$', 'contact'),
                        (r'^contact/contact/(?P<section>[^/]+)/?$', 'contact'),
#    (r'^contact/submit\.html$', 'contact_submit'),


    # Program stuff
    (r'^(onsite|manage|teach|learn|volunteer)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/classchangerequest/?$', 'classchangerequest'),
    (r'^(onsite|manage|teach|learn|volunteer|json)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/?$', 'program'),
    (r'^(onsite|manage|teach|learn|volunteer|json)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/?$', 'program'),

    #??? (axiak)
    #(r'^program/Template/$', 'esp.program.views.programTemplateEditor'),
    #(r'^program/(?P<program>[-A-Za-z0-9_ ]+)/(?P<session>[-A-Za-z0-9_ ]+)/Classes/Template/$', 'esp.program.views.classTemplateEditor'),

    # all the archives
                        (r'^archives/([-A-Za-z0-9_ ]+)/?$', 'archives'),
                        (r'^archives/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/?$', 'archives'),
                        (r'^archives/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/([-A-Za-z0-9_ ]+)/?$', 'archives'),
                        (r'^myesp/([-A-Za-z0-9_ ]+)/?$', 'myesp'),

    # DB-generated QSD pages: HTML or plaintext
    #                        (r'^(?P<url>.*)\.html$', 'redirect', { 'section_redirect_keys': section_redirect_keys , 'renderer': qsd} ),
                        )
    
    # Event-generation
    # Needs to get fixed (axiak)
    #(r'^events/create/$', 'esp.cal.views.createevent'),
    #(r'^events/edit/$', 'esp.cal.views.updateevent'),
    #(r'^events/edit/(?P<id>\d+)/$', 'esp.cal.views.updateevent'),

urlpatterns += patterns('',
                        (r'^(?P<subsection>onsite|manage|teach|learn|volunteer)/(?P<program>[-A-Za-z0-9_ ]+)/?$', RedirectView.as_view(url='/%(subsection)s/%(program)s/index.html')),)

urlpatterns += patterns('esp.web.views.navBar',
    # Update navbar
                        (r'^navbar/edit.scm', 'updateNavBar') 
                        )
    
urlpatterns += patterns('', 
                        (r'^dataviews/', include('esp.dataviews.urls')) 
                        )

urlpatterns +=patterns('esp.customforms.views',
                       (r'^customforms/$','landing'),
                       (r'^customforms/create/$','formBuilder'),
                       (r'^customforms/submit/$','onSubmit'),
                       (r'^customforms/modify/$','onModify'),
                       (r'^customforms/view/(?P<form_id>\d{1,6})/$','viewForm'),
                       (r'^customforms/success/(?P<form_id>\d{1,6})/$', 'success'),
                       (r'^customforms/responses/(?P<form_id>\d{1,6})/$', 'viewResponse'),
                       (r'^customforms/getData/$', 'getData'),
                       (r'^customforms/metadata/$', 'getRebuildData'),
                       (r'^customforms/getperms/$', 'getPerms'),
                       (r'^customforms/getlinks/$', 'get_links'),
                       (r'^customforms/builddata/$', 'formBuilderData'),
                       (r'^customforms/exceldata/(?P<form_id>\d{1,6})/$', 'getExcelData'),
                       )	

#Theme editor
urlpatterns += patterns('esp.theme_editor.views',
                        (r'^theme/?$', 'editor'),
                        (r'^theme/submit/?$', 'theme_submit'),
                        (r'^layout/?$', 'layout'),
                        )

