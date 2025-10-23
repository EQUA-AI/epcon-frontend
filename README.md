EPCON Frontend Tweaks Plugin
============================

Purpose
-------
Lightweight InvenTree plugin that injects CSS to hide selected navigation/help links (Documentation, About, Getting Started) without forking the frontend.

Installation
------------
1. Clone or add directly via pip from git:
   pip install git+https://github.com/EQUA-AI/epcon-frontend.git

2. Ensure plugin is discovered (entry point "inventree_plugins"). If using a container, restart the backend service (e.g. gunicorn) after installation.

3. Enable plugin in InvenTree Admin > Plugins and set "Active" to True.

4. Hard refresh the browser (Ctrl+Shift+R / Cmd+Shift+R) to clear cached CSS.

Local Development
-----------------
pip install -e .

Packaging Notes
---------------
- Uses PEP 621 metadata in pyproject.toml
- MANIFEST.in ensures CSS assets are included
- setup.py is optional with pyproject; retained only if needed for legacy tooling (currently absent)

Future Extensions
-----------------
- Add selectors list setting for user-managed hides
- Theme adjustments (color, font-size overrides)
- Conditional hide based on user role

Uninstall
---------
pip uninstall epcon-frontend

License
-------
MIT