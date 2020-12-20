import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sport Analytics - xvalerog", # Replace with your own username
    version="0.0.1",
    author="Xavier Valero",
    author_email="xvalerog@gmail.com",
    description="Package to import Garmin data and do some analytics with it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xvalerog/sportAnalytics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)