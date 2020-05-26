from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import urllib.request
import requests
import numpy
import time
import urllib
from collections import defaultdict
from datetime import datetime

############################################################################################
#######################Made the chrome driver operate headlessly############################
############################################################################################

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

############################################################################################
######################Get the file information##############################################
############################################################################################

inputAlignment = "modifieduniprot-keyword-Cell+membrane-filtered-organism-Homo.fasta" # An alignment file produced by AliView.
inputAlignmentPath = "/Users/newumuser/Desktop/Coronavirus Python/Furin Cleavage and O-glycosylation/UniProt Homo Sapiens Swiss-Prot Reviewed Proteome 20350/2. Cell Membrane/"
file = open(inputAlignmentPath + inputAlignment, "r")
lines = file.readlines() # The readline() function returns a list of lines in the file.
file.close()

def chunks(lst, n):
    dataUpload = []
    for i in range(0, len(lst), n):
        dataUpload.append(lst[i:i + n])
    return dataUpload

############################################################################################
######################First half of the code################################################
############################################################################################

nogData = []
i = 0
for each in chunks(lines, 40):

   #start it up
   driver = webdriver.Chrome('/Users/newumuser/Desktop/Coronavirus Python/Furin Cleavage and O-glycosylation/UniProt Homo Sapiens Swiss-Prot Reviewed Proteome 20350/chromedriver', options = options)
   driver.implicitly_wait(15) # wait's for the page to get done loading before it does anything with it
   driver.get('http://www.cbs.dtu.dk/services/NetOGlyc/')
   current_url = driver.current_url

   #To fill out a form
   search = driver.find_element_by_name('SEQPASTE')
   driver.execute_script("arguments[0].value = arguments[1];", search, ''.join(each))
   # search.send_keys(each)

   #to press a button based on the value (what it says)
   search = driver.find_element_by_xpath('//input[@type="submit" and @value="Submit"]')
   # time.sleep(10)
   newURL = search.click()

   WebDriverWait(driver, 15).until(EC.url_changes(current_url))
   resultPage = driver.current_url
   nogData.append(resultPage)
   i+=1
   print(i, 'of', len(chunks(lines,40)), 'sub-fastas have been submitted to NetOGlyc4.0')

print('All of the sub-fastas have been submitted')
print('A list of the file output pages: ', nogData)
print('This many URLs should be retrieved: ', len(nogData))

############################################################################################
######################Second half of the code###############################################
############################################################################################

nogScoresCompiled = []
extractedURLs = []
j = 0
print('Initiating the extraction process...')
while len(nogData) > 0:
    now = datetime.now().time()

    print('\n', 'Resting...', now)
    time.sleep(300)
    print('Searching...', now)

    i = 0
    for result in nogData:
        # print('url is being checked!')
        html = requests.get(result).text
        if "the output" in html:
            extractedURLs.append(result)
            # print(result)

            # parse the html data
            prelimTrim = html.split('#seqname	source	feature	start	end	score	strand	frame	comment')
            # print(prelimTrim)
            middleTrim = prelimTrim[1].split('<font face="ARIAL,HELVETICA">')
            # print(middleTrim)
            finalTrim = middleTrim[0].lstrip('\n')
            nogScoresCompiled.append(finalTrim)
            j+=1
            nogData.remove(result)
            print(len(extractedURLs), "of", len(chunks(lines,40)), 'result pages have been acquired. The original URL list now has this many links left: ', len(nogData))
        i+=1

print('length', len(nogData), nogData)
print('length', len(extractedURLs), extractedURLs)
print(nogScoresCompiled)

nogPredictionFile = open('NetOGlycResults_' + inputAlignment + '.txt', 'w')
for prediction in nogScoresCompiled:
	nogPredictionFile.write(prediction)
