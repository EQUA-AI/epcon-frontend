try:
    from setuptools import setup, find_packages
except ImportError as e:
    raise RuntimeError("setuptools is required to build epcon-frontend plugin") from e
from pathlib import Path

README = (Path(__file__).parent / "README.md")
long_description = README.read_text(encoding="utf-8") if README.exists() else "EPCON Frontend Tweaks plugin for InvenTree."

setup(
    name="epcon-frontend",
    version="0.1.0",
    packages=find_packages(include=["hide_links_plugin*"]),
    include_package_data=True,
    entry_points={
        'inventree_plugins': [
            # Use slug name for clarity; now points to class EpconFrontend
            'epcon-frontend = hide_links_plugin.core:EpconFrontend',
        ],
    },
    install_requires=[],
    author="EPCON",
    author_email="dev@epcon.ai",
    description="InvenTree UI plugin to hide Documentation / About / Getting Started links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EQUA-AI/epcon-frontend",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: InvenTree",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.9",
)
