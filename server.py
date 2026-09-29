from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, io
try:
    import qrcode
except ImportError:
    qrcode = None

ROOT = Path(__file__).parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        path=urlparse(self.path)
        if path.path == '/qr':
            payload=parse_qs(path.query).get('data',['{}'])[0]
            if qrcode:
                qr=qrcode.QRCode(version=None, box_size=8, border=3)
                qr.add_data(payload); qr.make(fit=True)
                img=qr.make_image(fill_color='black',back_color='white').convert('RGB')
                out=io.BytesIO(); img.save(out,format='PNG'); data=out.getvalue()
                self.send_response(200); self.send_header('Content-Type','image/png'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data); return
            self.send_error(503,'QR support unavailable. Install qrcode and pillow.')
            return
        super().do_GET()

if __name__=='__main__':
    print('FeedCare AI running at http://localhost:8000')
    print('Keep this window open while using the prototype.')
    ThreadingHTTPServer(('localhost',8000),Handler).serve_forever()
