from setuptools import setup, find_packages

setup(
    name='navi-cli',
    version='0.1.0',
    description='See the Github repo',
    author="Real Python",
    author_email="hyden.dev@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'Click',
    ],
    py_modules=['nav'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'navi=nav.__main__:main',
        ],
    },
)