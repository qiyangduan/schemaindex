from setuptools import setup

setup(name='stanmo',
      version='0.2',
      description='Execution engine for standard business learning models.',
      url='https://github.com/qiyangduan/stanmo',
      author='Duan Qiyang',
      author_email='qiyang.duan@qq.com',
      license='Apache Software License',
      include_package_data=True,
      packages=['stanmo'
               ,'stanmo.app'
               ,'stanmo.data'
               ,'stanmo.log'
               ,'stanmo.spec'
               ,'stanmo.spec'
               ,'stanmo.test'
                ],
      install_requires=[
          'simplejson', 'flask', 'docopt','sqlalchemy',
          'pandas','scikit-learn','scipy'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3', 'simplejson','sqlalchemy',
                    'flask',
                    'docopt',
                    'pandas',
                    'scikit-learn',
                    'scipy'],
      entry_points={
          'console_scripts': ['stanmo=stanmo.stanmoctl:main'],
      },
      classifiers = [ ],
      zip_safe=False)