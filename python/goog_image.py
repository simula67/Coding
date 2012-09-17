from BeautifulSoup import BeautifulSoup
import urllib2
import sys
def getImagesFromGoogle(keyword):
    images = []
    url = """http://images.google.com/images?q=%s&hl=en&safe=off&biw=1280&bih=865&gbv=2&tbs=isch:1,isz:m&source=lnt&sa=X&ei=sIWjTN2cGcX_lgecr4WZAw&ved=0CAgQpwU""" % (keyword.replace(' ', '+'))
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 ( .NET CLR 3.5.30729)')
    data = opener.open(request).read()
    soup = BeautifulSoup(data)
    span = soup.findAll('span', {'class':'rg_ctlv'})[0]
    links = span.findAll('a', href=True)
    for link in links:
        images.append(link['href'].split('=')[1].split('&')[0])
    return images

print getImagesFromGoogle("lion");
