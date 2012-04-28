Spam
====

.. py:module:: djutils.utils.spam

A registry-style interface for checking whether particular objects are spam.


Creating SpamProviders
----------------------

Spam filters need to subclass :class:`SpamProvider`, which implements a few
methods for extracting information from arbitrary objects and sending it off
to Akismet for checking.

Take a look at the :class:`CommentProvider`::

    class CommentProvider(SpamProvider):
        """
        Sample implementation for checking Comments for spam
        """
        def get_comment(self, obj):
            return obj.comment
        
        def get_author(self, obj):
            return obj.user_name
        
        def get_email(self, obj):
            return obj.user_email
        
        def get_ip(self, obj):
            return obj.ip_address
        
        def should_check(self, obj):
            return obj.is_public
        
        def is_spam(self, obj):
            obj.is_public = False
            obj.save()


Each SpamProvider you create needs to be registered::

    from django.contrib.comments.models import Comment
    
    from djutils.utils.spam import site
    
    # associate the Comment model with the CommentProvider
    site.register(Comment, CommentProvider)


This *still* doesn't do everything - you'll need to wire up a signal or some
other system for telling the Spam checking system when an object needs to be
checked.  The Comment example does the following::

    def moderate_comment(sender, comment, request, **kwargs):
        if not comment.id:
            site.check_spam(comment)

    def attach_comment_listener(func=moderate_comment):
        comment_will_be_posted.connect(func, sender=Comment,
            dispatch_uid='djutils.spam.comments.listeners')

If you want to activate the comment listener for your own site, call the following
anywhere in your code you would normally configure a Signal::

    from djutils.utils.spam import attach_comment_listener
    
    # comments will now be wired up
    attach_comment_listener()
