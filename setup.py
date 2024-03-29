from setuptools import setup, find_packages

# Install axi as a package for use in CLI with setup_tools
# - During development, axi can still be used as a module.
# $ python3.8 setup.py develop
# $ axi
# $ axi-repl

# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# Creating:
# /opt/homebrew/lib/python3.8/site-packages/axi.egg-link (link to .)
# Installing axi script to:
# /opt/homebrew/Cellar/python@3.8/3.8.13_3/Frameworks/Python.framework/Versions/3.8/bin

setup(
    name="axi",
    description="Tool to interface with AxiDraw via shell",
    version="0.0.0",
    url="https://github.com/joeysapp/axi",
    author="Joey Sapp",
    
    py_modules=["axi"],
    python_requires="<=3.8.13",
    entry_points={
        "console_scripts": [
            "axi=axi:foo",
            "axi-repl=axi:repl",
        ],
    },

    # note(@joeysapp): does not twerk
    # packages = find_packages(include=['pyaxidraw']), 
)
