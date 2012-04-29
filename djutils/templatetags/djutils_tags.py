import os
import re
import urllib

from django import template
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage
from django.db.models.loading import get_model, get_models
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils.hashcompat import md5_constructor
from django.utils.safestring import mark_safe

from djutils.constants import SYNTAX_HIGHLIGHT_RE
from djutils.decorators import memoize
from djutils.db.managers import PublishedManager
from djutils.utils.highlighter import highlight
from djutils.utils.images import resize as img_resize


register = template.Library()

def get_fields_for_formset(formset, fields):
    """
    Utility method to grab fields that should be displayed for a FormSet
    """
    if fields is None:
        return formset.empty_form.visible_fields()
    else:
        return [
            f for f in formset.empty_form.visible_fields() \
                if f.name in fields.split(',')
        ]

@register.filter
def formset_empty_row(formset, fields=None):
    """
    Render the 'empty row' of a FormSet in the template.
    
    Usage::
    
        {{ formset|formset_empty_row:"title,pub_date,status" }}
    """
    return render_to_string('djutils/formset-empty-row.html', {
        'formset': formset,
        'form': formset.empty_form,
        'fields': get_fields_for_formset(formset, fields),
    })

@register.filter
def formset_add_row(formset, colspan=None):
    """
    Render the 'add another row' row for a formset - optional param is the
    colspan, which should be the number of visible fields + 1
    
    Usage::
        
        {{ formset|formset_add_row }}
    """
    if colspan is None:
        fields = formset.empty_form.visible_fields()
        colspan = len(fields) + 1 # add one for the 'remove' link
    
    return render_to_string('djutils/formset-add-row.html', {
        'formset': formset,
        'colspan': colspan,
    })

@register.filter
def formset_forms(formset, fields=None):
    """
    Render the forms in a formset as a series of <tr> elements, optional
    param is which fields should be displayed
    
    Usage::
    
        {{ formset|forms:"title,pub_date,status" }}
    """
    fields = get_fields_for_formset(formset, fields)
    col_span = len(fields) + 1 # adding one for the 'remove' link
    
    return mark_safe(render_to_string('djutils/formset-forms.html', {
        'formset': formset,
        'fields': [f.name for f in fields],
        'col_span': col_span,
    }).strip())

@register.filter
def formset_header_row(formset, fields=None):
    """
    Render the header row for a FormSet as a series of <th> elements, optional
    param is which fields should be displayed
    
    Usage::
    
        {{ formset|formset_header_row:"title,pub_date,status" }}
    """
    return render_to_string('djutils/formset-header-row.html', {
        'formset': formset,
        'fields': get_fields_for_formset(formset, fields)
    })

@register.filter
def dynamic_formset(formset, fields=None):
    """
    Wraps up all of the formset_ filters to generate a complete dynamic
    FormSet for the given fields.
    
    Usage::
    
        {{ formset|dynamic_formset }}
        {{ formset|dynamic_formset:"field1,field2,etc" }}
    """
    form_fields = get_fields_for_formset(formset, fields)
    col_span = len(form_fields) + 1 # adding one for the 'remove' link
    
    return render_to_string('djutils/formset-dynamic.html', {
        'formset': formset,
        'fields': fields,
        'col_span': col_span,
    })

@register.filter
def popular_tags(ctype, limit=None):
    """
    Given a string representation of a model (and assuming that tags is the
    reference to a TaggableManager) return a queryset of the most commonly
    used tags
    
    {% for tag in "media.photos"|popular_tags:5 %}
      ... do something with tag ...
    {% endfor %}
    """
    model = get_model(*ctype.split('.', 1))
    tag_qs = model.tags.most_common()
    if limit:
        tag_qs = tag_qs[:int(limit)]
    return tag_qs

def _model_to_queryset(model):
    if isinstance(model, QuerySet):
        return model
    
    if isinstance(model, basestring):
        model = get_model(*model.split('.'))
    
    if isinstance(model._default_manager, PublishedManager):
        return model._default_manager.published()
    else:
        return model._default_manager.all()

@register.filter
def latest(model_or_qs, date_field='id'):
    """
    Given a model string or a queryset, return the 'newest' instances based
    on the provided field (default is "id")
    
    {% for obj in "media.photos"|latest:"pub_date"|slice:":5" %}
      ... iterate over the 5 newest photos ...
    {% endfor %}
    """
    return _model_to_queryset(model_or_qs).order_by('-%s' % date_field)

@register.filter
def alpha(model, field='title'):
    """
    Given a model string or a queryset, return the instances ordered 
    alphabetically on the provided field (default is "title")
    
    {% for obj in "blog.entries"|alpha:"title" %}
      ... iterate over blog entries alphabetically ...
    {% endfor %}
    """
    return _model_to_queryset(model).order_by('%s' % field)

