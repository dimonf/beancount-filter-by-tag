import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["beancount"]

setuptools.setup(
        name="beancount-filter-by-tag",
        version="0.0.1",
        author="Dmitri Kourbatsky",
        author_email="camel109@gmail.com",
        decription="A beancount plugin, which filters transactions by tag",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dimonf/beancount-filter-by-tag",
#        packages = setuptools.find_packages(),
        packages = ['beancount_filter_by_tag'],
        package_dir={'beancount_filter_by_tag':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=requirements,
)

