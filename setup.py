from setuptools import setup, find_packages

LONG_DESCRIPTION = open("README.md", "r").read()

setup(
    name="pareto-client-v1",
    version="0.1.0",
    author="grubiroth",
    author_email="mike@paretolabs.xyz",
    packages=find_packages(),
    description="Client for interacting with Pareto v1 API",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/pareto-xyz/pareto-client-v1",
    install_requires=[
        "eth_account==0.5.9",
        "requests==2.28.1",
    ]
)