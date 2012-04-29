from django import forms
from django.forms.formsets import formset_factory

from djutils import constants
from djutils.templatetags.djutils_tags import (
    formset_empty_row, formset_add_row, formset_forms, formset_header_row,
    dynamic_formset, popular_tags, latest, alpha, call_manager, tumble,
    as_template, 
)
from djutils.test import TestCase
from djutils.tests.models import Note1, Note2, Note3


class TestForm(forms.Form):
    name = forms.CharField()
    choice = forms.ChoiceField(choices=(
        (1, 'One'),
        (2, 'Two'),
    ))
    invisible = forms.CharField(widget=forms.HiddenInput())


class DjangoUtilsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.FormSet = formset_factory(TestForm)
        self.formset = self.FormSet()
    
    def test_formset_empty_row(self):
        self.assertEqual(self.formset.prefix, 'form')
        
        rendered = formset_empty_row(self.formset)
        
        self.assertEqual(rendered.splitlines(), [
            '<tr class="empty-row form">',
            '  <td><input type="text" name="form-__prefix__-name" id="id_form-__prefix__-name" /></td><td><select name="form-__prefix__-choice" id="id_form-__prefix__-choice">',
            '<option value="1">One</option>',
            '<option value="2">Two</option>',
            '</select></td>',
            '  <td><a href="javascript:void(0)" class="form-delete-row">Remove</a></td>',
            '</tr>'
        ])
        
        rendered = formset_empty_row(self.formset, 'name')
        self.assertEqual(rendered.splitlines(), [
            '<tr class="empty-row form">',
            '  <td><input type="text" name="form-__prefix__-name" id="id_form-__prefix__-name" /></td>',
            '  <td><a href="javascript:void(0)" class="form-delete-row">Remove</a></td>',
            '</tr>'
        ])
    
    def test_formset_add_row(self):
        rendered = formset_add_row(self.formset)
        
        self.assertEqual(rendered.splitlines(), [
            '<tr id="form-add-row">',
            '  <td colspan="3"><a href="javascript:void(0)" class="form-add-row">Add row</a></td>',
            '</tr>'
        ])
    
    def test_formset_forms(self):
        rendered = formset_forms(self.formset)
        self.assertEqual(rendered.splitlines(), [
            '<tr class="dynamic-form form">',
            '    <td><input type="text" name="form-0-name" id="id_form-0-name" /></td><td><select name="form-0-choice" id="id_form-0-choice">',
            '<option value="1">One</option>',
            '<option value="2">Two</option>',
            '</select></td>',
            '    ',
            '  </tr>',
        ])
        
        rendered = formset_forms(self.formset, 'name')
        self.assertEqual(rendered.splitlines(), [
            '<tr class="dynamic-form form">',
            '    <td><input type="text" name="form-0-name" id="id_form-0-name" /></td>',
            '    ',
            '  </tr>',
        ])
    
    def test_formset_header_row(self):
        rendered = formset_header_row(self.formset)
        self.assertEqual(rendered.splitlines(), [
            '<thead><tr class="header-row form">',
            '  <th>Name</th><th>Choice</th>',
            '</tr></thead>'
        ])
        
        rendered = formset_header_row(self.formset, 'name')
        self.assertEqual(rendered.splitlines(), [
            '<thead><tr class="header-row form">',
            '  <th>Name</th>',
            '</tr></thead>'
        ])
    
    def test_dynamic_formset(self):
        rendered = dynamic_formset(self.formset)
        self.assertEqual(rendered.splitlines(), [
            '',
            '<thead><tr class="header-row form">',
            '  <th>Name</th><th>Choice</th>',
            '</tr></thead>',
            '',
            '<tr class="empty-row form">',
            '  <td><input type="text" name="form-__prefix__-name" id="id_form-__prefix__-name" /></td><td><select name="form-__prefix__-choice" id="id_form-__prefix__-choice">',
            '<option value="1">One</option>',
            '<option value="2">Two</option>',
            '</select></td>',
            '  <td><a href="javascript:void(0)" class="form-delete-row">Remove</a></td>',
            '</tr>',
            '',
            '<tr class="dynamic-form form">',
            '    <td><input type="text" name="form-0-name" id="id_form-0-name" /></td><td><select name="form-0-choice" id="id_form-0-choice">',
            '<option value="1">One</option>',
            '<option value="2">Two</option>',
            '</select></td>',
            '    ',
            '  </tr>',
            '<tr id="form-add-row">',
            '  <td colspan="3"><a href="javascript:void(0)" class="form-add-row">Add row</a></td>',
            '</tr>',
            ''
        ])
    
    def test_popular_tags(self):
        result = popular_tags('tests.simple')
        self.assertEqual(result, ['apple', 'orange'])

        result = popular_tags('tests.simple', 1)
        self.assertEqual(result, ['apple'])
    
    def create_notes(self):
        for i, Note in enumerate([Note1, Note2, Note3]):
            note_class = i + 1
            for j in range(5):
                Note.objects.create(status=constants.LIVE_STATUS, message='live%d-%d' % (note_class, j+1))
                Note.objects.create(status=constants.DRAFT_STATUS, message='draft%d-%d' % (note_class, j+1))
    
    def test_latest(self):
        self.create_notes()
        
        self.assertEqual([x.message for x in latest('tests.note2', 'pub_date')], [
            'live2-5', 'live2-4', 'live2-3', 'live2-2', 'live2-1', 
        ])
        
        alternate = Note3.objects.filter(status=constants.DRAFT_STATUS)
        self.assertEqual([x.message for x in latest(alternate, 'pub_date')], [
            'draft3-5', 'draft3-4', 'draft3-3', 'draft3-2', 'draft3-1', 
        ])
    
    def test_alpha(self):
        self.create_notes()
        
        self.assertEqual([x.message for x in alpha('tests.note2', 'message')], [
            'live2-1', 'live2-2', 'live2-3', 'live2-4', 'live2-5', 
        ])
        
        alternate = Note3.objects.filter(status=constants.DRAFT_STATUS)
        self.assertEqual([x.message for x in alpha(alternate, 'message')], [
            'draft3-1', 'draft3-2', 'draft3-3', 'draft3-4', 'draft3-5', 
        ])
    
    def test_call_manager(self):
        self.create_notes()
        
        self.assertEqual([x.message for x in call_manager('tests.note2', 'published')], [
            'live2-1', 'live2-2', 'live2-3', 'live2-4', 'live2-5', 
        ])
        
        alternate = Note3.objects.filter(status=constants.DRAFT_STATUS)
        self.assertEqual([x.message for x in call_manager(alternate, 'all')], [
            'draft3-1', 'draft3-2', 'draft3-3', 'draft3-4', 'draft3-5', 
        ])
    
    def test_tumble(self):
        self.create_notes()
        
        self.assertEqual([x.message for x in tumble('tests.note1:pub_date,tests.note3:pub_date', 3)], [
            'live3-5', 'live3-4', 'live3-3', 'live1-5', 'live1-4', 'live1-3'
        ])
    
    def test_as_template(self):
        note = Note1.objects.create(message='test')
        
        rendered = as_template(note, 'tests/test.template.html').strip()
        self.assertEqual(rendered, str(note.pk))
