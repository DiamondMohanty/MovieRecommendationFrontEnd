from datetime import date
def generate_message_body(items, customer_addr, customer_name, customer_phone):
    orderedItemsString = '';
    for element in items:
        orderedItemsString += element['name']+ '(' + str(element['qty']) + '),'
    orderedItemsString = orderedItemsString.rstrip(',')
        
    messageString = 'New Ordered Recived from ' + customer_name + '(' + customer_phone + '). Ordered Items \n' + orderedItemsString + '\n' + 'Delivery Address: ' + customer_addr;
    return messageString;


def date_from_string(date_str):
    components_of_date = date_str.split('/')
    year = int(components_of_date[2])
    month = int(components_of_date[1])
    day = int(components_of_date[0])
    return date(year,month,day)