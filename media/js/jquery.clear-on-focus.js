/* Jquery code from
http://bassistance.de/2007/01/23/unobtrusive-clear-searchfield-on-focus/
*/


$(document).ready(function(){

$.fn.search = function() {
	return this.focus(function() {
		if( this.value == this.defaultValue ) {
			this.value = "";
		}
	}).blur(function() {
		if( !this.value.length ) {
			this.value = this.defaultValue;
		}
	});
};

});
