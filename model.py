from table import Company, init_connect, operation_complete


if __name__ == '__main__':
    company = Company(company_name='长隆欢乐谷', phone='13059551109', email='631711487@qq.com')
    session = init_connect()
    data: list = []
    for i in range(10):
        data.append(Company(company_name='长隆欢乐谷', phone='13059551109', email='631711487@qq.com'))
    print(data)
    session.add_all(data)
    operation_complete(session)
    print('successfully operation complete')