@register.filter
def call_manager(model_or_obj, method):
    """
    Given a model or object, call a manager method
    
    {% for obj in "blog.entries"|call_manager:"published" %}
      ...
    {% endfor %}
    """
    # load up the model if we were given a string
    if isinstance(model_or_obj, basestring):
        model_or_obj = get_model(*model_or_obj.split('.'))

    # figure out the manager to query
    if isinstance(model_or_obj, QuerySet):
        manager = model_or_obj
    else:
        manager = model_or_obj._default_manager

    return getattr(manager, method)()

@register.filter
def tumble(models_and_dates, limit=5):
    """
    Generate a tumble for one or more models:
    
    {% for activity in "blog.entries:pub_date,media.photos:pub_date,github.commit:commit_date"|tumble:5 %}
      {{ show the 5 most recent things I did }}
    {% endfor %}
    """
    models_and_dates = models_and_dates.split(',')
    
    tumble = []
    
    for model_date in models_and_dates:
        model, date_field = model_date.split(':')
        queryset = _model_to_queryset(model).order_by('-%s' % date_field)[:limit]
        
        for obj in queryset:
            tumble.append((getattr(obj, date_field), obj))
    
    tumble.sort(reverse=True)
    
    return [r[1] for r in tumble]

@register.filter
def syntax_highlight(text):
    """
    Automatically syntax-highlight text between
    &lt;code&gt; tags.
    
    Usage:
    {{ entry.body|syntax_highlight|linebreaks }}
    """
    return mark_safe(re.sub(
        SYNTAX_HIGHLIGHT_RE,
        syntax_highlight_callback,
        text
    ))

def syntax_highlight_callback(match_object):
    data = match_object.group(4)
    data = data.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    return highlight(data)

@register.filter
def gravatar(email, size=80):
    """
    Return the url for a gravatar given an email address
    """
    return 'http://www.gravatar.com/avatar.php?%s' % urllib.urlencode({
        'gravatar_id': md5_constructor(email).hexdigest(),
        'size': str(size)
    })

@register.filter
def as_template(obj, template=None):
    """
    Render a model instance using the given template, defaulting to
        includes/app_label.module_name.html
    """
    if not template:
        template = 'includes/%s.html' % str(obj._meta)
    
    return mark_safe(render_to_string(template, {'object': obj}))

@memoize
def get_media_url_regex():
    media_url = settings.MEDIA_URL.rstrip('/')
    return re.compile(r'^%s/([^\s]+\.(jpg|gif|png))' % media_url, re.I)

@register.filter
def resize(url, width):
    """
    Return a url to a resized version of the given image at the url -- only
    works for files hosted on your MEDIA_ROOT --- CACHE THIS HEAVILY
    """
    width = int(width)
    
    regex = get_media_url_regex()
    
    # check to see if the url is one we can handle, otherwise just return the
    # full size image
    url_match = re.match(regex, url)
    if not url_match:
        return url
    
    # get the path, i.e. images/photos/kitties.jpg    
    image_path = url_match.groups()[0]
    
    # create the entire url as it would be on site, minus the filename
    base_url, ext = url.rsplit('.', 1)
                
    # create the file path minus the extension
    base_path, ext = image_path.rsplit('.', 1)
    
    append = '_%s.%s' % (width, ext)
        
    new_path = '%s%s' % (base_path, append)
    
    if not default_storage.exists(new_path):
        # open the original to calculate its width and height
        img_resize(image_path, new_path, width)
    
    return '%s%s' % (base_url, append)


INLINE_REGEX = re.compile('<inline (?P<attrs>[^>]+)>')
KV_REGEX = re.compile('(\w+)=[\"\']?([^\"\']+)[\"\']?\s*')

@register.filter
def parse_inlines(text):
    """
    Replace <inline type="photo" id="val" class=""> with an embedded object
    rendered using the template as inlines/<model>.html
    """
    text = re.sub(INLINE_REGEX, inline_callback, text)
    return mark_safe(text)

def inline_callback(match_object):
    attrs = match_object.groupdict()['attrs']
    attr_dict = dict([item.groups() for item in KV_REGEX.finditer(attrs)])
    
    inline_type = attr_dict.pop('type')
    inline_pk = attr_dict.pop('id')
    
    if '.' in inline_type:
        model_class = get_model(*inline_type.split('.'))
    else:
        for model in get_models():
            if model._meta.module_name == inline_type:
                model_class = model
                break
        
        if not model_class:
            raise template.TemplateSyntaxError('Could not find model %s' % inline_type)
    
    try:
        obj = model_class._default_manager.get(pk=inline_pk)
    except model_class.DoesNotExist:
        raise template.TemplateSyntaxError('Unable to load %s with pk %s' % (inline_type, inline_pk))
    
    module_name = model_class._meta.module_name
    data = {
        'object': obj,
        'module_name': module_name,
        'attrs': attr_dict
    }
    
    return render_to_string('inlines/%s.html' % module_name, data)

@register.filter
def flatpage_for_url(url):
    try:
        return FlatPage.objects.get(url=url)
    except FlatPage.DoesNotExist:
        pass
