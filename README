# Demo.cratica

A web application for visualising parliamentary information. Originally
developed for the Portuguese Parliament; this version of the application can be
seen in action at http://demo.cratica.org

## Want to use this?

If you're interested in this software, awesome!

However, you'll probably need our help to get it going. So you just need to ping us at contacto (at) cratica (dot) org and we'll be glad to help get you up to speed -- and use the excuse to writer proper docs so everyone can benefit.

Below we hastily specify the steps to get it going, mostly for our own reference. We'll document this better as soon as someone lets us know they need it.

## Bootstrapping after install

	python manage.py syncdb
	python manage.py migrate --all
	
	cd scripts
	python import_mps.py
	python import_parties.py
	python import_governments.py
	python import_linksets.py
	python import_mp_photos.py
	python import_legislatures.py
	python determine_mp_gender.py
	for f in ~/repos/dar-json/12/*.json; do python import_json_transcripts.py -i ${f} -f; done

## Updating after git pull

	python manage.py migrate --all

	cd scripts
	python import_mps.py
	python import_mp_photos.py
	for f in ~/repos/dar/12/*.json; do python import_json_transcripts.py -i ${f} -f; done
	
## Rights and licencing

Copyright (c) 2010-2011 - [Ana Carvalho](ana@manufacturaindependente.org) & [Ricardo
Lafuente](ricardo@manufacturaindependente.org).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see (http://www.gnu.org/licenses).

The full license text can be found inside the AGPL.txt file inside this directory.

Other bundled software
----------------------

Demo.cratica bundles software by other authors. Here you can find the licensing
terms for each of the packages included in the Demo.cratica repository.

Django-Haystack is Copyright (c) 2009-2010 - Daniel Lindsley. 
Licensed under the BSD license. Read the license at:
https://github.com/toastdriven/django-haystack/blob/master/LICENSE

(Located at democratica/haystack/)

Django Extensions is Copyright (c) Michael Trier <mtrier at gmail com>.
Licensed under the new BSD license. Read the license at:
https://github.com/django-extensions/django-extensions/blob/master/LICENSE

(Located at democratica/django_extensions/)

Text counting utilities from Openparliament.ca are Copyright (C) 2010 Michael
Mulley (michaelmulley.com). 
Licensed under the AGPL. Read the license at:
https://github.com/rhymeswithcycle/openparliament/blob/master/LICENSE

(Located at democratica/core/text_utils.py)

Django Debug Toolbar is Copyright (c) Rob Hudson and individual contributors.
Licensed under the BSD license. Read the license at:
https://github.com/robhudson/django-debug-toolbar/blob/master/LICENSE

(Located at democratica/debug_toolbar/)

Django South is Copyright (c) Andrew Godwin.  
Licensed under the Apache license 2.0. Read the license at:
https://bitbucket.org/andrewgodwin/south/src/5f96edecdc73/LICENSE

(Located at democratica/south/)

jQuery is Copyright (c) 2010 The jQuery Project.
Licensed under the GPL. Read the license at:
http://jquery.org/license/

(Located at democratica/media/js/)

HighCharts is Copyright (c) Highslide Software.
Licensed under the Creative Commons Attribution-NonCommercial license. Read the
license at: 
http://www.highcharts.com/license

(Located at democratica/media/js/highcharts)

Tipsy is Copyright (c) 2008 Jason Frame.
Licensed under the MIT license. Read the
license at: 
http://www.opensource.org/licenses/mit-license.php

(Located at democratica/media/js/tipsy)

Selectivizr v1.0.2 is Copyright (c) Keith Clark.
Licensed under the MIT license. Read the
license at: 
http://www.opensource.org/licenses/mit-license.php

(Located at democratica/media/js/selectivizr.js)

ScrollToCopyright is Copyright (c) 2007-2009 Ariel Flesler.
Licensed under the GPL license. Read the
license at: 
http://www.gnu.org/licenses/gpl.html

(Located at democratica/media/js/scrollTo)

Uniform is Copyright (c) 2009 Josh Pyles / Pixelmatrix Design LLC.
Licensed under the MIT license. Read the
license at: 
http://www.opensource.org/licenses/mit-license.php

(Located at democratica/media/js/uniform)
