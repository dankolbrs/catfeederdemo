from setuptools import setup

setup(
    name='catfeeder',
    packages=['catfeeder'],
    include_package_data=True,
    install_requires=[open('requirements.txt').read().split('\n')]
)
