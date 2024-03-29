import setuptools


def readme():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='selenium-helpers',
    version='1.0.5',
    description='Tools to make certain selenium tasks more straightforward.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ExSidius/selenium_helpers',
    author='ExSidius',
    author_email='mukul.ram97@gmail.com',
    license='MIT',
    install_requires=['selenium'],
    include_package_data=True,
    packages=setuptools.find_packages(),
    zip_safe=False,
)
