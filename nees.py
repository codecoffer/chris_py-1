import requests
import config
import cloudscraper
import hashlib
import re
from lxml import html
from bs4 import BeautifulSoup

# H SYNARTHSH POU VRISKEI TOYS TITLOYS KAI TA URL
def findurls(soup):
    soup0 = soup.findAll("div", attrs={'class': 'rating0 sticky'}) + soup.findAll("div", attrs={'class': 'rating0 nonsticky'})

    with open("results_greek_to.txt", "a+") as r1:
        for a in soup0:
            # if not a.find('img', attrs={'src': 'images/Seamus/misc/tag.png'}): #  OK MH TO SVHSEIS TO THELW !!!
            if not re.search('.+attachmentid=94264&amp+.', str(a)) and not re.search('.+attachmentid=94262&amp+.', str(a)):
                soup1 = a.find('a', attrs={'class': 'title'})
                soup2 = a.find('a', attrs={'class': 'title threadtitle_unread'}, href=True)
                if not soup2:
                    soup2 = a.find('a', attrs={"class": ["title"]}, href=True)
                if soup2:
                    link = (soup2.get('href'))
                if soup1:
                    title = soup1.text.split(sep, 1)[0]

                r1.write(title)
                r1.write(")")
                r1.write("  ")
                r1.write(link)
                r1.write("\n")

open('results_greek_to.txt', 'w').close()  # to empty contents

### GREEKTO LOGIN_START
url = "http://www.greek.to/forum/login.php?do=login"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}
scraper = cloudscraper.create_scraper()  # returns a CloudflareScraper instance

with scraper.post(url) as s:
    username = 'mimaras125'
    password = 'votsi125'
    BASE_URL = 'http://www.greek.to/forum/'

    r = scraper.post(BASE_URL + '/login.php?do=login', {
    'vb_login_username':        username,
    'vb_login_password':        password,
    'vb_login_md5password':     hashlib.md5(password.encode()).hexdigest(),
    'vb_login_md5password_utf': hashlib.md5(password.encode("utf-8")).hexdigest(),

    'cookieuser': 1,
    'do': 'login',
    's': '',
    'securitytoken': 'guest'
    })
### GREEKTO_LOGIN_END

    sep = ')'
    # ANOIKSE TO ARXEIO ME TIS SELIDES POY THA XRHSIMOPOIHSOYME
    basepages= open("selides_greekto", "r")

    while True:
        base_page = basepages.readline()
        if not base_page:
            break;
        base_page = base_page.strip()
        use_page = scraper.get(base_page)
        soup = BeautifulSoup(use_page.content, 'lxml')
        findurls(soup)

        # DHLWNOYME METABLHTES GIA NA KOITAEI KAI TIS EPOMENES SELIDES
        last_page = soup.find('span', attrs={"class": ["first_last"]})
        if last_page:
            last_page_num = last_page.a['href'].split('/')[1].replace('page', '')
            for page in range(2, int(last_page_num) + 1):
                use_page = base_page + '/page' + str(page)
                use_page = scraper.get(use_page)
                soup = BeautifulSoup(use_page.content, 'lxml')
                findurls(soup)
                #print(base_page0)




print(1)