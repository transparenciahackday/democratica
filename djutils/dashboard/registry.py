from django.conf import settings


class PanelRegistryException(Exception):
    pass


class PanelRegistry(object):
    """\
    A simple Registry used to track subclasses of :class:`PanelProvider`
    """
    _registry = {}
    
    def register(self, panel_class):
        # register a panel class and cause it to be updated periodically
        if panel_class in self._registry:
            raise PanelRegistryException('"%s" is already registered' % panel_class)
        
        panel_obj = panel_class()
        self._registry[panel_class] = panel_obj

    def unregister(self, panel_class):
        if panel_class not in self._registry:
            raise PanelRegistryException('"%s" is not registered' % panel_class)
        
        del(self._registry[panel_class])
    
    def __contains__(self, panel_class):
        return panel_class in self._registry
    
    def get_provider_instances(self):
        return self._registry.values()
    
    def get_titles(self):
        return [
            provider.get_title() for provider in self.get_provider_instances()
        ]


registry = PanelRegistry()
