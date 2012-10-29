from setuptools import setup, find_packages
from turbogears.finddata import find_package_data


packages=find_packages()
package_data = find_package_data(where='tgldapid', package='tgldapid')

setup(name="tgldapid",
      version="0.1",
      description="A TurboGeard LDAP identity provider",
      author="Mathieu Bridon",
      author_email="bochecha@fedoraproject.org",
      url="TODO",
      download_url="TODO",
      license="MIT",
      install_requires=[
          "TurboGears >= 1.1",
          "python-ldap >= 2.3",
      ],
      zip_safe=False,
      packages=packages,
      package_data=package_data,
      keywords=[
          'turbogears.identity.provider',
      ],
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Framework :: TurboGears',
      ],
      entry_points = {
          'turbogears.identity.provider': [
              'ldapprovider = tgldapid.provider:LdapIdentityProvider'
          ]
      },
      )
