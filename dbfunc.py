from boltons.cacheutils import cached, LRU
from tld import get_tld
from time import time
from model import DnsRecord, TldRecord
from mongoengine.errors import NotUniqueError

my_cache = LRU()


@cached(my_cache)
def save_record(domain_name, address):
    try:
        tld = get_tld("http://" + domain_name)
    except Exception as e:
        pass
    else:
        tld_record = TldRecord.objects(tld_name=tld).first()
        if tld_record:
            dns_record = DnsRecord.objects(domain_name=domain_name).first()
            if dns_record:
                if address not in dns_record.address:
                    dns_record.address.append(address)
                    dns_record.save()
            else:
                dr = DnsRecord(
                    domain_name=domain_name, tld=tld_record.to_dbref())
                dr.address.append(address)
                dr.save()
        else:
            tld_r = TldRecord(tld_name=tld).save()
            dns_record = DnsRecord.objects(domain_name=domain_name).first()
            if dns_record:
                if address not in dns_record.address:
                    dns_record.address.append(address)
                    dns_record.save()
            else:
                dr = DnsRecord(domain_name=domain_name, tld=tld_r.to_dbref())
                dr.address.append(address)
                dr.save()
