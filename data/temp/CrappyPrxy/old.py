import os
from flask import Flask, request, render_template
import datetime
import requests
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
app = Flask(__name__, static_url_path='/static')
import psutil
import os
#hosttorequest = ''
proc_url =''
host=''
current_host=''
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
script_fix = 0
css_fix = 0
img_fix = 0
fixURLbool = False
import time
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
    #print(url+'\n')
    append_html = session.get(url).content

    # parse HTML using beautiful soup
    soup = bs(append_html, "html.parser")
    # get the JavaScript files
    script_files = []
    #append_html = requests.get(url)
    print("[   ]")
    #append_html = append_html.content()
    for script in soup.find_all("script"):
        process = psutil.Process(os.getpid())#check and handle memory pressure
        currentUsage = (process.memory_info().rss)
        if currentUsage >= 1073721824:  #little less than the 1 gb hard limit
            print('WARN: MEMORY PRESSURE CRITICAL')
            gc.collect()
            end='' #trying to clear as many variables as possible
            start=''
            re=''
            f=''
            if currentUsage >= 1073721824: #Exit gracefully by clearing current failed directory to prevent corruption.
                try:
                    os.remove(search_script2)
                except Exception:
                    pass
                raise MemoryError('Memory ran out, exited gracefully and killed self.')
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
                    os.mkdir('static/'+search_script2)

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
                    append_html = str(append_html).replace(url+search_script, search_script).replace('/'+search_script2, '/static/'+search_script2)
                script_fix += 1
                script_files.append(search_script)



    # get the CSS files

    css_files = []
    print('[#  ]')
    for css in soup.find_all("link"):
        process = psutil.Process(os.getpid())#check and handle memory pressure
        currentUsage = (process.memory_info().rss)
        if currentUsage >= 1073721824:  #little less than the 1 gb hard limit
            print('WARN: MEMORY PRESSURE CRITICAL')
            gc.collect()
            end='' #trying to clear as many variables as possible
            start=''
            re=''
            f=''
            if currentUsage >= 1073721824: #Exit gracefully by clearing current failed directory to prevent corruption.
                try:
                    os.remove(search_css2)
                except Exception:
                    pass
                raise MemoryError('Memory ran out, exited gracefully and killed self.')
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
                    os.mkdir('static/'+search_css2)

                except Exception as er:
                    pass
                if url not in css_url:
                    if '.ico' in css_url:

                        print('WARN: BUGFIX1: IMG FILE REGARDED AS CSS, WRTITING '+css_url+' AS BINARY')
                        try:
                            re = url+css_url
                            re = requests.get(re)
                            re = re.content
                        except Exception:

                            re = 'http:'+url+css_url
                            re = requests.get(re)
                            re = re.content
                        f = open(search_css, 'wb')
                        f.write(re)
                        f.flush()
                        f.close()
                    else:
                        re = url+css_url
                        re = requests.get(re)
                        re = re.content
                        f = open(search_css.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'").strip("'"), 'w')

                        f.write(re)
                        f.flush()
                        f.close()
                    re =''
                    e = open('currentTempDirs', 'a')
                    e.write('\n'+search_css)
                    e.flush()
                    e.close()
                else:
                    if '.ico' in css_url:
                        print('WARN: BUGFIX1: IMG FILE REGARDED AS CSS, WRTITING '+css_url+' AS BINARY')
                        print(css_url)
                        try:

                            re = css_url
                            #print(re)
                            re = requests.get(re)

                            #re = re.content
                        except Exception:
                            re = 'http:'+css_url
                            #print(re)
                            re = requests.get(re)
                            #re = re.content
                        f = open(search_css, 'wb')
                        f.write(re.content)
                        f.flush()
                        f.close()
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

                    append_html = str(append_html).replace(url+search_css, search_css).replace('/'+search_script2, '/static/'+search_script2)
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
        process = psutil.Process(os.getpid())#check and handle memory pressure
        currentUsage = (process.memory_info().rss)
        if currentUsage >= 1073721824:  #little less than the 1 gb hard limit
            print('WARN: MEMORY PRESSURE CRITICAL')
            gc.collect()
            end='' #trying to clear as many variables as possible
            start=''
            re=''
            f=''
            if currentUsage >= 1073721824: #Exit gracefully by clearing current failed directory to prevent corruption.
                try:
                    os.remove(search_img2)
                except Exception:
                    pass
                raise MemoryError('Couldnt be usefull to the world, used to many resources and committed suicide.')
        if search_img not in img_files:
            #print(search_img+' is not in '+str(img_files))
            print('downloading '+url+'/'+search_img)
            #print('soup replacing '+search_img+' with '+img_ur
            search_f = search_img.split('/')
            search_c = search_img.count('/')
            search_r = search_f[search_c]
            search_img2 = search_img.replace(search_r, '')
            try:
                os.mkdir('static/'+search_img2)
            except Exception as er:
                pass
            if url not in img_url:
                re = url+img_url
                re = requests.get(re)
                re = re.content
                f = open(search_img, 'w')
                f.write(re.replace('\\n', '\n').replace("b'", '').strip("'"))
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
                f = open(search_img, 'w')
                f.write(str(re).replace('\\n', '\n').replace("b'", '').strip("'"))
                f.flush()
                f.close()
                re =''
                e = open('currentTempDirs', 'a')
                e.write('\n'+search_img)
                e.flush()
                e.close()
                append_html = str(append_html).replace(url+search_img, search_img).replace('/'+search_script2, '/static/'+search_script2)
            img_fix += 1
            img_files.append(search_img)
    append_html = append_html.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
    #print(img_files)
    print('[###]')
    end = time.time()
    return append_html
@app.route('/')
def getUrl():
    return render_template('form.html')
url =''
@app.route('/devolopment')
def getUrl2():
    return render_template('form_dev.html')
url2 =''
@app.route('/', methods=HTTP_METHODS)
def root():
    global url
    #feedback = request.form['feedback']
    #feedback_dat = feedback.upper()
    #fed = open('feedback.txt', 'a')
    #fed.write(feedback_dat)
    text = request.form['text']
    url = text
    r = requests.get('http://'+url)
    #logfile = open('currentlog.log', 'a')
    #logfile.write('http://'+url+'/')
    #logfile.flush()
    #logfile.close() #Here for testing.
    #return r.content
    if 'search?' in request.url:
            logfile = open('currentlog.log', 'a')
            logfile.write('\nEXCEPTION DETECTED AS GOOGLE SEARCH.')
            logfile.flush()
            logfile.close()
            goog_proc = request.url
            goog_proc = goog_proc.split("/", 3)
            goog_proc = goog_proc[3]
            goog_proc = goog_proc.split("q=", 1)
            goog_proc = goog_proc[1]
            goog_proc = goog_proc.split("&", 1)
            goog_proc = goog_proc[0]
            goog_proc = 'google.com/search?q='+goog_proc

            r3 = requests.get('http://'+goog_proc)
            logfile = open('currentlog.log', 'a')
            logfile.write('\nHOST:\n'+host)
            logfile.flush()
            logfile.close()
            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM URL AS SEARCH(GOOGLE):\n'+'http://'+goog_proc)
            logfile.flush()
            logfile.close()
            #r3_back = 'http://'+goog_proc

            return r3.content
    else:

        return r.content
#@app.route('/assets/<path:other>')
#def redirect_assets():
    #global url
    #cr = request.url
    #cr = cr.split('.com')
    #cr = cr[1]
    #ie = 'http://'+url+cr
    #ie = requests.get(ie)
    #return ie.content
@app.route('/devolopment', methods=HTTP_METHODS)
def root2():
    global url2
    #feedback = request.form['feedback']
    #feedback_dat = feedback.upper()
    #fed = open('feedback.txt', 'a')
    #fed.write(feedback_dat)

    text2 = request.form['text2']
    url2 = text2
    if request.method == 'POST':
        request.form.getlist('repair_site')
    r2 = fixURL('http://'+url2)
    r2 = r2.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
    logfile = open('currentlog.log', 'a')
    logfile.write('START: session dev\n')
    logfile.write('http://'+url2+'\n')
    logfile.flush()
    logfile.close()
    #Here for testing.
    #request_str = 'http://'+url2
    #return request_str
    if 'search?' in request.url:
            logfile = open('currentlog.log', 'a')
            logfile.write('\nEXCEPTION DETECTED AS GOOGLE SEARCH.')
            logfile.flush()
            logfile.close()
            goog_proc = request.url
            goog_proc = goog_proc.split("/", 3)
            goog_proc = goog_proc[3]
            goog_proc = goog_proc.split("q=", 1)
            goog_proc = goog_proc[1]
            goog_proc = goog_proc.split("&", 1)
            goog_proc = goog_proc[0]
            goog_proc = 'google.com/search?q='+goog_proc

            r3 = requests.get('http://'+goog_proc)

            logfile = open('currentlog.log', 'a')
            logfile.write('\nHOST:\n'+host)
            logfile.flush()
            logfile.close()
            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM URL AS SEARCH(GOOGLE):\n'+'http://'+goog_proc)
            logfile.flush()
            logfile.close()
            #r3_back = 'http://'+goog_proc

            return r3
    else:

        return r2
    #return r2.content

@app.route('/<path:other>', methods=HTTP_METHODS)
def other(other):
    global url
    #text = request.form['text']
    #url = text.upper()
    r0 = requests.get('http://'+url+'/'+other)
    #print ('\n'*12)
    #print ('http://'+url+'/'+other)
    #print ('\n'*12)
    #return r.content
    if 'search?' in request.url:
            logfile = open('currentlog.log', 'a')
            logfile.write('\nEXCEPTION DETECTED AS GOOGLE SEARCH.')
            logfile.flush()
            logfile.close()
            goog_proc = request.url
            goog_proc = goog_proc.split("/", 3)
            goog_proc = goog_proc[3]
            goog_proc = goog_proc.split("q=", 1)
            goog_proc = goog_proc[1]
            goog_proc = goog_proc.split("&", 1)
            goog_proc = goog_proc[0]
            goog_proc = 'google.com/search?q='+goog_proc

            r3 = requests.get('http://'+goog_proc)
            logfile = open('currentlog.log', 'a')
            logfile.write('\nHOST:\n'+host)
            logfile.flush()
            logfile.close()
            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM URL AS SEARCH(GOOGLE):\n'+'http://'+goog_proc)
            logfile.flush()
            logfile.close()
            #r3_back = 'http://'+goog_proc

            return r3.content
    else:

        return r0.content

@app.route('/devolopment/<path:other>', methods=HTTP_METHODS)
def other2(other2):
    global host
    global url2


    #text = request.form['text']
    #url = text.upper()
    r2 = fixURL('http://'+url2+'/'+other2)
    r2 = r2.replace('\\n', '\n').replace("b'", '').replace('\xe2\x80\x99', "'")
    #print ('\n'*12)
    #print ('http://'+url+'/'+other)
    #print ('\n'*12)
    logfile = open('currentlog.log', 'a')
    logfile.write('URL:\n'+url2+'OTHER:\n'+other2+'\n')
    logfile.flush()
    logfile.close()
    if 'search?' in request.url:
            logfile = open('currentlog.log', 'a')
            logfile.write('\nEXCEPTION DETECTED AS GOOGLE SEARCH.')
            logfile.flush()
            logfile.close()
            goog_proc = request.url
            goog_proc = goog_proc.split("/", 3)
            goog_proc = goog_proc[3]
            goog_proc = goog_proc.split("q=", 1)
            goog_proc = goog_proc[1]
            goog_proc = goog_proc.split("&", 1)
            goog_proc = goog_proc[0]
            goog_proc = 'google.com/search?q='+goog_proc

            r3 = requests.get('http://'+goog_proc)
            logfile = open('currentlog.log', 'a')
            logfile.write('\nHOST:\n'+host)
            logfile.flush()
            logfile.close()
            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM URL AS SEARCH(GOOGLE):\n'+'http://'+goog_proc)
            logfile.flush()
            logfile.close()
            #r3_back = 'http://'+goog_proc

            return r3.content
    else:

        return r2


@app.errorhandler(500) #shut up, it works.(sometimes)
def page_not_found(e):
    print('MAIN bugfix1: HANDLE 500 ERROR')
    global proc_url
    global url2
    global host
    global current_host
    try:
        errorlog = open('errorlog.log', 'a')
        errorlog.write('\nError recived with page '+request.url)
        errorlog.flush()
        errorlog.close()
        rulen=''
        ruleen=''
        rule=''
        proc_url=''
        goog_proc=''
        r3=''
        logfile = open('currentlog.log', 'a')
        logfile.write('\nHOST:\n'+host)
        logfile.flush()
        logfile.close()

        rulen = request.url
        ruleen = str(rulen)

        logfile = open('currentlog.log', 'a')
        logfile.write('\nURL BEFORE PROC:\n'+ruleen)
        logfile.flush()
        logfile.close()
        rule = ruleen.replace('%2F', '/')
        #rule = rule.replace('http://', '')
        rule_split = rule.split("&", 1)
        proc_url = rule_split[0]
        proc_url = proc_url.split("=", 1)
        proc_url = proc_url[1]

        if 'search?' in rulen:
            logfile = open('currentlog.log', 'a')
            logfile.write('\nEXCEPTION DETECTED AS GOOGLE SEARCH.')
            logfile.flush()
            logfile.close()
            goog_proc = request.url
            goog_proc = goog_proc.split("/", 3)
            goog_proc = goog_proc[3]
            goog_proc = goog_proc.split("q=", 1)
            goog_proc = goog_proc[1]
            goog_proc = goog_proc.split("&", 1)
            goog_proc = goog_proc[0]
            goog_proc = 'google.com/search?q='+goog_proc

            r3 = requests.get('http://'+goog_proc)
            logfile = open('currentlog.log', 'a')
            logfile.write('\nHOST:\n'+host)
            logfile.flush()
            logfile.close()
            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM URL AS SEARCH(GOOGLE):\n'+'http://'+goog_proc)
            logfile.flush()
            logfile.close()
            #r3_back = 'http://'+goog_proc

            return r3.content
        else:

            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM GOOGLE RESULT:\n'+'http://'+proc_url)
            logfile.flush()
            logfile.close()
            r3 = requests.get('http://'+proc_url)
            #r3 = r3.replace('\\n', '\n').replace("b'", '').replace('xe2x80x99', "'")
            return r3.content
            current_host = request.url
            current_host = current_host.split("/", 3)
            current_host = current_host[3]  #url?q=https://thesatanictemple.com/&sa=U&ved=2a
            current_host = current_host.split("=", 1)
            current_host = current_host[1]
            current_host = current_host.split("&", 1)
            current_host = current_host[0]
    #return rule
    except Exception as er:
        if 'list index out of range' in str(er):
            ur = request.url
            ur = ur.split('/', 3)
            ur = ur[3]
            ur = current_host+ur

            logfile = open('currentlog.log', 'a')
            logfile.write('\nREQUESTING HTML FROM IN SITE URL:\n'+'http://'+ur)
            logfile.flush()
            logfile.close()
            r4 = fixURL(ur)

            return r4
        else:
            current_time = datetime.datetime.now()
            print('LOGGED ERROR AT:'+current_time)
            errorlog = open('errorlog.log', 'a')
            errorlog.write('\n'+current_time+' ERR WITH REQUEST:'+request.url+' ERR:'+er)
            errorlog.flush()
            errorlog.close()
            return render_template('500.html', variable=request.url, variable2=er), 500
if __name__ == '__main__':
    app.run()
