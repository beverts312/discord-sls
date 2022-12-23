from setuptools import find_packages, setup

__version__ = "0.3.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="discord-sls",
    version=__version__,
    license="MIT",
    author="Bailey Everts",
    author_email="bailey@evertsenterprises.com",
    description="For building serverless discord bots",
    url="https://github.com/beverts312/discord-sls",
    packages=find_packages(),
    install_requires=["requests", "PyNaCl", "PyYAML"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points = {
        "console_scripts": ["discord-sls=discord_sls.cli.main:main"],
    }
)