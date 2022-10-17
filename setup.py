from setuptools import setup, find_packages

dev_require=[
    'prospector[with_everything] >= 1.7.7, <2',
]

setup(
    name='morsa',
    version='0.2.1',
    url='qwe',
    author='qwe',
    author_email='qwe',
    license='good luck',
    description='crawler dorks',
    long_description='super long descruiptio',
    long_description_content_type='text/markdown',
    keywords='Prima Cloud, SDK',
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: GLWT(Good Luck With That) Public License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['requests >= 2.27.1, < 3', 'PyYAML','beautifulsoup4','prospector','openpyxl','wcmatch','click','mariadb','tenacity'],
    extras_require={  
        "test": ["pytest"],
        "dev": dev_require,
    },
    
    # entry_points={
    #     'console_scripts': [
    #         'cspm-reporter=prisma_cloud_api.cspm_report:get_alerts'
    #     ]
    # }
)
