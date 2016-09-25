from distutils.core import setup

setup(
    name='SSKJpy',
    author="DefaltSimon",
    version='0.2',
    license='MIT',
    packages=["sskjpy"],
    description="A Slovenian dictionary scrapper written in python",
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 >= 4.4.1",
    ],
)
