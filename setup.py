from setuptools import setup, find_packages

setup(
    name='ibkrtwsapi_modules',
    version='0.0.6',
    packages=find_packages(),
    install_requires=['ibapi', 'pandas', 'ta'],
    author='Diego Tamayo',
    author_email='diegowork2203@gmail.com',
    description='Modules for the Interactive Brokers API',
    license='MIT',
    keywords='interactive brokers api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.7',
    ]
)
