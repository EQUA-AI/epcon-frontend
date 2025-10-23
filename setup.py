from setuptools import setup, find_packages

setup(
    name="epcon-frontend",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'inventree_plugins': [
            'HideLinksPlugin = hide_links_plugin.core:HideLinksPlugin',
        ],
    },
    install_requires=[],
    author="EPCON",
    author_email="",
    description="InvenTree UI plugin to hide Documentation / About / Getting Started links",
    url="https://github.com/EQUA-AI/Inventree_IPN_Generator",
    license="MIT",
)
