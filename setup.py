import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyTeleBot",
    version="0.0.2",
    author="Ido Zahavy",
    author_email="idozahavy@gmail.com",
    description="Configurable Telegram Bot package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idozahavy/EasyTeleBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",  # 3 - Alpha , 4 - Beta , 5 - Production/Stable
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["python-telegram-bot", "flask"]
)
# https://packaging.python.org/tutorials/packaging-projects/
