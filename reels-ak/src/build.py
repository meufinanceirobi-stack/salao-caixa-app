import base64, pathlib, sys
here = pathlib.Path(__file__).parent
name = sys.argv[1] if len(sys.argv) > 1 else 'ak-reels'
html = (here / f'{name}.template.html').read_text(encoding='utf-8')
html = html.replace('__FONT__', base64.b64encode((here / 'Montserrat.ttf').read_bytes()).decode())
html = html.replace('__LOGO__', base64.b64encode((here / 'logo-ak.png').read_bytes()).decode())
(here.parent / f'{name}.html').write_text(html, encoding='utf-8')
print('ok', name, len(html))
