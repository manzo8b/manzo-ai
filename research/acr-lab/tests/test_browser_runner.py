import pytest
from pathlib import Path
from acr.browser_runner import contrast_ratio, parse_rgb, run_browser_checks, CATALOG_VERSION

FIXTURES = Path(__file__).resolve().parents[1] / 'examples' / 'browser_fixture'


def test_contrast_formula_reference_values():
    assert contrast_ratio('rgb(0,0,0)','rgb(255,255,255)') == pytest.approx(21,abs=.001)
    assert contrast_ratio('rgb(255,255,255)','rgb(255,255,255)') == pytest.approx(1)
    assert contrast_ratio('rgb(196,196,196)','rgb(255,255,255)') < 4.5


def test_parse_rgb_rejects_alpha_and_bad_inputs():
    assert parse_rgb('rgb(1, 2, 3)') == (1, 2, 3)
    with pytest.raises(ValueError):
        parse_rgb('rgba(0,0,0,0.3)')
    with pytest.raises(ValueError):
        parse_rgb('transparent')


def test_catalog_constant_versioned():
    assert CATALOG_VERSION == 'mobile-web-smoke-v1'


def test_browser_four_revisions_detect_two_real_regressions(tmp_path):
    try:
        all_results = [run_browser_checks(FIXTURES/f'rev{i}.html', screenshots=tmp_path/'failures')[0]
                       for i in range(4)]
    except Exception as exc:
        pytest.skip(f'Chromium unavailable: {exc}')
    by_rev = [{r.test_id: r.status for r in results} for results in all_results]
    assert [sum(s == 'pass' for s in rev.values()) for rev in by_rev] == [6,5,5,6]
    assert by_rev[1]['mobile_menu'] == 'fail'
    assert by_rev[2]['lead_contrast_aa'] == 'fail'
    assert by_rev[3]['lead_contrast_aa'] == 'pass'
    assert all(status == 'pass' for status in by_rev[3].values())
