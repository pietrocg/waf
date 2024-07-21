from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='Aikido-WAF-PoC',
    version='0.0.1',
    packages=find_packages(),
    install_requires= required_packages,
    author='Pietro Capece',
    author_email='pietro.capece.galeota@gmail.com',
    description='A short description of the library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pietrocg/waf',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update based on your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
