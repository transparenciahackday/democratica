from djutils.utils.http import fetch_url


class AkismetClient(object):
    """
    Client library to talk to Akismet, the spam detection service.
    """
    
    def __init__(self, api_key, blog_url):
        self.api_key = api_key
        self.blog_url = blog_url

    def verify_key(self):
        try:
            return fetch_url('http://rest.akismet.com/1.1/verify-key', {
                'key': self.api_key,
                'blog': self.blog_url
            }, 'POST') == 'valid'
        except:
            return False
    
    def _make_call(self, action, comment, ip, author='', email='', user_agent=''):
        return fetch_url('http://%s.rest.akismet.com/1.1/%s' % (self.api_key, action), {
            'comment_content': comment,
            'comment_type': 'comment',
            'comment_author': author,
            'comment_author_email': email,
            'user_agent': user_agent,
            'user_ip': ip,
            'blog': self.blog_url
        }, 'POST')

    def is_spam(self, comment, ip, author='', email=''):
        """
        Determine whether the comment is spam, returns True/False
        """
        try:
            return self._make_call('comment-check', comment, ip, author, email) == 'true'
        except:
            return False
    
    def submit_spam(self, comment, ip, author='', email=''):
        try:
            return 'Thanks' in self._make_call('submit-spam', comment, ip, author, email)
        except:
            return False
    
    def submit_ham(self, comment, ip, author='', email=''):
        try:
            return 'Thanks' in self._make_call('submit-ham', comment, ip, author, email)
        except:
            return False
