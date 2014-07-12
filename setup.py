from distutils.core import setup

setup(
    name='boa',
    version='0.0.1',
    packages=['boa', 'boa.dom', 'boa.gen', 'boa.game', 'boa.lang', 'boa.tools'],
    url='https://github.com/gratimax/boa',
    license='MIT',
    author='Max Ovsiankin',
    author_email='max@ovsankin.com',
    description='A JS runtime for Python.'
)
