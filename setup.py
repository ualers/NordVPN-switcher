import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.3.3'
PACKAGE_NAME = 'nordvpn_switcher'
AUTHOR = 'Kristof Boghe, ualers'
AUTHOR_EMAIL = 'unknown@nowhere.com'
URL = 'https://github.com/ualers/NordVPN-switcher'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Rotate between different NordVPN servers with ease. Works both on Linux and Windows without any required changes to your code!'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['psutil',
'bs4',
'requests',
'lxml',
'pathlib',
'random_user_agent'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      include_package_data=True
      )
