import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.5.1"               , # change this on every release
    name                          = "pbx_gs_python_utils"  ,

    author                        = "Dinis Cruz",
    author_email                  = "dinis.cruz@owasp.org",
    description                   = "PBX GS Python Utils",
    long_description              = long_description,
    long_description_content_type = " text/markdown",
    url                           = "https://github.com/pbx-gs/pbx-gs-python-utils",
    install_requires              = [
                                      'boto3',
                                      'elasticsearch',
                                      'matplotlib',
                                      'osbot_aws',
                                      'requests',
                                      'slackclient',
                                  ],
    packages                      = setuptools.find_packages(),
    tests_require                 = ['pytest'],
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])