#!/usr/bin/env python3
"""Responsive and keyboard-accessibility smoke tests for MANZO AI navigation."""
from playwright.sync_api import sync_playwright

ORIGIN='http://127.0.0.1:8765/manzo-ai'
MOBILE=[
 ('it/','it'),('es/','es'),('en/','en'),
 ('it/academy/','it'),('it/risorse/','it'),
 ('en/academy/','en'),('es/academia/','es'),
 ('it/video-e-slide/prompt-engineering/','it')
]
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        for width in (320,390,430):
            page=browser.new_page(viewport={'width':width,'height':812},is_mobile=True,has_touch=True)
            try:
                for path,lang in MOBILE:
                    response=page.goto(f'{ORIGIN}/{path}',wait_until='domcontentloaded')
                    assert response is not None and response.status==200, (width,path)
                    portal=page.locator('.manzo-mobile-portal')
                    menu=page.locator('.manzo-mobile-toggle')
                    assert portal.is_visible(),('Portal link absent',width,path)
                    assert menu.is_visible(),('Menu trigger absent',width,path)
                    assert portal.get_attribute('href')=='/manzo-ai/',('Wrong portal URL',width,path)
                    assert menu.get_attribute('aria-expanded')=='false',(width,path,'initial state')
                    assert page.locator('.manzo-mobile-bar').count()==1,(width,path)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'), ('horizontal overflow',width,path,page.evaluate('document.documentElement.scrollWidth'))
                    menu.click()
                    assert menu.get_attribute('aria-expanded')=='true',(width,path,'open state')
                    page.locator('.manzo-mobile-drawer').wait_for(state='visible',timeout=4000)
                    assert page.locator('.manzo-mobile-quick-portal').get_attribute('href')=='/manzo-ai/'
                    assert page.locator('.manzo-mobile-lang-link').count()==3
                    assert page.locator('.manzo-mobile-drawer').get_attribute('aria-hidden')=='false'
                    page.keyboard.press('Escape')
                    assert menu.get_attribute('aria-expanded')=='false',(width,path,'Esc close')
                    assert page.locator('.manzo-mobile-drawer').get_attribute('aria-hidden')=='true'
                    page.locator('.manzo-mobile-drawer').wait_for(state='hidden',timeout=4000)
                    assert page.evaluate('document.documentElement.style.overflow')=='',(width,path,'scroll lock')
                response=page.goto(f'{ORIGIN}/',wait_until='domcontentloaded')
                assert response.status==200
                assert page.locator('a[href="/manzo-ai/it/"]').count()>0
                assert page.locator('a[href="/manzo-ai/es/"]').count()>0
                assert page.locator('a[href="/manzo-ai/en/"]').count()>0
            finally:
                page.close()
        desktop=browser.new_page(viewport={'width':1280,'height':900})
        for path in ('it/','en/academy/','it/risorse/'):
            desktop.goto(f'{ORIGIN}/{path}',wait_until='domcontentloaded')
            assert desktop.locator('.manzo-mobile-bar').is_hidden(),('Mobile bar visible on desktop',path)
            assert desktop.locator('.rail').is_visible(),('Desktop sidebar absent',path)
            assert desktop.locator('.manzo-global-home[href="/manzo-ai/"]').count()==1,('No central portal in desktop sidebar',path)
        print('MANZO AI mobile nav: 8 page types × 3 small widths; portal; drawer, Escape, languages, overflow and desktop checks PASSED.')
    finally:
        browser.close()
