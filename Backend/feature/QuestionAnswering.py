import sys
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

LENGTHLIMIT = 60

try:
    import logger
    logger = logger.get_logger(__name__)
except ModuleNotFoundError:
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class ConnectoinError():
    pass


class QuestionAnswering():
    def __init__(self):
        self.query = ""
        self.url = "https://www.google.com/search?q="
        self.thread = None

    def import_thread(self, thread):
        self.thread = thread

    def get_source(self, url):
        """
        Return the source code for the provided URL.
        Args:
            url (string): URL of the page to scrape.
        Returns:
            response (object): HTTP response object from requests_html.
        """
        try:
            # open session for url page
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            raise ConnectoinError
            logger.error(e)
            return None

    def get_results(self):
        """
        Return html object from url and query
        """
        query = urllib.parse.quote_plus(self.query)
        response = self.get_source(self.url + self.query)

        return response

    def parse_results(self, response):
        """
        Return content from html body
        Args:
            response(html response): html body of a scraped page
        Returns:
            output(list): content parsed from html
        """
        # css identifier to find result from Google result page
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".IsZvec"
        css_identifier_diet = ".hgKElc"
        css_identifier_ecom = ".PZPZlf span"
        css_identifier_exchange = ".b1hJbf"
        css_identifier_calculate = ".vUGUtc, .qv3Wpe"
        css_identifier_weather = ".nawv0d"
        css_identifier_support = ".kno-rdesc span"
        css_identifier_internet_diet = ".kp-blk"
        css_identifier_time = ".card-section.sL6Rbf"
        css_identifier_unit = ".card-section"
        css_identifier_location = ".rllt__details"

        # store css find result
        output = []

        # get content from html body by css identifier
        results = response.html.find(css_identifier_result)
        diet = response.html.find(css_identifier_diet, first=True)
        ecom = response.html.find(css_identifier_ecom, first=False)
        exchange = response.html.find(css_identifier_exchange, first=True)
        calculate = response.html.find(css_identifier_calculate, first=False)
        weather = response.html.find(css_identifier_weather, first=False)
        support = response.html.find(css_identifier_support, first=False)
        idiet = response.html.find(css_identifier_internet_diet, first=True)
        time = response.html.find(css_identifier_time, first=True)
        unit = response.html.find(css_identifier_unit, first=True)
        location = response.html.find(css_identifier_location, first=False)

        if diet:
            output.append({'diet': diet.text})
        else:
            output.append({'diet': None})

        if time:
            output.append({'time': time.text})
        else:
            output.append({'time': None})

        if ecom:
            output.append({'ecom': ""})
            for it in ecom:
                if 'jscontroller' in it.attrs and it.attrs['jscontroller'] == 'B82lxb':
                    output[-1]['ecom'] += it.text + ' '
                if 'jsname' in it.attrs and it.attrs['jsname'] == 'qRSVye':
                    output[-1]['ecom'] += it.text + ' '
                if 'class' in it.attrs and it.attrs['class'][0] == 'jBBUv':
                    output[-1]['ecom'] += it.attrs['aria-label'] + ' '

            if output[-1]['ecom'] == '':
                output[-1]['ecom'] = None
        else:
            output.append({'ecom': None})

        if exchange:
            output.append({'exchange': exchange.text.replace('\n', ' ')})
        else:
            output.append({'exchange': None})

        if unit:
            if unit.text.startswith("目前顯示的是以下字詞的搜尋結果"):
                output.append({'unit': None})
            else:
                output.append({'unit': unit.text.replace(
                    '\n', ' ').replace("詳細內容", '')})
        else:
            output.append({'unit': None})

        if location:
            output.append({'location': ""})
            for it in location:
                output[-1]['location'] += it.text.replace('\n', ' ') + ' '
        else:
            output.append({'location': None})

        if calculate:
            output.append({'calculate': ""})
            for it in calculate:
                output[-1]['calculate'] += it.text.replace('\n', ' ') + ' '
        else:
            output.append({'calculate': None})

        if weather:
            output.append({'weather': ""})
            output[-1]['weather'] += weather[0].find(
                ".VQF4g")[0].text.replace('\n', ' ') + ' '
            output[-1]['weather'] += weather[0].find(
                ".wtsRwe")[0].text.replace('\n', ' ')[:-5]
            for it in weather[0].find('span'):
                if 'id' in it.attrs and it.attrs['id'] == 'wob_ttm':
                    output[-1]['weather'] = f' {it.text}°F' + \
                        output[-1]['weather']
                if 'id' in it.attrs and it.attrs['id'] == 'wob_tm':
                    output[-1]['weather'] = f' {it.text}°C' + \
                        output[-1]['weather']
        else:
            output.append({'weather': None})

        if support:
            output.append({'support': []})
            for it in support:
                tmp = it.find('a')
                if tmp:
                    for iit in tmp:
                        output[-1]['support'].append(
                            f'[{it.text}]({str(iit.absolute_links.pop())})')
                else:
                    output[-1]['support'].append(it.text)

        else:
            output.append({'support': None})

        if idiet:
            output.append(
                {'internet_diet': idiet.text.replace("查看以下內容的搜尋結果:", "")})
        else:
            output.append({'internet_diet': None})

        for result in results:

            if result.find(
                css_identifier_title,
                first=True) is not None and result.find(
                css_identifier_link,
                first=True) is not None and result.find(
                css_identifier_text,
                    first=True) is not None:
                item = {
                    'title': result.find(
                        css_identifier_title, first=True).text, 'link': result.find(
                        css_identifier_link, first=True).attrs['href'], 'text': result.find(
                        css_identifier_text, first=True).text}
            else:
                item = {
                    "title": None,
                    "link": None,
                    "text": None
                }

            output.append(item)

        return output

    def get_answer(self, results):
        """
        Select answer from parsed output, if no answer found, return not found string.
        Args:
            results(list): list of parsed result
        Returns:
            ans(string): answer string to respond
        """
        flag = True
        ans = ''
        for result in results:
            if list(
                    result.keys())[0] != 'title' and list(
                    result.items())[0][1] is not None:
                ans += (urllib.parse.unquote(str(list(result.items())
                                                 [0][1]) + '\n'))
                flag = False
                break

        if flag:
            for result in results[:14]:
                if list(
                        result.keys())[0] == 'title' and list(
                        result.items())[0][1] is not None:
                    ans += (urllib.parse.unquote(
                        str(result['title']) + ',' + str(result['text']) + '\n'))

        ans = (ans.strip())
        if ans.startswith('找不到符合搜尋字詞') or ans.startswith("您是不是要查"):
            ans = ''
        if ans == '':
            ans = f"沒有查到「{search.query}」的相關資料"

        return ans

    def google_search(self, query):
        """
        Main function to scrape and parse result and return answer string.
        Args:
            query(string): query string to search for
        Return:
            ans(string): result of query.
        """
        self.query = query
        response = self.get_results()
        ans = ''
        if response is None:
            ans = f"沒有查到「{search.query}」的相關資料"
        else:
            results = self.parse_results(response)
            ans = self.get_answer(results)
            if len(ans) > LENGTHLIMIT:
                ans = ans[:LENGTHLIMIT] + "......其他查詢結果請點詳細網址連結"
        self.thread.add_thread({
            "class": "TextToSpeech",
            "func": "text_to_voice",
            "args": str(ans),
        })
        return ans


if __name__ == '__main__':
    search = QuestionAnswering()
    ans = search.google_search(str(input("請輸入問題:")))

    print(ans)
