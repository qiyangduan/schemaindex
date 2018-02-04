from setuptools import setup, find_packages


# following https://python-packaging-user-guide.readthedocs.io/tutorials/distributing-packages/

setup(name='schemaindex',
      version='0.243',
      description='An indexing engine for different types of data sources, including HDFS, Mysql, etc.',
      url='https://github.com/qiyangduan/schemaindex',
      author='Duan Qiyang',
      author_email='qiyang.duan@gmail.com',
      license='Apache Software License',
      include_package_data=True,
      packages=['schemaindex'
               # ,'schemaindex.plugin'
               ,'schemaindex.jupyterext'
               ,'schemaindex.app'
                ],
      install_requires=[
           'tornado',
           'docopt',
           'sqlalchemy',
           'whoosh',
           'hdfs',
           'future',
          'pymssql',
          'pymysql',



      ],
      entry_points={
          'console_scripts': ['schemaindex=schemaindex.schemaindexctl:main'],
      },
      classifiers = [
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: System :: Systems Administration',
          'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
      ],
      zip_safe=False)
