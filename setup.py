from setuptools import find_packages, setup

setup(
    name="rdw-ingestion-tools",
    version="0.2.2",
    license="MIT",
    description="Utilities for data ingestion.",
    author="Praekelt.org DS Team",
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=["boto3", "pandas", "requests", "awswrangler"],
)
