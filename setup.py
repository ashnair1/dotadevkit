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
    author="Ashwin Nair",
    author_email="ash1995@gmail.com",
    description="""DOTA Devkit CLI""",
    version="1.0",
    url="https://github.com/ashnair1/DOTA_devkit",
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
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
