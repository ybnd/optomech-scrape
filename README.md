# optomech-scrape

Query price and information on optical & optomechanical components by vendor and part ID.

### Usage

```python
from optomech_scrape import part
part('Thorlabs ER3-P4')

>>> ('Thorlabs', 'ER4-P4', {'title': 'Cage Assembly Rod, 4" Long, Ø6 mm, 4 Pack', 'price': '€24.52'}, 'https://www.thorlabs.com/thorproduct.cfm?partnumber=ER4-P4')
```

### Supported vendors

- [Thorlabs](https://www.thorlabs.com/)
- [Edmund Optics](https://www.edmundoptics.com/)

### Disclaimer

This code is intended to help gathering pricing for limited amounts of parts from a bill of materials. It is not the authors intention to write automated crawlers to copy any of the vendors' databases or to cause excessive server load. 

Please [contact me](ybnd@tuta.io) with any questions or remarks.

