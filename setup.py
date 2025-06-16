from setuptools import setup, find_packages

setup(
    name='KDSlib',
    version='0.2',
    description="Python library for automating the KDS legato 110.",
    author='Kylie Herbstzuber',
    author_email='kmhswimgirl@gmail.com',
    maintainer='@kmhswimgirl',
    url="https://github.com/kmhswimgirl/KDSlib",
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.5'
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown"
)