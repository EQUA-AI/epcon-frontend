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
    VERSION = "0.1.4"
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

    # Hook to perform setup actions once plugin is loaded
    def plugin_setup(self):  # Called by InvenTree after plugin is instantiated
        """Attempt to inject our CSS/JS tags directly into the resolved SPA index.html template if override mechanism did not work.

        This is a pragmatic fallback because the React SPA currently resolves `web/index.html` only from the core app template directory, ignoring plugin template overrides.
        We patch the file in-place (idempotently) to include our assets before `</head>` so the browser will request them.
        """
        try:
            from django.template.loader import get_template
            from django.conf import settings
            import os
            template_name = "web/index.html"
            t = get_template(template_name)
            origin = getattr(t, 'template', getattr(t, 'origin', None))
            # Django versions differ; we captured earlier path via t.template.origin.name
            path = None
            try:
                path = t.template.origin.name  # type: ignore[attr-defined]
            except Exception:
                try:
                    path = t.origin.name  # type: ignore[attr-defined]
                except Exception:
                    pass
            if not path or not os.path.isfile(path):
                self.logger.info(f"[epcon-frontend] Could not determine path for template '{template_name}'. Skipping index patch.")
                return

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            css_tag = f'<link rel="stylesheet" href="/static/plugins/epcon-frontend/css/hide-links.css?v={VERSION}" />'
            js_tag = f'<script src="/static/plugins/epcon-frontend/js/hide-links.js?v={VERSION}"></script>'
            marker = 'epcon-frontend/css/hide-links.css'

            if marker in content:
                # Already patched for current or prior version
                self.logger.debug("[epcon-frontend] index.html already contains injection markers; no patch applied.")
                return

            if '</head>' not in content:
                self.logger.warning("[epcon-frontend] index.html missing </head>; cannot inject assets.")
                return

            new_content = content.replace('</head>', f'    {css_tag}\n    {js_tag}\n</head>')
            backup_path = f"{path}.bak_epcon_frontend"
            try:
                if not os.path.exists(backup_path):
                    with open(backup_path, 'w', encoding='utf-8') as b:
                        b.write(content)
            except Exception:
                # Non-fatal
                pass
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.logger.info(f"[epcon-frontend] Injected hide-links assets into {path}")

            # Attempt to clear template caches so change is picked up without full restart
            try:
                from django.template import engines
                for eng in engines.all():
                    loaders = getattr(eng.engine, 'template_loaders', [])
                    for loader in loaders:
                        reset = getattr(loader, 'reset', None)
                        if callable(reset):
                            reset()
                self.logger.debug("[epcon-frontend] Requested template loader cache reset.")
            except Exception:
                pass
        except Exception as exc:
            self.logger.warning(f"[epcon-frontend] Failed to patch index.html: {exc}")
