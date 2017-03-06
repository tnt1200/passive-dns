from bottle import route, run, template, static_file, error, abort
from model import TldRecord
import json


def get_dict(record):
    return dict(name=record.domain_name + "\t" + ", ".join(sorted(record.address)), open="true")


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')


@error(404)
def error404(error):
    return '404 NOT FOUND'


@route('/<tld_name>')
def test(tld_name):
    tld = TldRecord.objects(tld_name=tld_name).first()
    if tld:
        l = [dict(open="true", name=tld.tld_name, children=list(
            map(get_dict, tld.dnsrecords)))]
        js = json.dumps(l)
        return template('domain_list', js=js)
    else:
        return abort(404)


@route('/')
def index():
    return template('domain', dl=TldRecord.objects)

if __name__ == "__main__":
    run(host='localhost', port=8000)
