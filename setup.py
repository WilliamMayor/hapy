try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A Python wrapper around the Heritrix API.',
    'author': 'William Mayor',
    'url': 'https://github.com/WilliamMayor/hapy',
    'download_url': 'https://github.com/WilliamMayor/hapy',
    'author_email': 'w.mayor@ucl.ac.uk',
    'version': '0.1',
    'install_requires': ['nose', 'requests'],
    'packages': ['hapy'],
    'scripts': [],
    'name': 'hapy-heritrix',
    'package_data': {
        'hapy': ['scripts/delete_job.groovy']
    },
}

setup(**config)
