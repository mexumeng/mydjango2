__author__ = "xumeng"
__date__ = "2018/8/14 17"
from urllib import request


url = 'http://vd3.bdstatic.com/mda-ihd6ap4hvduu1nii/sc/mda-ihd6ap4hvduu1nii.mp4'
req = request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',)
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))