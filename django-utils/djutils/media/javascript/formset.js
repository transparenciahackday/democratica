FormSet = function(prefix, fs_options) {
  var $ = jQuery;
  var prefix = prefix;
  var options = (typeof fs_options == 'object')? fs_options: {};
  var addFormCallback = (typeof options.addFormCallback == 'function')? options.addFormCallback: undefined;
  var deleteFormCallback = (typeof options.deleteFormCallback == 'function')? options.deleteFormCallback: undefined;
  
  /* update the label, name and id of each element in the row */
  function updateElementIndex(el, ndx) {
    var id_regex = new RegExp(prefix + '-(__prefix__|\\d+)-');
    var replacement = prefix + '-' + ndx + '-';
    
    /* update labels */
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    
    /* update id and name attributes */
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
  }

  function addForm(btn) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('tr.empty-row.' + prefix).clone(true).get(0);
    var rowObj = $(row);
    
    rowObj.removeClass('empty-row').addClass('dynamic-form');
    rowObj.insertBefore($('tr#' + prefix + '-add-row'));
    rowObj.children().not(':last').children().each(function() {
	    updateElementIndex(this, formCount);
	    $(this).val('');
    });
    
    rowObj.find('.' + prefix + '-delete-row').click(function() {
	    deleteForm(this, prefix);
    });
    
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    
    if (addFormCallback) { addFormCallback(rowObj); }
    
    return false;
  }

  function deleteForm(btn) {
    $(btn).parents('.dynamic-form').remove();
    var forms = $('tr.dynamic-form.' + prefix);
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    
    for (var i=0, formCount=forms.length; i < formCount; i++) {
	    $(forms.get(i)).children().not(':last').children().each(function() {
	        updateElementIndex(this, i);
	    });
    }
    
    if (deleteFormCallback) { deleteFormCallback(forms); }
    
    return false;
  }
    
  /* configure the events */
  $('.'+prefix+'-add-row').click(function() {
    return addForm(this);
  });
  $('.'+prefix+'-delete-row').click(function() {
    return deleteForm(this);
  });
};
