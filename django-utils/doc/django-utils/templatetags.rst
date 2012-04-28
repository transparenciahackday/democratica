Templatetags
============

All templatetags are included in a library named :mod:`djutils_tags`.  There
are a handful of tags related to creating dynamic formsets, numerous filters
for grabbing querysets dynamically, and a couple other miscellaneous filters.


Dynamic FormSets
----------------

.. py:function:: dynamic_formset(formset, fields)

    Wraps up all of the formset filters to generate a complete dynamic
    FormSet for the given fields.
    
    Usage::
    
        <script type="text/javascript" src="/path/to/djutils/media/javascript/formset.js"></script>
        <script type="text/javascript">
            $(function() {
                FormSet('{{ formset.prefix }}');
            });
        </script>
        
        ...
    
        {{ formset|dynamic_formset }}
        {{ formset|dynamic_formset:"field1,field2,etc" }}
    
    Generates::
    
        <thead><tr class="header-row form">
          <th>Name</th><th>Choice</th>
        </tr></thead>
        
        <tr class="empty-row form">
          <td><input type="text" name="form-__prefix__-name" id="id_form-__prefix__-name" /></td><td><select name="form-__prefix__-choice" id="id_form-__prefix__-choice">
        <option value="1">One</option>
        <option value="2">Two</option>
        </select></td>
          <td><a href="javascript:void(0)" class="form-delete-row">Remove</a></td>
        </tr>
        
        <tr class="dynamic-form form">
            <td><input type="text" name="form-0-name" id="id_form-0-name" /></td><td><select name="form-0-choice" id="id_form-0-choice">
        <option value="1">One</option>
        <option value="2">Two</option>
        </select></td>
        
          </tr>
        <tr id="form-add-row">
          <td colspan="3"><a href="javascript:void(0)" class="form-add-row">Add row</a></td>
        </tr>
    
    Looking closer, there are 4 "distinct" chunks of markup generated.  The :func:`dynamic_formset`
    function wraps up the following filters which are responsible for generating
    each chunk of markup:
    
    .. py:function:: dynamic_formset_header_row(formset, fields)
    
    .. py:function:: dynamic_formset_empty_row(formset, fields)
    
    .. py:function:: dynamic_formset_forms(formset, fields)
    
    .. py:function:: dynamic_formset_add_row(formset, colspan)
    
    .. warning: Be sure to include the formset javascript when you use the
        :func:`dynamic_formset` filter - located in djutils/media/javascript/formset.js
    

Model Filters
-------------

A collection of filters that operates on querysets or models.

.. note:: if the model uses a :class:`PublishedManager` then these filters will
    operate on the :func:`published` instances as opposed to :func:`all`

.. py:function:: latest(model_or_qs, date_field='id')

    Given a model string or a queryset, return the 'newest' instances based
    on the provided field (default is "id")
    
    Example::
    
        {% for obj in "media.photos"|latest:"pub_date"|slice:":5" %}
          ... iterate over the 5 newest photos ...
        {% endfor %}

.. py:function:: alpha(model, field='title')

    Given a model string or a queryset, return the instances ordered 
    alphabetically on the provided field (default is "title")
    
    Example::
    
        {% for obj in "blog.entries"|alpha:"title" %}
          ... iterate over blog entries alphabetically ...
        {% endfor %}

.. py:function:: call_manager(model_or_obj, method)

    Given a model or object, call a manager method
    
    Example::
    
        {% for obj in "blog.entries"|call_manager:"published" %}
          ...
        {% endfor %}

.. py:function:: tumble(models_and_dates, limit=5)

    Generate a tumble for one or more models.  Useful for creating a list
    comprised of various model classes.
    
    The first argument, `models_and_dates`, is a comma-separated list of
    models.  Each model can optionally define a field to sort by, separated
    by a colon, i.e. "app.model_name:field"
    
    Example::
    
        {% for activity in "blog.entries:pub_date,github.commit:commit_date"|tumble:5 %}
          {{ show the 5 most recent things I did }}
        {% endfor %}


Miscellaneous Filters
---------------------

.. py:function:: syntax_highlight(text)

    Automatically syntax-highlight text between
    <code> tags.
    
    Example::
    
        {{ entry.body|syntax_highlight|linebreaks }}

.. py:function:: gravatar(email, size=80)

    Return the url for a gravatar given an email address

.. py:function:: as_template(obj, template=None)

    Render a model instance using the given template, defaulting to
    `includes/*app_label.module_name*.html`
    
    Example::
    
        <ul>
        {% for obj in object_list %}
          <li>{{ obj|as_template }}</li>
        {% endfor %}
        </ul>
