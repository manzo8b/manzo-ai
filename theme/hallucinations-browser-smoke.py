#!/usr/bin/env python3
"""Responsive and interactive smoke test for MANZO AI hallucinations course.
Run against http://127.0.0.1:8765/manzo-ai/ after full editorial/SEO overlay.
"""
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE='http://127.0.0.1:8765/manzo-ai/'
ROUTES={
    'it':'it/impara/allucinazioni-ai-verificabilita/',
    'en':'en/learn/ai-hallucinations-verification/',
    'es':'es/aprende/alucinaciones-ia-verificacion/'
}
WORDS=[
    ('PROVENIENZA',0,5,0,1),('VERIFICABILITA',0,8,1,0),
    ('RISCHIO',2,8,0,1),('FONTE',4,8,0,1),
    ('TRACCIABILITA',6,5,0,1),('PROBATORIO',8,5,0,1),
    ('CONTROLLO',10,2,0,1),('CONTESTO',12,5,0,1)
]
def assert_page(page,locale,mobile):
    page.goto(urljoin(BASE,ROUTES[locale]),wait_until='load',timeout=30000)
    assert page.locator('h1').count()==1,locale
    assert page.locator('.hx-module').count()==5,locale
    assert page.locator('.hx-case').count()==10,locale
    assert page.locator('.hx-source').count()==8,locale
    assert page.locator('.hx-cell input').count()>60,locale
    assert page.locator('#hx-quiz-position').inner_text().strip()=='1 / 10',locale
    assert page.locator('.hx-q-options label').count()>=2,locale
    width=page.evaluate('document.documentElement.scrollWidth')
    viewport=page.evaluate('window.innerWidth')
    assert width<=viewport+2,f'{locale} mobile={mobile} horizontal overflow: {width}>{viewport}'
    if mobile:
        assert page.locator('.hx-orbit').is_visible(),locale
    page.locator('.hx-case').first.locator('textarea').fill('This analysis identifies missing source documentation.')
    assert page.locator('.hx-case').first.locator('.hx-reveal').is_enabled(),locale
    page.locator('.hx-case').first.locator('.hx-reveal').click()
    assert page.locator('.hx-case').first.locator('.hx-case-feedback').is_visible(),locale
    page.locator('.hx-q-options input').nth(1).check()
    page.locator('#hx-quiz-check').click()
    assert page.locator('#hx-quiz-feedback').is_visible(),locale
    page.locator('#hx-quiz-next').click()
    assert page.locator('#hx-quiz-position').inner_text().strip()=='2 / 10',locale

def assert_crossword(page):
    # Complete all intersections with the same character in every applicable answer.
    expected={}
    for word,r,c,dr,dc in WORDS:
        for i,ch in enumerate(word):
            key=(r+dr*i,c+dc*i)
            assert key not in expected or expected[key]==ch
            expected[key]=ch
    for (r,c),letter in expected.items():
        page.locator(f'#hx-cross-grid input[data-r="{r}"][data-c="{c}"]').fill(letter)
    page.locator('#hx-cross-check').click()
    assert 'correttamente' in page.locator('#hx-cross-status').inner_text().lower(), 'Crossword did not validate'

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
    for locale in ROUTES:
        page=browser.new_page(viewport={'width':1366,'height':850})
        assert_page(page,locale,False)
        if locale=='it':
            assert_crossword(page)
        page.close()
    for locale in ROUTES:
        page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,device_scale_factor=2)
        assert_page(page,locale,True)
        page.close()
    browser.close()
print('PASS: IT/EN/ES course, cases, quiz, crossword, desktop and mobile layout.')
