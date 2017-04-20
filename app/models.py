# coding:utf-8
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
import config
from werkzeug.security import generate_password_hash


# 数据库映射文件
# 报警邮件数据库映射
class EmailInfo(db.Model):
	__tablename__ = 'einfo'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	emailname = db.Column(db.String(30))
	emailtime = db.Column(db.Integer)
	identifier = db.Column(db.String(30), unique=True)
	bj1 = db.Column(db.Integer)
	bj2 = db.Column(db.Integer)
	bj3 = db.Column(db.Integer)
	bj4 = db.Column(db.Integer)
	bj5 = db.Column(db.Integer)
	ctime = db.Column(db.Integer)


# 代码发布统计数据库映射文件
class CodeInfo(db.Model):
	__tablename__ = 'codeinfo'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	emailname = db.Column(db.String(30))
	emailtime = db.Column(db.Integer)
	identifier = db.Column(db.String(30), unique=True)
	bjsl = db.Column(db.Integer)
	ctime = db.Column(db.Integer)


# 用户映射文件
class UserInfo(db.Model):
	__tablename__ = 'userinfo'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), nullable=False, index=True)
	password = db.Column(db.String(128), nullable=False)

	# -----------------password加密 解密 token生成 验证-----------------------
	def hash_password(self, password):
		self.password = generate_password_hash(password)

	def verify_password(self, password_hash):
		return pwd_context.verify(self.password, password_hash)

	def generate_testhome_token(self, expiration=3600):
		s = Serializer(config.SECRET_KEY, expires_in=expiration)
		return s.dumps({'name': self.name})

	def verify_testhome_token(self, token):
		s = Serializer(config.SECRET_KEY)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		return data['name'] == self.name


# Jenkins项目名映射文件
class ProjectInfo(db.Model):
	__tablename__ = 'projectinfo'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), nullable=False, index=True)


# 日报数据库模板
class DailyInfo(db.Model):
	__tablename__ = 'dailyinfo'
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.Integer)
	dailyName = db.Column(db.String(32), nullable=False)
	dailyCont = db.Column(db.String(1024), nullable=False)
	type = db.Column(db.String(128), default='未审核')
	username = db.Column(db.String(32))


# 周报数据库模板
class WeeklyInfo(db.Model):
	__tablename__ = 'weeklyinfo'
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.Integer)
	weeklyName = db.Column(db.String(32), nullable=False)
	weeklyCont = db.Column(db.String(1024), nullable=False)
	type = db.Column(db.String(128), default='未审核')
	username = db.Column(db.String(32))
