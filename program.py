import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WheaterReport', 'cond, temp, scale, loc')

def main():
    print_the_header()

    code = input('What zipcode do you want the weather for (97201)? ')

    html = get_html_from_web(code)

    report = get_weather_from_html(html)

    print('The temp in {} is {} {} and {}'.format(report.loc, report.temp, report.scale, report.cond))



    #display the forecast


def print_the_header():
    print('----------------------------------------------')
    print('                  WHEATER APP')
    print('----------------------------------------------')
    print()

def get_html_from_web(zipcode):
    url = 'https://www.wunderground.com/weather-forecast/{}'.format(zipcode)

    #print(url)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text[0:250])
    return response.text


def get_weather_from_html(html):
    soup = bs4.BeautifulSoup(html,'html.parser')
    loc = soup.find(id='location').find('h1').get_text()
    condition = soup.find(id='curCond').find(class_='wx-value').get_text()
    temp = soup.find(id='curTemp').find(class_='wx-value').get_text()
    scale = soup.find(id='curTemp').find(class_='wx-unit').get_text()

    loc = cleanup_text(loc)
    loc = find__city_and_state_from_location(loc)
    condition = cleanup_text(condition)
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)

    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)

    return report
#    return condition, temp, scale, loc
#    print(condition, temp, scale, loc)

def find__city_and_state_from_location(loc : str):
    parts = loc.split('\n')
    return parts[0].strip()


def cleanup_text(text : str):
    if not text:
        return text

    text = text.strip()
    return text

if __name__ == '__main__':
    main()
