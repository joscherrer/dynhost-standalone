import os
import ovh
import time
import signal
import urllib.request

client = ovh.Client()
zoneName = "mvd.ovh"
root_url = f'/domain/zone/{zoneName}/dynHost'

subd = "str"
fp = urllib.request.urlopen("https://api.ipify.org")
_bytes = fp.read()

ipv4 = _bytes.decode("utf8")
fp.close()

record_id = client.get(f'{root_url}/record',
    subDomain=subd
)
if not record_id:
    result = client.post(f'{root_url}/record',
        ip=ipv4,
        subDomain=subd
    )
    print(f'Creating record {subd} with IPv4 {ipv4}')
else:
    result = client.get(f'{root_url}/record/{record_id[0]}')
    if ipv4 == result['ip']:
        exit()
    result = client.put(f'{root_url}/record/{record_id[0]}',
        ip=ipv4,
        subDomain=subd
    )
    print(f'Updating record {subd} with IPv4 {ipv4}')
result = client.post(f'/domain/zone/{zoneName}/refresh')
