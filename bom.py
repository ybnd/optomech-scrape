from optomech import parse
import argparse
import pandas as pd

# parser = argparse.ArgumentParser()
#
# parser.add_argument('-file', type=str)


if __name__ == '__main__':
    file_in = 'D:/Box Sync/Setup/190327 - update bom1.csv'
    file_out = 'D:/Box Sync/Setup/bom.xlsx'

    data_in = pd.read_csv(file_in)
    data_out = pd.DataFrame(
        [], columns=['id', 'Title', 'Vendor', 'Part', 'Quantity', 'Unit Price', 'URL', 'Notes']
    )

    for i in range(len(data_in)):
        id = data_in.iloc[i]['Part name']
        vendor, part, info, url = parse(id)

        if info is not None:
            try:
                title, unit_price = info
            except ValueError:
                unit_price = info
                title = '?'
        else:
            title = '?'
            unit_price = '?'

        print(f"{i+1}/{len(data_in)}: {id} -> {vendor} {part}")

        notes = data_in.iloc[i]['Description']

        if not isinstance(notes, str):
            notes = ''

        row = {
            'Vendor': vendor, 'Part': part, 'Unit Price': unit_price, 'URL': url,
            'id': id, 'Quantity': data_in.iloc[i]['Quantity'],
            'Title': title, 'Notes': notes
        }

        row = pd.Series(row, index=row.keys())
        data_out = data_out.append(row, ignore_index=True)

    data_out.to_excel(file_out, index=False)
