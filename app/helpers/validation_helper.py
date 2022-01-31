import re

def validate_email(email):
    
    # Old regex '^[a-z0-9]+[\._]?[-z0-9]+[@]\w+[.]\w{2,3}$'
    regex_email = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return True if ( re.search(regex_email, email) ) else False

def validate_phone(phone):
    regex_phone = '^[0-9]*$'
    return True if ( re.search(regex_phone, phone) ) else False

def validate_meetingspot_parameters(parameters):
    
    result = { 'message': 'El punto de encuentro fue agregado con éxito', 'category':'success', 'valid': True  }
    
    #Validate mail
    if (parameters['email']):
        if (not validate_email(parameters['email'])):
            result['message'] = 'El formato de email no es válido'
            result['category'] = 'error'
            result['valid'] = False
            return result

    #Validate phone (*)
    if (parameters['phone']):
        if (not validate_phone(parameters['phone'])):
            result['message'] = 'El formato de telefono no es válido'
            result['category'] = 'error'
            result['valid'] = False
            return result
    else:
        result['message'] = 'El telefono es un campo requerido.' 
        result['category'] = 'error'
        result['valid'] = False
        return result  

    return result

def validate_evacuation_route_parameters(parameters):
    
    result = { 'message': 'El recorrido de evacuacion fue agregado con éxito', 'category':'success', 'valid': True  }
    
    if (not parameters['name']):
        result['message'] = 'El nombre del recorrido de evacuación es obligatorio!'
        result['category'] = 'error'
        result['valid'] = False
        return result

    if (not parameters['description']):
        result['message'] = 'La descripción del recorrido de evacuación es obligatoria!'
        result['category'] = 'error'
        result['valid'] = False
        return result

    return result

def validate_coordinates(arreglo_coordenadas):
    
    result = { 'message': 'El recorrido de evacuacion fue agregado con éxito', 'category':'success', 'valid': True  }
    
    if (not arreglo_coordenadas):
        result['message'] = 'Las coordenadas son obligatorias!'
        result['category'] = 'error'
        result['valid'] = False
        return result
    
    for i in range(0,len(arreglo_coordenadas),1):
        print('recorriendo for con coordenada en i: ',arreglo_coordenadas[i])
        print('research: ',re.search('[a-zA-Z]', arreglo_coordenadas[i]))
        if (re.search('[a-zA-Z]', arreglo_coordenadas[i])):
            result['message'] = 'Las coordenadas no pueden contener letras!'
            result['category'] = 'error'
            result['valid'] = False
            return result

    return result

def validate_denunciation_parameters(parameters):
    
    result = { 'message': 'La denuncia fue agregada con éxito', 'category':'success', 'valid': True  }
    
    #Validate email
    if (parameters['email_d']):
        if (not validate_email(parameters['email_d'])):
            result['message'] = 'El formato de email no es válido'
            result['category'] = 'error'
            result['valid'] = False
            return result
    else:
        result['message'] = 'El email del denunciante es un campo requerido.' 
        result['category'] = 'error'
        result['valid'] = False
        return result

    #Validate phone (*)
    if (parameters['phone_d']):
        if (not validate_phone(parameters['phone_d'])):
            result['message'] = 'El formato de telefono no es válido'
            result['category'] = 'error'
            result['valid'] = False
            return result
    else:
        result['message'] = 'El telefono del denunciante es un campo requerido.' 
        result['category'] = 'error'
        result['valid'] = False
        return result  

    #Validate coordinates (*)
    if (not parameters['latitude']):
        result['message'] = 'La latitud del punto de denuncia es un campo requerido!'
        result['category'] = 'error'
        result['valid'] = False
        return result

    if (not parameters['longitude']):
        result['message'] = 'La longitud del punto de denuncia es un campo requerido!'
        result['category'] = 'error'
        result['valid'] = False
        return result
    
    #Validate title (*)
    if (not parameters['title']):
        result['message'] = 'El titulo es un campo requerido!'
        result['category'] = 'error'
        result['valid'] = False
        return result
    
    #Validate lastName (*)
    if (not parameters['last_name_d']):
        result['message'] = 'El apellido del denunciante es un campo requerido!'
        result['category'] = 'error'
        result['valid'] = False
        return result

    #Validate firstName (*)
    if (not parameters['first_name_d']):
        result['message'] = 'El nombre del denunciante es un campo requerido!'
        result['category'] = 'error'
        result['valid'] = False
        return result

    return result