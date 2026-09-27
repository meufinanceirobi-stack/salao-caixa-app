import base64, pathlib
here = pathlib.Path(__file__).parent
html = (here / 'ak-reels.template.html').read_text(encoding='utf-8')
html = html.replace('__FONT__', base64.b64encode((here / 'Montserrat.ttf').read_bytes()).decode())
html = html.replace('__LOGO__', base64.b64encode((here / 'logo-ak.png').read_bytes()).decode())
(here.parent / 'ak-reels.html').write_text(html, encoding='utf-8')
print('ok', len(html))
