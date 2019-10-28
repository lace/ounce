from setuptools import setup, find_packages

version_info = {}
exec(open("ounce/package_version.py").read(), version_info)

readme = open("README.md", "rb").read().decode("utf-8")

setup(
    name="ounce",
    version=version_info["__version__"],
    description="A simple Python package to manipulate units",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Metabolize, Body Labs, and other contributors",
    author_email="github@paulmelnikow.com",
    url="https://github.com/lace/ounce",
    project_urls={
        "Issue Tracker": "https://github.com/lace/ounce/issues",
        "Documentation": "https://ounce.readthedocs.io/en/stable/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
