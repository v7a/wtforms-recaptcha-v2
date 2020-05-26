import setuptools

from wtforms_recaptcha_v2 import __version__


with open("README.md", "r") as readme:
    setuptools.setup(
        name="wtforms-recaptcha-v2",
        version=__version__,
        author="v7a",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/v7a/wtforms-recaptcha-v2",
        keywords=["wtforms", "recaptcha", "recaptcha-v2", "google"],
        install_requires=["wtforms >= 2.2", "requests >= 2.10"],
        py_modules=["wtforms_recaptcha_v2"],
        license="MIT",
        project_urls={
            "Source": "https://github.com/v7a/wtforms-recaptcha-v2",
            "Tracker": "https://github.com/v7a/wtforms-recaptcha-v2/issues",
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3 :: Only",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Internet :: WWW/HTTP",
        ],
    )
