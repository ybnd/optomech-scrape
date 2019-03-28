# optomech-scrape

Query price and information on optical & optomechanical components by vendor and part ID.

### Installation

```bash
pip install -r requirements.txt
```

Compile to binary with PyInstaller:

```bash
pyinstaller --onefile optomech-scrape.py
```

### Usage

Most optomechanics vendors provide 3D models of their parts. To plan a setup, these models can be combined in any CAD software. If you name each part according to its vendor and part number and extract the bill of materials from your setup design, ```optomech-scrape``` can be used to return the price for the entire BOM.

```python
from optomech_scrape import part
part('Thorlabs ER4-P4')

>>> ('Thorlabs', 'ER4-P4', {'title': 'Cage Assembly Rod, 4" Long, Ø6 mm, 4 Pack', 'price': '€24.52'}, 'https://www.thorlabs.com/thorproduct.cfm?partnumber=ER4-P4')
```

```bash
> python optomech-scrape.py "Thorlabs ER4-P4"
€24.52
```

Some components (such as cage rods, posts, ...) are also sold in 'packs' at a better value, so make sure to double check your BOM when you make an order list.

### Supported vendors

- [Thorlabs](https://www.thorlabs.com/)
- [Edmund Optics](https://www.edmundoptics.com/)

### Disclaimer

This code is intended to help gathering pricing for limited amounts of parts from a bill of materials. It is not the authors intention to write automated crawlers to copy any of the vendors' databases or to cause excessive server load. 

Please contact me with any questions or remarks.

