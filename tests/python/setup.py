from setuptools import setup, find_packages

setup(
    name='test_package',
    version='0.1.dev0',
    url='https://github.com/test-package-for-scade-actions.git',
    author='ESEG',
    author_email='test@unknown.com',
    description='Test purpose',
    packages=find_packages(where='./src'),
    package_dir={"": "src"},
)
