import setuptools

# Developer self-reminder for uploading in pypi:
# - install: wheel, twine
# - build  : python setup.py bdist_wheel
# - deploy : twine upload dist/*

with open("README.md", "r") as file:
    long_description = """
# DUFuz
Incorporating discrete numeric fuzzy sets in Python algorithms.
These sets are more general than fuzzy numbers.

**Dependencies**: `numpy`, `torch`, `matplotlib`, `ply`<br>
**Contact**: Manios Krasanakis (maniospas@hotmail.com)<br>
**License**: Apache 2<br>
<br>
Documentation in the [github](https://github.com/maniospas/dufuz) page.
    """

setuptools.setup(
    name='dufuz',
    version='0.1.4',
    author="Emmanouil (Manios) Krasanakis",
    author_email="maniospas@hotmail.com",
    description="Discrete numeric fuzzy sets in Python algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maniospas/dufuz",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
    install_requires=['numpy', 'torch', 'matplotlib', 'ply'],
 )