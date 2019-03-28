import requests
import lxml.html
import re
from io import StringIO
import warnings
import time
from typing import Tuple, Any, Type

from fuzzywuzzy import fuzz


def request(vendor, url) -> Tuple[lxml.html.HtmlElement, Any]:  # todo: correctly type this!
        # Check if enough time has passed  since the last request
        while time.time() - vendor.__LAST_REQUEST__ < vendor.__REQUEST_INTERVAL__:
            pass

        # Send a request & parse it
        r = vendor.session.get(url)
        dom = lxml.html.parse(StringIO(r.content.decode('utf-8')))

        # Log this as the last request
        __LAST_REQUEST__ = time.time()

        return dom.getroot(), r.cookies


class Vendor:
    """ Subclassed to define specific vendors """
    __REQUEST_INTERVAL__ = 1
    __LAST_REQUEST__ = 0

    __part_pattern__ = re.compile('!')      # placeholder regex
    __approx_partp__ = re.compile('(!)')    # placeholder regex

    session = requests.Session()

    @classmethod
    def part(cls, string: str) -> str:
        matches = re.findall(cls.__approx_partp__, string)
        try:
            return cls.fix(max(matches, key=len))  # todo: assuming the longest match is the correct one
        except ValueError:
            return ''

    @classmethod
    def fix(cls, part: str) -> str:
        return part  # todo: check if the string fits the expected pattern at this point?

    @classmethod
    def valid_part(cls, part: str) -> bool:
        if re.match(cls.__part_pattern__, part) is not None:
                return True
        else:
            cls.warn_pattern(part)
            return False

    @classmethod
    def url(cls, part: str) -> str:
        raise NotImplementedError

    @classmethod
    def request(cls, part: str) -> lxml.html.HtmlElement:
        part = cls.fix(part)
        if cls.valid_part(part):
            url = cls.url(part)
            r, cookies = request(cls, url)
            cls.__cookies__ = cookies
            return r

    @classmethod
    def format_price(cls, price: str) -> str:
        numbers = re.findall('[0-9]+', price)

        price = 0
        for n, V in zip(reversed(numbers), [0.01, 1, 1000]):
            price = price + float(n)*V

        return "€" + str(price)

    @classmethod
    def get_info(cls, part: str) -> dict:
        raise NotImplementedError

    @classmethod
    def warn_metric(cls, part):
        warnings.warn(f"Invalid part number: '{part}' ends with '-M', should be '/M'", stacklevel=3)

    @classmethod
    def warn_pattern(cls, part):
        pattern = cls.__part_pattern__.pattern
        warnings.warn(f"Invalid part number: '{part}' does not fit '{pattern}'", stacklevel=3)

    @classmethod
    def warn_page(cls, part):
        url = cls.url(part)
        warnings.warn(f"Parse error: '{part}' not found or unexpected format at {url}", stacklevel=3)


class Thorlabs(Vendor):

    __part_pattern__ = re.compile('^[A-Z0-9\-.]+(/M)?$')
    __approx_partp__ = re.compile('([A-Z0-9\-/_.\\\]+)')
    __metric__ = re.compile('[-|_]M$')

    @classmethod
    def fix(cls, part: str) -> str:
        part = re.sub(cls.__metric__, '/M', part)
        return part

    @classmethod
    def valid_part(cls, part: str) -> bool:
        if re.match(cls.__part_pattern__, part) is not None:
            if part[-2:] == '-M': # 'unfixed' part number
                cls.warn_metric(part)
                return False
            else:
                return True
        else:
            cls.warn_pattern(part)
            return False

    @classmethod
    def url(cls, part: str) -> str:
        return f"https://www.thorlabs.com/thorproduct.cfm?partnumber={part}"

    @classmethod
    def get_info(cls, part: str) -> dict:
        page = cls.request(part)

        if page is not None:
            price = page.xpath('.//font')
            title = page.xpath('.//td[@class="PartTitle"]/b')

            if len(title) > 0:
                title = title[0].text
                title = re.sub(part + '\s-', '', title).strip()
            else:
                title = ''

            if price is not None and len(price) == 1:
                return {'title': title, 'price': cls.format_price(price[0].text)}
            else:
                cls.warn_page(part)
        else:
            cls.warn_page(part)
        return {'title': None, 'price': None}


class EdmundOptics(Vendor):

    __part_pattern__ = re.compile('^#[0-9]{2}-[0-9]{3}$')
    __approx_partp__ = re.compile('[#0-9\-_]+')

    @classmethod
    def url(cls, part: str) -> str:
        # ommit # from part number in the url - assuming that's the first character!
        return f"https://www.edmundoptics.com/search/?criteria={part[1:]}"

    @classmethod
    def format_price(cls, price: str):
        return "(!) $" + Vendor.format_price(price)[1:]

    @classmethod
    def get_info(cls, part) -> dict:
        page = cls.request(part)

        if page is not None:
            price = page.xpath('.//span[@class="Price"]')
            if price is not None and len(price) > 0:
                return {'price': cls.format_price(price[0].text)}
            else:
                cls.warn_page(part)
        else:
            cls.warn_page(part)
        return {'price': None}


class Newport(Vendor):

    __part_pattern__ = re.compile('^$')

    @classmethod
    def url(cls, part: str) -> str:
        pass

    @classmethod
    def get_info(cls, part: str) -> str:
        pass


def parse(part: str) -> Tuple[str, str, dict, str]:
    vendors = (Thorlabs, EdmundOptics, Newport)

    match = []
    for v in vendors:
        match.append(fuzz.partial_ratio(v.__name__, part))

    if max(match) < 75:
        return '?', part, {}, '?'
    else:
        vendor = vendors[match.index(max(match))]

        part = vendor.part(part)

        return vendor.__name__, part, vendor.get_info(part), vendor.url(part)



