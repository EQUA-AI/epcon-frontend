try:
    from plugin import InvenTreePlugin
    from plugin.mixins import SettingsMixin
except ModuleNotFoundError:
    # Fallback stubs for environments where InvenTree isn't installed (e.g., packaging introspection)
    class SettingsMixin:  # type: ignore
        pass
    class InvenTreePlugin:  # type: ignore
        pass

class EpconFrontend(SettingsMixin, InvenTreePlugin):
    """EPCON Frontend tweaks plugin.

    Provides UI cosmetic adjustments, currently hiding Documentation / About / Getting Started links
    without rebuilding the bundled frontend. Additional tweaks can be added here later.
    """

    NAME = "EpconFrontend"
    SLUG = "epcon-frontend"
    TITLE = "EPCON Frontend Tweaks"
    DESCRIPTION = "Enterprise UI tweaks: hide Documentation / About / Getting Started links (extensible)." 
    VERSION = "0.1.3"
    AUTHOR = "EPCON"
    WEBSITE = ""
    LICENSE = "MIT"

    SETTINGS = {
        'ACTIVE': {
            'name': 'Active',
            'description': 'Enable hiding of UI help links',
            'validator': bool,
            'default': True,
        },
    }

    def load_css(self):
        """Return CSS assets to load when plugin is active.

        Avoid calling get_setting() if it is not available yet (e.g. raw import
        outside full InvenTree plugin initialization) to prevent AttributeError.
        """
        # Prefer real get_setting if present, otherwise use SETTINGS defaults.
        active = None
        if hasattr(self, 'get_setting') and callable(getattr(self, 'get_setting')):
            try:
                active = self.get_setting('ACTIVE')
            except Exception:
                active = None
        if active is None:
            active = self.SETTINGS.get('ACTIVE', {}).get('default', True)
        if active:
            return ['css/hide-links.css']
        return []

    def load_js(self):  # Optional refine: InvenTree will include if plugin framework supports load_js
        active = self.SETTINGS.get('ACTIVE', {}).get('default', True)
        if hasattr(self, 'get_setting') and callable(getattr(self, 'get_setting')):
            try:
                active = self.get_setting('ACTIVE')
            except Exception:
                pass
        if active:
            return ['js/hide-links.js']
        return []

    # Fallback get_setting only if missing from mixin (do not override real one)
    if not hasattr(SettingsMixin, 'get_setting'):
        def get_setting(self, key, default=None):  # type: ignore
            return self.SETTINGS.get(key, {}).get('default', default)
