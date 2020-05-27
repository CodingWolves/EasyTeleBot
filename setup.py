import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyTeleBot",  # Replace with your own username
    version="0.0.1",
    author="Ido Zahavy",
    author_email="idozahavy@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idozahavy/EasyBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
# https://packaging.python.org/tutorials/packaging-projects/
