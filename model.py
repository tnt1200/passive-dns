from mongoengine import *
import datetime

connect(db='nmapscan', host='127.0.0.1', port=27017, connect=False)


class TldRecord(Document):
    tld_name = StringField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    @property
    def dnsrecords(self):
        return DnsRecord.objects(tld=self.id)


class DnsRecord(Document):
    tld = ReferenceField(TldRecord, reverse_delete_rule=CASCADE)
    domain_name = StringField(unique=True)
    address = ListField()
    created_at = DateTimeField(default=datetime.datetime.now)

    @property
    def urlrecords(self):
        return HttpRecord.objects(dname=self.id)


class HttpRecord(Document):
    dname = ReferenceField(DnsRecord, reverse_delete_rule=CASCADE)
    url = StringField(unique=True)
    title = StringField()
    headers = DictField()
    info = ListField()
    info_flag = BooleanField(default=False)
