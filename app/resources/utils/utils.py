def get_parameters(request):
    try:
        return {'page': int(request.get('page')), 'search': request.get('search'), 'active': request.get('active')}
    except Exception:
        return {'page': int(1), 'search': '', 'active': 'nope'}


def get_filters(parameters):
    if (bool(parameters['search'] != '') & bool(parameters['active'] != 'nope')):
        return {'search': parameters['search'], 'active': int(parameters['active'])}
    elif (parameters['active'] != 'nope'):
        return {'active': int(parameters['active'])}
    elif (bool(parameters['search'] != 'nope')):
        return {'search': parameters['search']}
    return None


def get_dates_parameters(request):
    try:
        return {'from_date': request.get('from_date'), 'to_date': request.get('to_date')}
    except Exception:
        return {'from_date':'', 'to_date':''}


def get_url_parameters(request,array_parameters):
    parameters = {}
    for required_parameter in array_parameters:
        parameters.setdefault(required_parameter,request.get(required_parameter))
    try:
        parameters['page'] = int(parameters['page'])
    except Exception:
        pass
    return parameters


def get_url_parameters_v2(request,array_parameters):
    parameters = {}
    for required_parameter in array_parameters:
        print('parametro: ',required_parameter)
        parameters.setdefault(required_parameter,request.get(required_parameter))
    return parameters


def get_activate_filter(parameters):
    keys = list(parameters.keys())
    for parameter in keys:
        if parameters[parameter] != 'none' and parameter != 'page' :
            return { parameter: parameters[parameter] }
    return None 
