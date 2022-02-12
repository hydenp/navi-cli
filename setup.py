from setuptools import setup, find_packages

setup(
    name='navi-cli',
    version='0.1.0',
    py_modules=['nav'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'navi = nav.__main__:main',
        ],
    },
)