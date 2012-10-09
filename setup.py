try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'RocketOne connection manager',
    'author': 'Alex Partilov',
    'url': 'http://rocketone.ru/',
    'download_url': 'http://rocketone.ru/download',
    'author_email': 'partilov@rocketone.ru',
    'version': '0.5',
    'install_requires': [],
    'packages': ['RocketOne'],
    'scripts': [],
    'name': 'RocketOne'
}

setup(**config)
