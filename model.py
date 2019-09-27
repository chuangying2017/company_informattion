from table import Company, init_connect, operation_complete, Citys


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
        company_type=kwargs.get('company_type', ''),
        legal_representative=kwargs.get('legal_representative', '')
    )
    session = init_connect()
    session.add(company)
    operation_complete(session)


def data(kwargs: dict):
    return Company(
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
        company_type=kwargs.get('company_type', ''),
        legal_representative=kwargs.get('legal_representative', ''),
        the_social_code=kwargs.get('the_social_code', ''),
        registration_number=kwargs.get('registration_number', ''),
        register_number=kwargs.get('register_number', ''),
        organizing_institution_bar_code=kwargs.get('organizing_institution_bar_code', ''),
        contributors_in=kwargs.get('contributors_in', ''),
        type_of_business=kwargs.get('type_of_business', ''),
        web_url=kwargs.get('web_url', '')
    )


def create_all(datas: list = []) -> bool:
    ls = []
    for lb in datas:
        ls.append(data(lb))
    session = init_connect()
    session.add_all(ls)
    operation_complete(session)
    return True


def get_city() -> list:
    session = init_connect()
    all_ = list(map(lambda x: x.city, session.query(Citys).all()))
    operation_complete(session)
    return all_



