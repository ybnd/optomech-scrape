import argparse
from optomech_scrape import part

parser = argparse.ArgumentParser()

parser.add_argument('part', type=str, help="Part ID as <VENDOR> <PART NUMBER>. The vendor's name and part number "
                                           "should be formatted more or less correctly.")
parser.add_argument('-p', type=bool, help="Return part price.", default=True)
parser.add_argument('-t', help="Return part title.", action='store_true')
parser.add_argument('-u', help="Return part url.", action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()

    vendor, part_number, info, url = part(args.part)
    # todo: if an invalid part_id is given this thing will probably still send some html requests...

    if args.p:
        print(info['price'])

    if args.t:
        print(info['title'])

    if args.u:
        print(url)
