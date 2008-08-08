
__author__    = "MIT ESP"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "GPL v.2"
__copyright__ = """
This file is part of the ESP Web Site
Copyright (c) 2007 MIT ESP

The ESP Web Site is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Contact Us:
ESP Web Group
MIT Educational Studies Program,
84 Massachusetts Ave W20-467, Cambridge, MA 02139
Phone: 617-253-4882
Email: web@esp.mit.edu
"""

from esp.membership.models import AlumniInfo, AlumniContact, AlumniRSVP, AlumniMessage
from esp.users.models import User, ESPUser, ContactInfo
from esp.datatree.models import DataTree
from esp.db.forms import AjaxForeignKeyNewformField
from esp.utils.forms import CaptchaForm, CaptchaField, new_callback, grouped_as_table, add_fields_to_class, save_instance
from esp.membership.models import rsvp_choices, guest_choices
from django import forms

#   Modify the CharField class to support our formatting features.
add_fields_to_class(forms.CharField, {'is_long': False, 'line_group': 0})


class AlumniRSVPForm(forms.form_for_model(AlumniRSVP, formfield_callback=new_callback())):
    
    def __init__(self, *args, **kwargs):
        
        self.base_fields['name'].line_group = 1
        self.base_fields['num_guests'] = \
                forms.ChoiceField(choices = guest_choices,
                    label = AlumniRSVP._meta.get_field('num_guests').verbose_name)
        
        self.base_fields['num_guests'].line_group = 2
        self.base_fields['comments'].line_group = 3
        
        self.base_fields['attending'] = \
                forms.ChoiceField(choices = rsvp_choices,
                    label = AlumniRSVP._meta.get_field('attending').verbose_name)
                    
        self.base_fields['attending'].line_group = 2
        
        super(AlumniRSVPForm, self).__init__(*args, **kwargs)

    # use field grouping
    as_table = grouped_as_table

class ContactInfoForm(forms.form_for_model(ContactInfo, formfield_callback=new_callback(exclude=['phone_cell', 'phone_even', 'phone_day', 'user', 'address_postal', 'undeliverable']))):
    """
    This represents a standard pretty contact info form that can be used in a multitude of places.
    """
    
    def __init__(self, *args, **kwargs):
        self.base_fields['first_name'].widget = forms.TextInput(attrs={'size': 30})
        self.base_fields['last_name'].widget = forms.TextInput(attrs={'size': 30})
        self.base_fields['address_street'].widget = forms.TextInput(attrs={'size': 60})
        self.base_fields['address_city'].line_group = 1
        self.base_fields['address_state'].line_group = 1
        self.base_fields['address_zip'].line_group = 1
        self.base_fields['alt_user'] = AjaxForeignKeyNewformField(required=False, key_type=User, field_name='alt_user', help_text='If you already have an ESP user account, start typing your last name and select it here', label='ESP Web Site Account')
        self.base_fields['alt_user'].line_group = -1
        
        super(ContactInfoForm, self).__init__(*args, **kwargs)
        
        #   Make all fields non-required for alumni.
        for key in self.base_fields:
            self.base_fields[key].required = False

    def load_user(self):
        if self.clean_data.has_key('alt_user'):
            try:
                u = User.objects.get(id=self.clean_data['alt_user'])
                return ESPUser(u).getLastProfile().contact_user
            except:
                pass
        
        new_contact = ContactInfo()
        return save_instance(self, new_contact)

    # use field grouping
    as_table = grouped_as_table

class AlumniLookupForm(forms.Form):
    """
    This is a form to use if you're trying to find an ESP alumnus or alumna.
    """
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    start_year = forms.IntegerField(min_value=1950, max_value=2020, required=False)
    end_year = forms.IntegerField(min_value=1950, max_value=2020, required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['first_name'].line_group = 1
        self.base_fields['last_name'].line_group = 1
        self.base_fields['start_year'].line_group = 2
        self.base_fields['end_year'].line_group = 2        
        super(AlumniLookupForm, self).__init__(*args, **kwargs)

    as_table = grouped_as_table

class AlumniInfoForm(CaptchaForm, forms.form_for_model(AlumniInfo, formfield_callback=new_callback(exclude=['contactinfo']))):
    """
    This is an alumni contact form which is used to get information from alumni of ESP.
    """
    def __init__(self, *args, **kwargs):
        self.base_fields['involvement'].widget = forms.Textarea(attrs={'rows': 8, 'cols': 40})
        self.base_fields['start_year'].line_group = -1
        self.base_fields['end_year'].line_group = -1
        super(AlumniInfoForm, self).__init__(*args, **kwargs)

    # use field grouping
    as_table = grouped_as_table

anchor_choices = (  (DataTree.get_by_uri('Q/Programs/HSSP').id, 'HSSP'),
                    (DataTree.get_by_uri('Q/Programs/Splash').id, 'Splash'),
                    (DataTree.get_by_uri('Q/Programs/SATPrep').id, 'SAT Prep'),
                    (DataTree.get_by_uri('Q/Programs/Junction').id, 'Junction'),
                    (DataTree.get_by_uri('Q/Programs').id, 'Other program'),
                    (None, 'Other'))

class AlumniContactForm(CaptchaForm, forms.form_for_model(AlumniContact, formfield_callback=new_callback(exclude=['timestamp']))):
    """
    This is a form which allows alumni to submit a story, question or event relating to them.
    """
    def __init__(self, *args, **kwargs):
        self.base_fields['anchor'] = forms.ChoiceField(choices=anchor_choices, help_text='What program (if any) would you like to associate this posting with?', initial=None)
        self.base_fields['participants'] = AjaxForeignKeyNewformField(key_type=AlumniInfo, field_name='participants', help_text='Which ESP alumni would you like to associate with this posting?', label='Participants')
        super(AlumniContactForm, self).__init__(*args, **kwargs)

    # use field grouping
    as_table = grouped_as_table

    def load_data(self):
        #   Can't remove people... yet
        new_contact = AlumniContact()
        save_instance(self, new_contact, commit=False)
        new_contact.anchor_id = int(self.clean_data['anchor'])
        new_contact.save()
        if self.clean_data['participants']:
            new_contact.participants.add(self.clean_data['participants'])
        return new_contact

class AlumniMessageForm(CaptchaForm, forms.form_for_model(AlumniMessage, formfield_callback=new_callback(exclude=['seq','thread']))):
    
    def __init__(self, thread=None, *args, **kwargs):
        #   define some stuff so that save_instance does everything to save the message
        if thread:
            self.base_fields['seq'] = forms.IntegerField(initial=thread.max_seq()+1, widget=forms.HiddenInput)
            self.base_fields['thread'] = forms.IntegerField(initial=thread.id, widget=forms.HiddenInput)
        self.base_fields['poster'] = forms.CharField(widget=forms.TextInput(attrs={'size': 30}), help_text='Who are you?')
        self.base_fields['content'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 40}), label='Message')        
        super(AlumniMessageForm, self).__init__(*args, **kwargs)

