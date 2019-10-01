# zeroHarvest

Harvests and processes IP addresses from ZeroNet's log directory, while barebones - it still can be used at this stage.

## Configuration
Give the token key a value in the config file to use an ipinfo access secret, it will otherwise use the public limit.

## Usage

* Make cli.py executable `chmod +x cli.py`
* Fetch addresses, process and write to output `./cli.py path/to/log/dir --write output_file [attributes]`

attributes: 
```
address
loc
hostname
city
region
country
org
timezone
tor
```

### Example
 `./cli.py ~/ZeroNet-py3/log/ --write output_file address country city region tor` 
 
 returns 
 ```
 address: 79.172.193.32
country: HU
city: Budapest
region: Budapest
tor: True
------------------------------
address: 104.238.198.186
country: US
city: Studio City
region: California
tor: False
------------------------------
...
```

## Wishlist

- [ ] Asynchronous requests to API
- [ ] Multiple APIs to process addresses with
- [ ] Continuous fetching while browsing
- [ ] Reduce repeat requests for already processed addresses when writing to existing output file