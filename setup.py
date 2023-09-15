from setuptools import setup, find_packages

def read_requirements(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

setup(
    name='LiquidEarthAPI',
    version='0.1',
    packages=find_packages(),
    url='',
    license='EUGPL',
    author='MigueldelaVarga',
    author_email='miguel@terranigma-solutions.com',
    description='',
    install_requires=read_requirements("requirements.txt"),
)
