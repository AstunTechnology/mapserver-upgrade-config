from setuptools import setup

setup(name='mapfile-utils',
      version='2.3.0',
      description='Useful scripts for mapfile manipulation',
      url='',
      author='Ian Turton',
      author_email='ianturton@astuntechnology.com',
      license='MIT',
      entry_points={
          'console_scripts': [
              'load-map=maputils.map_loader:main',
              'fix-map=maputils.fix_mapfile:main',
              'map-to-xml=maputils.map_to_xml:main',
              'xml-to-sld=maputils.xml_to_sld:main'
          ]
      },
      packages=['maputils'],
      install_requires=['mappyfile>=0.8.4', 'lxml'],
      # dependency_links=[
      #     'http://download.astuntechnology.com/public/mappyfile-0.8.4b0-py3.6.egg'
      # ],
      zip_safe=False)
