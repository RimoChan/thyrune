import setuptools


setuptools.setup(
    name='thyrune',
    version='1.0.1',
    author='RimoChan',
    author_email='the@librian.net',
    description='thyrune',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/thyrune',
    packages=[
        'thyrune',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.24.1',
        'numpy-stl>=3.0.1',
    ],
)
