from djutils.dashboard.models import Panel


class PanelProvider(object):
    """\
    Base class from which other panel providers should derive.  Much like a
    munin plugin, there is no input provided and the output conforms to a
    standard format.
    
    Methods of interest:

    :method:`get_data` returns a dictionary of data to be plotted
    
    :method:`get_title` returns the title for the panel
    :method:`get_priority` returns an arbitrary integer indicating the order in
        which this panel should be processed
    """
    
    def get_data(self):
        """\
        Must be a dictionary keyed by a set of labels and their values::
        
            {
                'database_connections': 3,
                'idle_connections': 1,
                'idle_in_transaction': 1,
            }
        """
        raise NotImplementedError

    def get_title(self):
        raise NotImplementedError
    
    def get_priority(self):
        return 20
    
    def get_panel_instance(self):
        panel, _ = Panel.objects.get_or_create(title=self.get_title())
        return panel
