import requests, urllib
from requests_html import HTML
from requests_html  import HTMLSession

class QuestionAnswering():
    def __init__(self):
        self.query = ""
        self.url = "https://www.google.com/search?q="

    def get_source(self, url):
        """Return the source code for the provided URL. 
        Args: 
            url (string): URL of the page to scrape.
        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)


    def scrape_google(self):

        query = urllib.parse.quote_plus(self.query)
        response = self.get_source("https://www.google.com/search?q=" + query)

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        return links

    def get_results(self):
        
        query = urllib.parse.quote_plus(self.query)
        response = self.get_source(self.url+self.query)
        
        return response

    def parse_results(self, response):
        
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".IsZvec"
        css_identifier_diet = ".hgKElc"
        # css_identifier_similar = ".Wt5Tfe span"
        css_identifier_ecom = ".PZPZlf span"
        css_identifier_exchange = ".b1hJbf"
        css_identifier_calculate = ".vUGUtc, .qv3Wpe"
        css_identifier_weather = ".nawv0d"
        css_identifier_support = ".kno-rdesc span"
        css_identifier_internet_diet = ".kp-blk"
        css_identifier_time = ".card-section.sL6Rbf"

        results = response.html.find(css_identifier_result)

        output = []
        diet = response.html.find(css_identifier_diet, first=True)
        # similar = response.html.find(css_identifier_similar, first=False)
        ecom = response.html.find(css_identifier_ecom, first=False)
        exchange = response.html.find(css_identifier_exchange, first=True)
        calculate = response.html.find(css_identifier_calculate, first=False)
        weather = response.html.find(css_identifier_weather, first=False)
        support = response.html.find(css_identifier_support, first=False)
        idiet = response.html.find(css_identifier_internet_diet, first=True)
        time = response.html.find(css_identifier_time, first=True)

        if diet:
            output.append({'diet':diet.text})
        else:
            output.append({'diet':None})

        # if similar:
        #     output.append({'similar':""})
        #     print(similar)
        #     for it in similar:
        #         if 'class' in it.attrs and it.attrs['class'][0] == 'hgKElc':
        #             print(it.attrs)
        #             output[-1]['similar'] += it.html + ' '
        # else:
        #     output.append({'similar':None})

        if time:
            output.append({'time':time.text})
        else:
            output.append({'time':None})

        if ecom:
            output.append({'ecom':""})
            for it in ecom:
                # if 'class' in it.attrs:
                #     print( it.attrs['class'][0])
                #     print(it.attrs['class'][0] == 'a4vfUd')
                # if 'class' in it.attrs and it.attrs['class'][0]=='jBBUv':
                #     print(it.attrs['class'])
                if 'jscontroller' in it.attrs and it.attrs['jscontroller']=='B82lxb':
                    output[-1]['ecom']+=it.text+' '
                if 'jsname' in it.attrs and it.attrs['jsname']=='qRSVye':
                    output[-1]['ecom']+=it.text+' '
                if 'class' in it.attrs and it.attrs['class'][0]=='jBBUv':
                    output[-1]['ecom']+=it.attrs['aria-label']+' '

            if output[-1]['ecom'] == '':
                output[-1]['ecom'] = None
        else:
            output.append({'ecom':None})

        if exchange:
            output.append({'exchange':exchange.text.replace('\n',' ')})
        else:
            output.append({'exchange':None})

        if calculate:
            output.append({'calculate':""})
            for it in calculate:
                output[-1]['calculate'] += it.text.replace('\n',' ')+' '
        else:
            output.append({'calculate':None})

        if weather:
            output.append({'weather':""})
            output[-1]['weather'] += weather[0].find(".VQF4g")[0].text.replace('\n', ' ') + ' '
            output[-1]['weather'] += weather[0].find(".wtsRwe")[0].text.replace('\n', ' ')[:-5]
            for it in weather[0].find('span'):
                # if 'id' in it.attrs:
                #     print(it.attrs['id'])
                if 'id' in it.attrs and it.attrs['id'] == 'wob_tm':
                    output[-1]['weather'] += f' {it.text}°C'
                if 'id' in it.attrs and it.attrs['id'] == 'wob_ttm':
                    output[-1]['weather'] += f' {it.text}°F'
        else:
            output.append({'weather':None})

        if support:
            output.append({'support':[]})
            # print(support[0].find(".kno-rdesc")[0].text)
            for it in support:
                tmp = it.find('a')
                if tmp:
                    for iit in tmp:
                        output[-1]['support'].append(f'[{it.text}]({str(iit.absolute_links.pop())})')                
                else:
                    output[-1]['support'].append(it.text)

        else:
            output.append({'support':None})

        if idiet:
            output.append({'internet_diet':idiet.text.replace("查看以下內容的搜尋結果：", "")})
        else:
            output.append({'internet_diet':None})

        for result in results:

            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'],
                'text': result.find(css_identifier_text, first=True).text
            }
            
            output.append(item)
            
        return output

    def get_answer(self, results):
        flag = True
        ans = ''
        for result in results:
            if list(result.keys())[0] != 'title' and list(result.items())[0][1] != None:
                ans += (urllib.parse.unquote(str(list(result.items())[0][1])+'\n'))
                flag = False
                # break
    
        if flag:
            for result in results:
                if list(result.keys())[0] == 'title' and list(result.items())[0][1] != None:
                    ans += ( urllib.parse.unquote(str(result)+'\n'))
        
        ans = (ans.strip())
        if ans == '':
            print(f"沒有查到「{search.query}」的相關資料")

        return ans

    def google_search(self, query):
        self.query = query
        response = self.get_results()
        return self.parse_results(response)

if __name__ == '__main__':  
    search = QuestionAnswering()
    results = search.google_search("日幣")
    ans = search.get_answer(results)
    
    print(ans)