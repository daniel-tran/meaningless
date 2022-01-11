import setuptools

with open('VERSION.txt', 'r') as fh:
    version = fh.read()

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()
    
with open('CHANGELOG.md', 'r') as fh:
    changelog = fh.read()

# Read requirements file to determine the dependencies without duplicating the text
with open('REQUIREMENTS.txt', 'r') as fh:
    # Ignore comments, which start with '#'
    install_requires = [requirement.strip() for requirement in fh.readlines() if not requirement.startswith('#')]
    
setuptools.setup(
    name='meaningless',
    version=version,
    author='Daniel Tran',
    author_email='dantran.au@gmail.com',
    description='Retrieves, processes and downloads Bible passages from Bible Gateway',
    license='MIT License',
    long_description='\n'.join([readme, changelog]),
    long_description_content_type='text/markdown',
    url='https://github.com/daniel-tran/meaningless',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Religion',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Religion',
    ],
    keywords='bible yaml json xml biblegateway',
    python_requires='>=3.6',
    install_requires=install_requires,
)
