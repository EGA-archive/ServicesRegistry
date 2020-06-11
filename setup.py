from setuptools import setup, find_packages

setup(name='services_registry',
      version='0.1',
      license='Apache License 2.0',
      author='CRG System Developers',
      description='GA4GH Services Registry',
      packages=find_packages(),
      include_package_data=False,
      package_data={'services_registry': ['*.yml']},
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'services_registry = services_registry.dispatcher:main',
          ]
      },
      platforms='any',
      install_requires=[
          'aiohttp',
          'httpx',
          'pyyaml',
      ])
