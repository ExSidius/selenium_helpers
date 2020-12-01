# Building a new version

In order to build a new version - 

1. Increment the version in `setup.py`
2. `rm -rf build dist selenium_helpers.egg-info`
3. `python setup.py sdist bdist_wheel`
4. `python -m twine upload --repository pypi dist/*`