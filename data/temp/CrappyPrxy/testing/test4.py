import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import os
import time
import gc
script_fix = 0
css_fix = 0
img_fix = 0
end=''
start=''
objectsToDownload = 0
import os, psutil
def fixURL(url):
  print('fixURL called')
  start = time.time
  global objectsToDownload
  progStatus=''
  currentFile=''
  currentIteration = 1
  def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    global obectsToDownload
    global progStatus
    global currentFile
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}'+progStatus+' ('+currentFile+')', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
  global objectsToDownload
  global script_fix
  global end
  global css_fix
  
  global img_fix
  # URL of the web page you want to extract
  #url = "http://discord.com"

  # initialize a session
  #session = requests.Session()
  # set the User-agent as a regular browser
  #session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
  # get the HTML content
  #print('\n'*10)
  #print(url)
  #print('\n'*10)
  try:
      append_html = requests.get(url)
  except requests.exceptions.MissingSchema:
      print('Error getting '+url)
      append_html = requests.get('http://'+url)
  append_html = append_html.content
  
  # parse HTML using beautiful soup
  soup = bs(append_html, "html.parser")
  # get the JavaScript files
  script_files = []
  #append_html = requests.get(url)
  
  #append_html = append_html.content()
  def getDownStatus():
    global objectsToDownload
    print('Calculating how many assets to download.')
    for script in soup.find_all("script"):
      objectsToDownload += 1
    for script in soup.find_all("src"):
      objectsToDownload += 1
    for script in soup.find_all("css"):
      objectsToDownload += 1
  print('START: GET '+url+'.')
  getDownStatus()
  
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
              progStatus = 'Downloading scripts.'
              currentFile = 'downloading '+url+'/'+search_script
              printProgressBar(currentIteration, objectsToDownload)
              currentIteration += 1
              #sh_fix = open('fix.sh', w)
              search_f = search_script.split('/')
              search_c = search_script.count('/')
              search_r = search_f[search_c]
              search_script2 = search_script.replace(search_r, '')
              try:
                  os.mkdir('static/'+search_script2)

              except Exception as er:
                  print("error creating static folder. "+er)
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
                  append_html = str(append_html).replace(url+search_script, search_script[1:])#.replace('/'+search_script2, '/static/'+search_script2)
              script_fix += 1
              script_files.append(search_script)



  # get the CSS files
  progStatus='Downloading CSS files.'
  css_files = []
 
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
              raise MemoryError('Rather disappointed in self, committed suicide.')
      if css.attrs.get("href"):
          # if the link tag has the 'href' attribute
          #if url not in css.attrs.get("href"):
          css_url = urljoin(url, css.attrs.get("href"))
          css_files.append(css_url)
          search_css = str(css_url).split(url+'/')

          search_css = search_css[1]

          if search_css not in css_files:
              progStatus = 'Downloading scripts.'
              currentFile = 'downloading '+url+'/'+search_css
              printProgressBar(currentIteration, objectsToDownload)
              currentIteration += 1
              search_f = search_css.split('/')
              search_c = search_css.count('/')
              search_r = search_f[search_c]
              search_css2 = search_css.replace(search_r, '')
              try:
                  os.mkdir('/static'+search_css2)

              except Exception as er:
                  print('error creating static folder. '+er)
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

                  append_html = str(append_html).replace(url+search_css, search_css[1:])#.replace('/'+search_script2, '/static/'+search_script2)
              css_fix += 1
              css_files.append(search_css)

  progStatus = 'Downloading image files.'
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
              raise MemoryError('Not usefull enough, therfore murdered.')
      if search_img not in img_files:
          #print(search_img+' is not in '+str(img_files))
          progStatus = 'Downloading scripts.'
          currentFile = 'downloading '+url+'/'+search_image
          printProgressBar(currentIteration, objectsToDownload)
          currentIteration += 1
          #print('soup replacing '+search_img+' with '+img_ur
          search_f = search_img.split('/')
          search_c = search_img.count('/')
          search_r = search_f[search_c]
          search_img2 = search_img.replace(search_r, '')
          try:
              os.mkdir('static/'+search_img2)
          except Exception as er:
              print('error creating static folder '+er)
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
              append_html = str(append_html).replace(url+search_img, search_img[1:])#.replace('/'+search_script2, '/static/'+search_script2)
          img_fix += 1
          img_files.append(search_img)
  append_html = append_html.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
  #print(img_files)

  end = time.time()
  return append_html
html = fixURL('http://discord.com')
writeHtml = open('discord.html', 'w')
#html = html.replace('\\n', '\n').replace("\\", '').replace("b'", '').replace('xe2x80x99', "'")
writeHtml.write(str(html))
writeHtml.flush()
writeHtml.close()


