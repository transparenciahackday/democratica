var css_browser_selector = function() {
	var 
		ua=navigator.userAgent.toLowerCase(),
		is=function(t){ return ua.indexOf(t) != -1; },
		h=document.getElementsByTagName('html')[0],
		b=(!(/opera|webtv/i.test(ua))&&/msie (\d)/.test(ua))?('ie ie'+RegExp.$1):is('gecko/')? 'gecko':is('opera/9')?'opera opera9':/opera (\d)/.test(ua)?'opera opera'+RegExp.$1:is('konqueror')?'konqueror':is('applewebkit/')?'webkit safari':is('mozilla/')?'gecko':'',
		os=(is('x11')||is('linux'))?' linux':is('mac')?' mac':is('win')?' win':'';
	var c=b+os+' js';
	h.className += h.className?' '+c:c;
}();


// Browser Codes:
//Códigos de sistemas operativos

//.win - Microsoft Windows
//.linux - Linux (x11 and linux)
//.mac - Mac OS

//Códigos de Browsers

//.ie - Internet Explorer
//.ie6 - Internet Explorer 6
//.ie5 - Internet Explorer 5
//.gecko - Mozilla, Firefox, Camino
//.opera - Opera
//.konqueror - Konqueror
//.webkit or safari - Safari, NetNewsWire, OmniWeb, Shiira