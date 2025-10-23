from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin

class HideLinksPlugin(SettingsMixin, InvenTreePlugin):
    """EPCON Frontend tweaks plugin.

    Provides UI cosmetic adjustments, currently hiding Documentation / About / Getting Started links
    without rebuilding the bundled frontend. Additional tweaks can be added here later.
    """

    NAME = "EpconFrontend"
    SLUG = "epcon-frontend"
    TITLE = "EPCON Frontend Tweaks"
    DESCRIPTION = "Enterprise UI tweaks: hide Documentation / About / Getting Started links (extensible)." 
    VERSION = "0.1.0"
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
        """Return CSS assets to load when plugin is active."""
        if self.get_setting('ACTIVE'):
            return ['css/hide-links.css']
        return []
