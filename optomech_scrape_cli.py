import argparse
from optomech_scrape import part

parser = argparse.ArgumentParser()

parser.add_argument('part', type=str, help="Part ID as <VENDOR> <PART NUMBER>. The vendor's name and part number "
                                           "should be formatted more or less correctly.")
parser.add_argument('-p', type=bool, help="Return part price.")
parser.add_argument('-t', type=bool, help="Return part title.")
parser.add_argument('-u', type=bool, help="Return part url.")

if __name__ == '__main__':
    args = parser.parse_args()

    vendor, part_number, info, url = part(args.part)

    if args.p:
        price = info['price']
    else:
        price = ''

    if args.t:
        title = info['title']
    else:
        title = ''

    if not args.u:
        url = ''

    print(price, title, url)
