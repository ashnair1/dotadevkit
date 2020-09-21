from setuptools import Extension, find_packages, setup

# Parse requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Polyiou extension
polyiou_module = Extension(
    "dotadevkit.polyiou._polyiou",
    sources=["./dotadevkit/polyiou/polyiou_wrap.cxx", "./dotadevkit/polyiou/polyiou.cpp"],
    include_dirs=["./dotadevkit/polyiou"],
    language="c++",
)

setup(
    name="dotadevkit",
    version="1.0.0-beta",
    packages=find_packages(),
    package_dir={"dotadevkit": "dotadevkit"},
    python_requires=">=3.6",
    ext_modules=[polyiou_module],
    install_requires=requirements,
    include_package_data=True,
    entry_points="""
        [console_scripts]
        dotadevkit=dotadevkit.cli.cli:cli
    """,
    license="MIT",
    author="Ashwin Nair",
    author_email="ash1995@gmail.com",
    description="""DOTA Devkit CLI""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
