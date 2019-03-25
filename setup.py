import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pbx_gs_python_utils",
    version="0.2.12",
    author="Dinis Cruz",
    author_email="dinis.cruz@owasp.org",
    description="PBX GS Python Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbx-gs/pbx-gs-python-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)