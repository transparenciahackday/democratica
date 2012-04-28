import os
from setuptools import setup, find_packages

from djutils import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='djutils',
    version=".".join(map(str, VERSION)),
    description='a collection of tools',
    long_description=readme,
    author='Charles Leifer',
    author_email='coleifer@gmail.com',
    url='http://github.com/coleifer/django-utils/tree/master',
    packages=find_packages(),
    package_data = {
        'djutils': [
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests',
    tests_require=['pygments', 'PIL>=0.1.5', 'httplib2'],
)
