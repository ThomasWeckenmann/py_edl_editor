""" py_edl_editor setup.py

To install py_edl_editor:

    python setup.py install

"""

# Standard Library Imports
from setuptools import setup


def get_requires():
    """Returns a list of required packages."""
    return [
        'PySide2',
        'cdl_convert',
        'opentimelineio',
        'timecode',
        'edl',
    ]


setup(
    name='py_edl_editor',
    version='0.1.2',
    description="A python EDL (Edit Decision List) Editor GUI.",
    long_description=open('package-info.rst').read(),
    author='Thomas Weckenmann',
    author_email='tweckenmann0711@gmail.com',
    url='https://github.com/ThomasWeckenmann/py_edl_editor',
    license="MIT",
    keywords="video edit decision list editor",
    install_requires=get_requires(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=['py_edl_editor'],
    package_data={'': ['../LICENSE', '../USAGE.md', '../package-info.rst']},
    entry_points={"console_scripts": ["edl_editor=py_edl_editor.__main__:main"]},
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Utilities'
    ]
)
