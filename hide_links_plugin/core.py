"""Epcon Frontend Plugin core.

Clean re-write after patch corruption. Provides optional runtime injection of CSS/JS to hide help links.
"""

try:
    from plugin import InvenTreePlugin
    from plugin.mixins import SettingsMixin
except ModuleNotFoundError:  # pragma: no cover - packaging fallback
    class SettingsMixin:  # type: ignore
        pass
    class InvenTreePlugin:  # type: ignore
        pass


class EpconFrontend(SettingsMixin, InvenTreePlugin):
    NAME = "EpconFrontend"
    SLUG = "epcon-frontend"
    TITLE = "EPCON Frontend Tweaks"
    DESCRIPTION = "Enterprise UI tweaks: hide Documentation / About / Getting Started links (extensible)."
    VERSION = "0.1.5"
    AUTHOR = "EPCON"
    WEBSITE = ""
    LICENSE = "MIT"

    SETTINGS = {
        'ACTIVE': {
            'name': 'Active',
            'description': 'Enable hiding of UI help links',
            'validator': bool,
            'default': True,
        }
    }
    _ACTIVE_DEFAULT = True

    def __init__(self):
        super().__init__()
        # Auto-run plugin_setup (idempotent)
        try:
            self.plugin_setup()
        except Exception as exc:  # pragma: no cover - runtime safety
            try:
                self.logger.warning(f"[epcon-frontend] auto plugin_setup failed: {exc}")
            except Exception:
                pass

    # Provide fallback get_setting only if missing (avoid clobbering real one)
    if not hasattr(SettingsMixin, 'get_setting'):
        def get_setting(self, key, default=None):  # type: ignore
            return self.SETTINGS.get(key, {}).get('default', default)

    def _is_active(self) -> bool:
        try:
            return bool(self.get_setting('ACTIVE')) if hasattr(self, 'get_setting') else self._ACTIVE_DEFAULT
        except Exception:
            return self._ACTIVE_DEFAULT

    def load_css(self):
        return ['css/hide-links.css'] if self._is_active() else []

    def load_js(self):
        return ['js/hide-links.js'] if self._is_active() else []

    def plugin_setup(self):
        """Patch index.html directly to inject assets if template override not applied.

        Idempotent: skips if marker already present. Falls back silently if template not resolvable.
        """
        import os
        try:
            from django.template.loader import get_template
        except Exception:
            return  # Django not available in this context

        template_name = "web/index.html"
        try:
            t = get_template(template_name)
        except Exception as exc:
            try:
                self.logger.debug(f"[epcon-frontend] get_template failed: {exc}")
            except Exception:
                pass
            return

        path = None
        for attr_chain in ["template.origin.name", "origin.name"]:
            obj = t
            try:
                for part in attr_chain.split('.'):
                    obj = getattr(obj, part)
                if isinstance(obj, str):
                    path = obj
                    break
            except Exception:
                continue

        if not path or not os.path.isfile(path):
            try:
                self.logger.debug(f"[epcon-frontend] No file path for {template_name}; skipping patch")
            except Exception:
                pass
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as exc:
            try:
                self.logger.debug(f"[epcon-frontend] Failed reading index.html: {exc}")
            except Exception:
                pass
            return

        marker = 'epcon-frontend/css/hide-links.css'
        if marker in content:
            return  # already injected
        if '</head>' not in content:
            return

        css_tag = f'<link rel="stylesheet" href="/static/plugins/epcon-frontend/css/hide-links.css?v={self.VERSION}" />'
        js_tag = f'<script src="/static/plugins/epcon-frontend/js/hide-links.js?v={self.VERSION}"></script>'
        new_content = content.replace('</head>', f'    {css_tag}\n    {js_tag}\n</head>')

        # Backup original once
        backup_path = f"{path}.bak_epcon_frontend"
        try:
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as b:
                    b.write(content)
        except Exception:
            pass

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            try:
                self.logger.info(f"[epcon-frontend] Injected hide-links assets into {path}")
            except Exception:
                pass
        except Exception as exc:
            try:
                self.logger.warning(f"[epcon-frontend] Failed writing patched index.html: {exc}")
            except Exception:
                pass
