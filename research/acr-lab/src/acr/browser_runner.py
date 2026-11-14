"""Offline Chromium/Playwright acceptance suite for a mobile web UI.

Tests run against real browser-rendered HTML. This suite is deliberately narrow:
it is NOT axe-core, Lighthouse, or a full WCAG accessibility audit.
No AI model calls. No fixture checks are called proof of ACR efficacy.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import os
import re
import shutil
from typing import Callable


CATALOG_VERSION = 'mobile-web-smoke-v1'
VIEWPORT = {'width': 390, 'height': 844}


@dataclass(frozen=True)
class BrowserTestResult:
    test_id: str
    status: str
    detail: str


def available_chromium() -> str | None:
    """Prefer user-supplied executable, then system Chromium, else Playwright cache."""
    executable = os.environ.get('ACR_CHROMIUM_BIN')
    if executable:
        if not Path(executable).is_file():
            raise FileNotFoundError(f'ACR_CHROMIUM_BIN points to missing browser: {executable}')
        return executable
    return shutil.which('chromium') or shutil.which('google-chrome') or None


def parse_rgb(css: str) -> tuple[int, int, int]:
    """Extract numeric RGB from computed CSS rgb()/rgba(); alpha must be opaque."""
    rgb = re.fullmatch(r'rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)(?:\s*[,/]\s*([\d.]+))?\s*\)', css.strip())
    if not rgb:
        raise ValueError(f'Unsupported CSS color: {css!r}')
    if rgb[4] is not None and float(rgb[4]) != 1:
        raise ValueError('Semi-transparent CSS colors require compositing and are unsupported')
    values = tuple(map(int, rgb.group(1, 2, 3)))
    if any(v < 0 or v > 255 for v in values):
        raise ValueError('Invalid RGB channel')
    return values


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = map(channel, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    a = relative_luminance(parse_rgb(foreground))
    b = relative_luminance(parse_rgb(background))
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def _mobile_navigation(page) -> str:
    button = page.get_by_role('button', name='Apri menu')
    if not button.is_visible():
        raise AssertionError('Mobile menu button not visible')
    if button.get_attribute('aria-expanded') != 'false':
        raise AssertionError('Initial aria-expanded is not false')
    button.click()
    if button.get_attribute('aria-expanded') != 'true':
        raise AssertionError('aria-expanded did not update to true')
    if not page.locator('#primary-menu').is_visible():
        raise AssertionError('Navigation remained hidden after click')
    return 'Menu opens and exposes its state'


def _lead_contrast(page) -> str:
    colors = page.locator('#hero-lead').evaluate('''el => ({
       foreground: getComputedStyle(el).color,
       background: getComputedStyle(el).backgroundColor
    })''')
    ratio = contrast_ratio(colors['foreground'], colors['background'])
    if ratio < 4.5:
        raise AssertionError(f'Lead contrast {ratio:.2f}:1 is below targeted WCAG AA 4.5:1')
    return f'Lead contrast {ratio:.2f}:1 >= 4.5:1 (targeted check only)'


def _form_validation(page) -> str:
    field = page.get_by_label('Email')
    field.fill('bad-address')
    page.get_by_role('button', name='Invia').click()
    if field.evaluate('(el) => el.validity.valid'):
        raise AssertionError('Invalid email accepted')
    if page.locator('#form-status').inner_text().strip():
        raise AssertionError('Invalid email triggered success message')
    field.fill('test@example.org')
    page.get_by_role('button', name='Invia').click()
    if page.locator('#form-status').inner_text().strip() != 'Richiesta registrata':
        raise AssertionError('Valid email did not trigger local confirmation')
    return 'Browser validation rejects malformed email and accepts a valid value'


def _no_horizontal_overflow(page) -> str:
    metrics = page.evaluate('''() => ({
       scroll: document.documentElement.scrollWidth,
       client: document.documentElement.clientWidth
    })''')
    if metrics['scroll'] > metrics['client'] + 1:
        raise AssertionError(f'Mobile overflow: {metrics["scroll"]} > {metrics["client"]}')
    return f'No overflow at {VIEWPORT["width"]}px viewport'


def _headings_clean(page) -> str:
    values = page.locator('h1,h2').all_inner_texts()
    if not values or any(v.rstrip().endswith(('.', '!', '?')) for v in values):
        raise AssertionError('Empty headings or forbidden final punctuation')
    return 'Main headings have no final punctuation'


def _semantic_landmarks(page) -> str:
    if page.locator('main').count() != 1 or page.locator('nav[aria-label]').count() != 1:
        raise AssertionError('Expected one main and one navigation landmark')
    if page.get_by_label('Email').count() != 1:
        raise AssertionError('Email input is missing an accessible label')
    return 'Main/navigation landmarks and labeled email field present'


CHECKS: dict[str, Callable] = {
    'mobile_menu': _mobile_navigation,
    'lead_contrast_aa': _lead_contrast,
    'email_form_validation': _form_validation,
    'mobile_no_overflow': _no_horizontal_overflow,
    'headings_no_period': _headings_clean,
    'semantic_landmarks': _semantic_landmarks,
}


def browser_version() -> str:
    """Resolve Chromium version before calculating an immutable run configuration hash."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        executable = available_chromium()
        opts = {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
        if executable:
            opts['executable_path'] = executable
        browser = playwright.chromium.launch(**opts)
        try:
            return browser.version
        finally:
            browser.close()


def run_browser_checks(document: Path, *, screenshots: Path | None = None) -> tuple[list[BrowserTestResult], str]:
    """Run identical test catalog against one immutable local HTML fixture.

    Returns six pass/fail statuses + the actual installed Chromium version.
    Fails loudly if no browser can start; never invents passing results.
    """
    from playwright.sync_api import sync_playwright

    document = Path(document).resolve()
    if not document.is_file():
        raise FileNotFoundError(document)
    if screenshots:
        screenshots.mkdir(parents=True, exist_ok=True)
    results: list[BrowserTestResult] = []
    with sync_playwright() as playwright:
        executable = available_chromium()
        opts = {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
        if executable:
            opts['executable_path'] = executable
        browser = playwright.chromium.launch(**opts)
        try:
            for name, check in CHECKS.items():
                context = browser.new_context(viewport=VIEWPORT, device_scale_factor=1, is_mobile=True,
                                              has_touch=True, java_script_enabled=True, service_workers='block',
                                              accept_downloads=False)
                page = context.new_page()
                page.route('**/*', lambda route: route.abort())  # prohibit external HTTP(S) fetches
                # Bound waits for deliberate broken UI fixtures; otherwise a single
                # missing element may stall the entire offline pilot for 30 seconds.
                page.set_default_timeout(2000)
                page.set_default_navigation_timeout(5000)
                try:
                    page.set_content(document.read_text(encoding='utf-8'), wait_until='load')
                    details = check(page)
                    results.append(BrowserTestResult(name, 'pass', details))
                except Exception as exc:
                    details = f'{type(exc).__name__}: {str(exc)[:240]}'
                    results.append(BrowserTestResult(name, 'fail', details))
                    if screenshots:
                        page.screenshot(path=str(screenshots / f'{document.stem}_{name}.png'), full_page=True)
                finally:
                    context.close()
            version = browser.version
        finally:
            browser.close()
    return results, version


def as_json(results: list[BrowserTestResult]) -> list[dict]:
    return [asdict(result) for result in results]
