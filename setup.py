from setuptools import setup, Extension

# Parse requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Polyiou extension
polyiou_module = Extension(
    "dotadev.polyiou._polyiou",
    sources=["./dotadev/polyiou/polyiou.i", "./dotadev/polyiou/polyiou.cpp"],
    include_dirs=["./dotadev/polyiou"],
    language="c++",
    swig_opts=["-c++"],
)

setup(
    name="dotadev",
    version="0.1",
    packages=["dotadev"],
    package_dir={"dotadev": "dotadev"},
    ext_modules=[polyiou_module],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        dotadev=dotadev.cli.cli:cli
    """,
    license="MIT",
    author="Ashwin Nair",
    description="""DOTA Devkit CLI""",
    long_description=open("README.md").read(),
)
