import os 
from pyairtable import Api

API_TOKEN = os.environ.get('AIRTABLE_TOKEN')

BASE_ID = 'app8DpSUnqY2fLBUv'
TABLE_ID = 'tblU7bn8HNzVUFcnA'

api = Api(API_TOKEN)

table = api.table(BASE_ID, TABLE_ID)

def get_all_records(count=None, sort=None):
    sort_param = []
    if sort and sort.upper()=='DESC':
        sort_param = ['-exam']
    elif sort and sort.upper()=='ASC':
        sort_param = ['exam']

    return table.all(max_records=count, sort=sort_param)

def get_record_id(name):
    return table.first(formula=f"name='{name}'")['id']

def update_record(record_id, data):
    table.update(record_id, data)

    return True

def add_record(data):
    # require data contains a "name" key and a "options" key  and a "correct" key(data is a dict)
    if 'name' not in data or 'options' not in data or 'correct' not in data:
        return False
    
    # Convert options to a list if it's not already
    if not isinstance(data['options'], list):
        data['options'] = [data['options']]

    table.create(data)
    return True

if __name__ == '__main__':
    ## Show getting certain records
    print("Show getting certain records")
    print(table.all(formula="exam < 5", sort=['-exam']))

    ## Show getting a single record
    print("Show getting a single record")

    # Replace a record
    print("Replace a record")
    name = "Test Message"
    record_id = table.first(formula=f"name='{name}'")['id']
    table.update(record_id, {"exam": "UDEA"})

    ## Show all records
    print("All records!")
    print(table.all())