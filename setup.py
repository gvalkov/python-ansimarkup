from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: BSD License',
]

install_requires = [
    'colorama',
]

extras_require = {
    'tests': [
        'tox >= 2.6.0',
        'pytest >= 3.0.3',
        'pytest-cov >= 2.3.1',
    ],
    'devel': [
        'bumpversion >= 0.5.2',
        'check-manifest >= 0.35',
        'readme-renderer >= 16.0',
        'flake8',
        'pep8-naming',
    ]
}

kw = {
    'name':                 'ansimarkup',
    'version':              '1.5.0',

    'description':          'Produce colored terminal text with an xml-like markup',
    'long_description':     open('README.rst').read(),

    'author':               'Georgi Valkov',
    'author_email':         'georgi.t.valkov@gmail.com',
    'license':              'Revised BSD License',
    'keywords':             'ansi terminal markup',
    'url':                  'https://github.com/gvalkov/python-ansimarkup',
    'classifiers':          classifiers,
    'install_requires':     install_requires,
    'extras_require':       extras_require,
    'packages':             find_packages(),
    'zip_safe':             True,
}


if __name__ == '__main__':
    setup(**kw)
