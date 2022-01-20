from setuptools import setup

setup(
    name='navi',
    version='0.1.0',
    py_modules=['nav'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'navi = nav:nav',
        ],
    },
)