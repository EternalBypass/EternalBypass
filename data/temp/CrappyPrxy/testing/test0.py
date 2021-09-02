import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import os
import time
script_fix = 0
css_fix = 0
img_fix = 0
end=''
start=''
def fixURL(url):
    global start
    start = time.time()

    global script_fix
    global end
    global css_fix
    global img_fix
    # URL of the web page you want to extract
    #url = "http://discord.com"

    # initialize a session
    session = requests.Session()
    # set the User-agent as a regular browser
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    # get the HTML content
    append_html = session.get(url).content

    # parse HTML using beautiful soup
    soup = bs(append_html, "html.parser")
    # get the JavaScript files
    script_files = []
    #append_html = requests.get(url)
    print("[   ]")
    #append_html = append_html.content()
    for script in soup.find_all("script"):
        if script.attrs.get("src"):


            script_url = urljoin(url, script.attrs.get("src"))
            script_files.append(script_url)
            search_script = script_url.split(url+'/')
            search_script = search_script[1]

            if search_script not in script_files:
                print('downloading '+url+'/'+search_script)
                #sh_fix = open('fix.sh', w)
                search_f = search_script.split('/')
                search_c = search_script.count('/')
                search_r = search_f[search_c]
                search_script2 = search_script.replace(search_r, '')
                try:
                    os.mkdir(search_script2)
                except Exception as er:
                    pass
                if url not in script_url:
                    re = url+script_url
                    re = requests.get(re)
                    re = re.content
                    f = open(search_script, 'w')
                    f.write(re.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'").strip("'"))
                    f.flush()
                    f.close()
                    re =''


                    e = open('currentTempDirs', 'a')
                    e.write('\n'+search_script)
                    e.flush()
                    e.close()
                else:
                    re = script_url
                    re = requests.get(re)
                    re = re.content
                    f = open(search_script, 'w')
                    f.write(str(re).replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'").strip("'"))
                    f.flush()
                    f.close()
                    re =''
                    #s = script_url.split('/')
                    #s = s[1]
                    e = open('currentTempDirs', 'a')
                    e.write('\n'+search_script)
                    e.flush()
                    e.close()
                    append_html = str(append_html).replace(url+search_script, search_script)
                script_fix += 1
                script_files.append(search_script)

    # get the CSS files
    css_files = []
    print('[#  ]')
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            #if url not in css.attrs.get("href"):
            css_url = urljoin(url, css.attrs.get("href"))
            css_files.append(css_url)
            search_css = str(css_url).split(url+'/')

            search_css = search_css[1]

            if search_css not in css_files:
                print('downloading '+url+'/'+search_css)
                search_f = search_css.split('/')
                search_c = search_css.count('/')
                search_r = search_f[search_c]
                search_css2 = search_css.replace(search_r, '')
                try:
                    os.mkdir(search_css2)
                except Exception as er:
                    pass
                if url not in css_url:
                    re = url+css_url
                    re = requests.get(re)
                    re = re.content
                    f = open(search_css, 'w')
                    f.write(re.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'").strip("'"))
                    f.flush()
                    f.close()
                    re =''
                    e = open('currentTempDirs', 'a')
                    e.write('\n'+search_css)
                    e.flush()
                    e.close()
                else:
                    re = css_url
                    re = requests.get(re)
                    re = re.content
                    f = open(search_css, 'w')
                    f.write(str(re).replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'").strip("'"))
                    f.flush()
                    f.close()
                    re =''
                    e = open('currentTempDirs', 'a')
                    e.write('\n'+search_css)
                    e.flush()
                    e.close()

                    append_html = str(append_html).replace(url+search_css, search_css)
                css_fix += 1
                css_files.append(search_css)
    print('[## ]')
    img_files = []
    for img in soup.find_all('img'):
        #img_url = link.get('image-src')
            # if the tag has the attribute 'src'
        #print('soup found img')
#        if url not in img.get('src'):
        img_url = urljoin(url, img.get('src'))
            #print(img.get('image-src'))

        search_img = img_url.split(url+'/')
        search_img = search_img[1]
        #print('downloading '+url+'/'+search_css)
        #print(search_img)
        #print(str(search_img)+'    '+str(img_files))
        if search_img not in img_files:
            #print(search_img+' is not in '+str(img_files))
            print('downloading '+url+'/'+search_img)
            #print('soup replacing '+search_img+' with '+img_ur
            search_f = search_img.split('/')
            search_c = search_img.count('/')
            search_r = search_f[search_c]
            search_img2 = search_img.replace(search_r, '')
            try:
                os.mkdir(search_img2)
            except Exception as er:
                pass
            if url not in img_url:
                re = url+img_url
                re = requests.get(re)
                re = re.content
                f = open(search_img, 'wb')
                f.write(re)
                f.flush()
                f.close()
                re =''
                e = open('currentTempDirs', 'a')
                e.write('\n'+search_img)
                e.flush()
                e.close()
            else:
                re = img_url
                re = requests.get(re)
                re = re.content
                f = open(search_img, 'wb')
                f.write(re)
                f.flush()
                f.close()
                re =''
                e = open('currentTempDirs', 'a')
                e.write('\n'+search_img)
                e.flush()
                e.close()
                append_html = str(append_html).replace(url+search_img, search_img)
            img_fix += 1
            img_files.append(search_img)
    append_html = append_html.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
    #print(img_files)
    print('[###]')
    end = time.time()
    return append_html
html = fixURL('http://discord.com')
writeHtml = open('discord.html', 'w')
#html = html.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
writeHtml.write(str(html))
writeHtml.flush()
writeHtml.close()

print('Downloaded '+str(script_fix)+' js files, '+str(css_fix)+' css files, and '+str(img_fix)+' img files in '+str(end-start)+' seconds.')
