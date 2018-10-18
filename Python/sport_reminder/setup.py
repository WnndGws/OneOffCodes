from setuptools import setup

setup(
    name='sport_reminder',
    version='0.1',
    py_modules=['sport_reminder'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sport_reminder=sport_reminder:main
    ''',
)
