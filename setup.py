from setuptools import setup, find_packages

setup(
    name='RESI-BEM-BEM',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'numpy',
        'pandas',
        'matplotlib',
        'requests',
    ],

    author='Zixin Jiang',
    author_email='zjiang19@syr.edu',
    description='RESI-BEM: a click and run plugin for future weather, extreme weather, and power outage data download.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Bugs-Owner/RESI-One-click-for-future-building-energy-simulation.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)