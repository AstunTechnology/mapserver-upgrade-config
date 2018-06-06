from setuptools import setup

setup(name='mapfile-utils',
      version='1.0.0',
      description='Useful scripts for mapfile manipulation',
      url='',
      author='Ian Turton',
      author_email='ianturton@astuntechnology.com',
      license='MIT',
      entry_points = {
          'console_scripts':[
              'load-map=maputils.map_loader:main',
              'fix-map=maputils.fix_mapfile:main',
              'map-to-xml=maputils.map_to_xml:main'
              ]
          },
      packages=['maputils'],
      install_requires=['mappyfile','lxml','plyplus'],
      dependency_links=['http://download.astuntechnology.com/public/mappyfile-0.7.1a0-py2.7.egg',
                    'https://github.com/AstunTechnology/mapserver-upgrade-config/raw/master/dist/maputils-0.2.1-py2.7.egg'],
      zip_safe=False)
