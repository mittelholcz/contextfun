from setuptools import setup, find_packages
# from contextfun.version import version


with open('README.md', 'r') as fh:
    long_description = fh.read()


# This call to setup() does all the work
setup(
    name="contextfun",
    version='0.7.0',
    author="mittelholcz",
    author_email="dev.mittelholcz@gmail.com",
    description="context based filtering and mapping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mittelholcz/contextfun",
    license="MIT",
    packages=find_packages(exclude=["test"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
