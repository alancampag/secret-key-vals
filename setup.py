from setuptools import setup, find_packages


def read(filename):
    with open(filename) as f:
        return [req.strip() for req in f.readlines()]


setup(
    name="secretkv",
    version="0.0.0",
    description="Store encrypted and versioned key/value pairs",
    author="Alan Campagnaro",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={"dev": read("requirements-dev.txt")},
    entry_points="""
        [console_scripts]
        secretkv=secretkv.main:main
        skv=secretkv.main:main
    """,
)
