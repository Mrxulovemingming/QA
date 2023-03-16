# 配置 SECRET_KEY
SECRET_KEY ="afeasdfghjkghn"

# MySQL 所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL 监听的端口号，默认3306
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
# 这里的数据库为用户自己创建的数据库名
DATABASE = "qa"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = "961592690@qq.com"
MAIL_PASSWORD = "zartglebxcjibbhh"
MAIL_DEFAULT_SENDER = "961592690@qq.com"
