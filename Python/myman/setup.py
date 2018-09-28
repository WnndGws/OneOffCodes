from setuptools import setup

setup(
    name='myman',
    version='1.1',
    py_modules=['myman'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        myman=myman:try_tldr
    ''',
)

