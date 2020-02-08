import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.1",
    author="Keith Sloan",
    author_email="keith@sloan-home.co.uk",
    description="Python module for creation of GDML under CQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeithSloan/CQ_GDML_Package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
