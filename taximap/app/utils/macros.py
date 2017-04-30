# Given a comma separated string, split on the comma
# and trim any whitespace with rstrip(). For example:
# '    test@gmail.com,      hello  ' turns into
# ['test@gmail.com', 'hello']
import datetime
import pytz
import uuid
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app, request
from flask_login import current_user


def split_on_comma_and_trim(str):
    str_arr = []
    for s in str.split(','):
        str_arr.append(s.rstrip().lstrip())

    # Delete any empty strings from the list.
    str_arr = filter(None, str_arr)
    return str_arr


def byteify(input):
    """ convert the unicode string in json into string
    """
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def format_date(date):
    return str(date)


def format_date_thedaybefore(date):
    return format_date(date - datetime.timedelta(days=1))


def check_date(ticket, timezone):
    if ticket.start_date <= datetime.datetime.now(pytz.timezone(timezone)).date() <= ticket.end_date:
        return True
    else:
        return False


def timestamp():
    return datetime.date.today()


def product_has_sold(product):
    '''
    check if the product has been sold
    '''
    for product_option in product.options.all():
        if product_option.number_of_sold:
            return True
    return False


def generate_uuid(length=32):
    assert length > 1, ValueError
    return str(uuid.uuid4())[0:length]


def generate_timeout_token():
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'redirect': request.url, 'email': current_user.email})


def get_from_timeout_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return {}
    return data


def datetime_now_string():
    '''Convert current time to string
    return string like Jun 1 2005  1:33PM
    '''
    return datetime.datetime.now().strftime('%b %d %Y %I:%M%p')
