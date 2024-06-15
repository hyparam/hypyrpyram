from setuptools import setup, find_packages

setup(
    name='hypyrpyram',
    version='0.1.0',
    description='A description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/hyparam/hypyrpyram',
    packages=find_packages(),
    install_requires=[
        "wheel",
    ],
    entry_points={
        'console_scripts': [
            'hyp = hypyrpyram.hyp:main',
            'hyperparam = hypyrpyram.hyp:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
