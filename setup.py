from setuptools import setup

setup(name='schemaindex',
      version='0.1',
      description='An indexing engine for different types of data sources, including HDFS, Mysql, etc.',
      url='https://github.com/qiyangduan/schemaindex',
      author='Duan Qiyang',
      author_email='qiyang.duan@gmail.com',
      license='Apache Software License',
      include_package_data=True,
      packages=['schemaindex'
               ,'schemaindex.plugin'
               ,'schemaindex.test'
                ],
      install_requires=[
           'tornado',
           'docopt',
           'sqlalchemy',
           'whoosh',
           'hdfs',


      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3', ],
      entry_points={
          'console_scripts': ['stanmo=schemaindex.app.schemaindex:main'],
      },
      classifiers = [ ],
      zip_safe=False)