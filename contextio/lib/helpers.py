from datetime import datetime
import logging
import re

from contextio.lib.errors import ArgumentError

def to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def uncamelize(d):
    drop = []

    for k, v in list(d.items()):
        u = to_underscore(k)
        if u != k and u not in d:
            d[u] = v
            drop.append(k)

    for k in drop:
        del d[k]

    return d


def as_bool(v):
    if v == 0 or v is False:
        return False
    return True


def as_datetime(v):
    if isinstance(v, int):
        return datetime.fromtimestamp(v)


def process_person_info(parent, person_info, addresses):
    try:
        from contextIO2 import Contact
    except ImportError:
        from .__init__ import Contact
    contacts = {}
    to_addrs = []
    to_contacts = []
    from_addr = None
    from_contact = None

    if 'to' in addresses:
        for info in addresses['to']:
            person_info[info.get('email')].setdefault('name', info.get('name'))
            to_addrs.append(info.get('email'))

    info = addresses['from']
    person_info[info.get('email')].setdefault('name', info.get('name'))
    from_addr = info.get('email')

    for addr, d in list(person_info.items()):
        info = {
            'email': addr,
            'thumbnail': d.get('thumbnail'),
            'name': d.get('name')
        }
        c = Contact(parent, info)
        contacts.setdefault(addr, c)

        if addr in to_addrs:
            to_contacts.append(c)
            to_addrs.remove(addr)

        elif addr == from_addr:
            from_contact = c

    return contacts, to_contacts, from_contact


def sanitize_params(params, all_args, required_args=None):
    """Removes parameters that aren't valid.

    Required Arguments:
        params: dict - key/value pairs of arguments
        all_args: list - list of strings, each string is a
            valid parameter.

    Optional Args:
        required_arguments: list - ironically, required_arguments is an
            optional argument here. a list of string, each string is a
            required argument.

    Returns:
        dictionary of key, value pairs of valid parameters.
    """
    if required_args:
        # check to be sure we have all the required params
        missing_required_args = []
        for required_arg in required_args:
            param = params.get(required_arg)
            if param == None:
                missing_required_args.append(required_arg)

        # yell if we're missing a required argument
        if missing_required_args:
            raise ArgumentError("Missing the following required arguments: {0}".format(
                ", ".join(missing_required_args)))

    # remove any arguments not recognized
    cleaned_args = {}
    for key, val in params.items():
        if key in all_args and val is not None:
            cleaned_args[key] = val
        elif key in all_args and val is None:
            logging.warning("Invalid arguments found: None was passed in for '{0}'".format(key))
        else:
            logging.warning("Invalid arguments found: '{0}'".format(key))

    return cleaned_args

def check_for_account_credentials(argument_dict):
    if "password" in argument_dict or "provider_refresh_token" in argument_dict and "provider_consumer_key" in argument_dict:
        return True
    else:
        raise ArgumentError(
            "You must provide either a 'password' or a 'provider_refresh_token'"
            " and a 'provider_consumer_key'")
