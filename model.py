from table import Company, init_connect, operation_complete


def create(**kwargs):

    company = Company(
        company_name=kwargs.get('company_name', ''),
        phone=kwargs.get('phone', ''),
        status_quo=kwargs.get('status_quo', ''),
        trademark_info=kwargs.get('trademark_info', ''),
        registered_capital=kwargs.get('registered_capital', ''),
        date_of_establishment=kwargs.get('date_of_establishment', ''),
        email=kwargs.get('email', ''),
        address=kwargs.get('address', ''),
        introduction=kwargs.get('introduction', ''),
        register_address=kwargs.get('register_address', ''),
        business_scope=kwargs.get('business_scope', ''),
        industry=kwargs.get('industry', ''),
        staff_size=kwargs.get('staff_size', ''),
        former_name=kwargs.get('former_name', ''),
        business_term=kwargs.get('business_term', ''),
        date_of_approval=kwargs.get('date_of_approval', ''),
        company_type=kwargs.get('company_type', '')
    )
    session = init_connect()
    session.add(company)
    operation_complete(session)

