from sqlalchemy import Column, String, create_engine, Integer, BigInteger, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://newuser:newuser@localhost:3306/data_erp')


def init_connect():
    global engine

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    session = DBSession()

    return session


def operation_complete(session):
    session.commit()
    session.close()


# 定义User对象:
class Company(Base):
    # 表的名字:
    __tablename__ = 'company'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), comment='公司名称')  # 公司名称
    phone = Column(String(255), comment='公司电话')  # 公司电话
    more_phone = Column(String(255), comment='更多电话')  # 更多电话
    status_quo = Column(String(20), comment='公司经营状态')  # 公司经营状态
    trademark_info = Column(String(50), comment='商标信息')  # 商标信息
    registered_capital = Column(String(100), comment='注册资本')  # 注册资本
    date_of_establishment = Column(String(50), comment='成立日期')  # 成立日期
    email = Column(String(255), comment='邮箱')  # 邮箱
    more_email = Column(String(255), comment='更多邮箱')  # 更多邮箱
    address = Column(String(255), comment='公司地址')  # 公司地址
    introduction = Column(String(1000), comment='公司介绍')  # 公司介绍
    register_address = Column(String(255), comment='注册地址')  # 注册地址
    business_scope = Column(String(1000), comment='经营范围')  # 经营范围
    industry = Column(String(100), comment='行业')  # 行业
    staff_size = Column(String(255), comment='人员规模')  # 人员规模
    former_name = Column(String(255), comment='曾用名')  # 曾用名
    business_term = Column(String(255), comment='营业期限')  # 营业期限
    date_of_approval = Column(String(255), comment='审核日期')  # 审核日期
    company_type = Column(String(255), comment='公司类型')  # 公司类型
    legal_representative = Column(String(50), comment='法定代表人')  # 法定代表人
    shareholder_information = Column(String(255), comment='股东信息')  # 股东信息
    province = Column(String(20), comment='省份')
    city = Column(String(50), comment='市区')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = init_connect()
    operation_complete(session)
