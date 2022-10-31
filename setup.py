import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="elementary-tutorial",
    description="Tutorial for Elementary.",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.6.2",
    author="Elementary",
    entry_points="""
        [console_scripts]
        elementary-tutorial=elementary_tutorial.cli:cli
    """,
    long_description=README,
    install_requires=["click>=7.0,<9", "elementary-data"],
    extras_require={
        "snowflake": ["elementary-data[snowflake]"],
        "bigquery": ["elementary-data[bigquery]"],
        "redshift": ["elementary-data[redshift]"],
        "postgres": ["elementary-data[postgres]"],
        "databricks": ["elementary-data[databricks]"],
        "spark": ["elementary-data[spark]"],
    },
    long_description_content_type="text/markdown",
    url="https://github.com/elementary-data/tutorial",
    author_email="idan@elementary-data.com",
)
