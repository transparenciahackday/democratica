from django.template import Template, RequestContext

from djutils.test import RequestFactoryTestCase


class ContextProcessorsTestCase(RequestFactoryTestCase):
    def test_settings_context_processor(self):
        request = self.request_factory.get('/')
        rendered = Template('{{ settings.IGNORE_THIS }}').render(RequestContext(request))
        self.assertEqual(rendered, 'testing')
