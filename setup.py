from setuptools import setup, find_packages

setup(
    name="passwork-python",
    version="0.1.1",
    description="Python client for Passwork 7 API",
    author="Passwork Team",
    url="https://github.com/passwork-me/passwork-python",
    packages=["passwork_client", "passwork_client.modules", "passwork_client.enums", "cli", "cli.commands"],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "cryptography>=42.0.0",
        "pbkdf2>=1.3",
    ],
    entry_points={
        'console_scripts': [
            'passwork-cli=cli.main:main',
        ],
    },
) 