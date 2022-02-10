from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in facturacion/__init__.py
from facturacion import __version__ as version

setup(
	name='facturacion',
	version=version,
	description='Aplicacion inventario de productos y facturacion ',
	author='Frappe',
	author_email='odalisvalencia11@hotmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
