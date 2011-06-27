import sys
import os.path

paths = (os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'xhtml2pdf'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'libs/pyPdf'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'libs/html5lib/src'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'libs/reportlab/src')
)

for p in paths:
    if not p in sys.path:
        sys.path.append(p)
