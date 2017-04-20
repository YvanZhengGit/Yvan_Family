# coding:utf-8
import shutil

import werkzeug
from flask import jsonify, session, make_response
from sqlalchemy import and_, func, distinct
from . import testhome
from .forms import searchForm, codeReleaseForm
from ..models import EmailInfo, CodeInfo, UserInfo, ProjectInfo, DailyInfo, WeeklyInfo
from .. import db, babel
from config import LANGUAGES
from flask import Flask, request, render_template, redirect
import xlwt, xlrd, re, datetime, time, os
from xml.dom.minidom import parse
from xml.dom.minidom import Document
import xml.dom.minidom, logging
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(LANGUAGES.keys())


# -----------------------------日报系统-------------------------------
@testhome.route('/daily', methods=['GET', 'POST'])
def daily():
	return render_template('dailys/daily.html', u=session['username'], title=u'日报系统')


# 添加日报
@testhome.route('/addDaily', methods=['GET', 'POST'])
def addDaily():
	return render_template('dailys/addDaily.html', u=session['username'], title=u'日报系统')


@testhome.route('/add_daily', methods=['GET', 'POST'])
def add_daily():
	if request.method == 'POST':
		dailyName = request.form['dailyName']
		dailyCont = request.form['dailyCont']
		times = int(time.time())
		if dailyName is not None or dailyCont is not None:
			daily = DailyInfo(dailyName=dailyName, dailyCont=dailyCont, time=times, username=session['username'])
			db.session.add(daily)
			db.session.commit()
			return redirect('testhome/showDaily')
		else:
			return render_template('dailys/adddaily.html', title=u'测试中心')
	return render_template('dailys/adddaily.html', title=u'测试中心')


# 日报分页展示
@testhome.route('/showDaily', methods=['GET', 'POST'])
def showDaily():
	return redirect('testhome/showDaily/info/1')


@testhome.route('/showDaily/info/<int:page>')
def show_pages(page):
	_g = page
	if session['username'] == 'admin':
		pagination = DailyInfo.query.filter(DailyInfo.id > 0).paginate(
			page=_g, per_page=5, error_out=False)
	elif session['username'] != 'admin':
		pagination = DailyInfo.query.filter(DailyInfo.username == session['username']).paginate(
			page=_g, per_page=5, error_out=False)
	posts = pagination.items
	for i in posts:
		t = time.localtime(float(str(i.time)))
		i.newtime = time.strftime('%Y-%m-%d', t)
	return render_template('dailys/showDaily.html', u=session['username'], infos=posts, pagination=pagination)


# 删除日报
@testhome.route('/delDaily/<int:num>', methods=['GET', 'POST'])
def delDaily(num):
	_n = num
	data = DailyInfo.query.filter_by(id=_n).first()
	db.session.delete(data)
	db.session.commit()
	return redirect('testhome/showDaily')


# 修改日报
@testhome.route('/updateDaily/<int:num>', methods=['GET', 'POST'])
def updateDaily(num):
	_n = num
	data = DailyInfo.query.filter_by(id=_n).first()
	return render_template('dailys/updateDaily.html', u=session['username'], info=data, title=u'日报系统')


@testhome.route('/update_daily', methods=['GET', 'POST'])
def updatedaily():
	id = request.form['id']
	data = DailyInfo.query.filter_by(id=id).first()
	data.dailyName = request.form['dailyName']
	data.dailyCont = request.form['dailyCont']
	return redirect('testhome/showDaily')


# 条件查询日报
@testhome.route('/findDaily', methods=['GET', 'POST'])
def findDaily():
	dtime = request.form['datetime']
	if dtime != '':
		dtime = int(time.mktime(time.strptime(request.form['datetime'], '%Y-%m-%d')))
	if dtime == '':
		ttime = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
		dtime = int(time.mktime(time.strptime(ttime, '%Y-%m-%d')));
	s_time = dtime
	e_time = s_time+60*60*24
	if session['username'] == 'admin':
		data = DailyInfo.query.filter(DailyInfo.time >= s_time, DailyInfo.time <= e_time)
	elif session['username'] != 'admin':
		data = DailyInfo.query.filter(DailyInfo.time >= s_time, DailyInfo.time <= e_time, DailyInfo.username == session['username'])
	print data
	return render_template('dailys/selectDaily.html', u=session['username'], infos=data, datetime=datetime)


# 日报详情
@testhome.route('/showDetails/<int:num>', methods=['GET', 'POST'])
def showDetails(num):
	_n = num
	data = DailyInfo.query.filter_by(id=_n).first()
	return render_template('dailys/showDetails.html', u=session['username'], info=data)


# -----------------------------周报系统------------------------------
@testhome.route('/weekly', methods=['GET', 'POST'])
def weekly():
	return render_template('weeklys/weekly.html', u=session['username'], title=u'日报系统')


# 添加周报
@testhome.route('/addWeekly', methods=['GET', 'POST'])
def addWeekly():
	return render_template('weeklys/addWeekly.html', u=session['username'], title=u'日报系统')


@testhome.route('/add_weekly', methods=['GET', 'POST'])
def add_weekly():
	if request.method == 'POST':
		weeklyName = request.form['weeklyName']
		weeklyCont = request.form['weeklyCont']
		times = int(time.time())
		if weeklyName is not None or weeklyCont is not None:
			weekly = WeeklyInfo(weeklyName=weeklyName, weeklyCont=weeklyCont, time=times, username=session['username'])
			db.session.add(weekly)
			db.session.commit()
			return redirect('testhome/showWeekly')
		else:
			return render_template('weeklys/addWeekly.html', title=u'测试中心')
	return render_template('weeklys/addWeek.html', title=u'测试中心')


# 周报分页展示
@testhome.route('/showWeekly', methods=['GET', 'POST'])
def showWeekly():
	return redirect('testhome/showWeekly/info/1')


@testhome.route('/showWeekly/info/<int:page>')
def show_Weekly(page):
	_g = page
	if session['username'] == 'admin':
		pagination = WeeklyInfo.query.filter(WeeklyInfo.id > 0).paginate(
			page=_g, per_page=5, error_out=False)
	elif session['username'] != 'admin':
		pagination = WeeklyInfo.query.filter(WeeklyInfo.username == session['username']).paginate(
			page=_g, per_page=5, error_out=False)
	posts = pagination.items
	for i in posts:
		t = time.localtime(float(str(i.time)))
		i.newtime = time.strftime('%Y-%m-%d', t)
	return render_template('weeklys/showWeekly.html', u=session['username'], infos=posts, pagination=pagination)


# 删除周报
@testhome.route('/delWeekly/<int:num>', methods=['GET', 'POST'])
def delWeekly(num):
	_n = num
	data = WeeklyInfo.query.filter_by(id=_n).first()
	db.session.delete(data)
	db.session.commit()
	return redirect('testhome/showWeekly')


# 修改周报
@testhome.route('/updateWeekly/<int:num>', methods=['GET', 'POST'])
def updateWeekly(num):
	_n = num
	print _n
	data = WeeklyInfo.query.filter_by(id=_n).first()
	return render_template('weeklys/updateWeekly.html', u=session['username'], info=data, title=u'日报系统')


@testhome.route('/update_weekly', methods=['GET', 'POST'])
def update_Weekly():
	id = request.form['id']
	data = WeeklyInfo.query.filter_by(id=id).first()
	data.weeklyName = request.form['weeklyName']
	data.weeklyCont = request.form['weeklyCont']
	return redirect('testhome/showWeekly')


# # 条件查询周报
# @testhome.route('/findWeekly', methods=['GET', 'POST'])
# def findWeekly():
# 	dtime = request.form['datetime']
# 	if dtime != '':
# 		dtime = int(time.mktime(time.strptime(request.form['datetime'], '%Y-%m-%d')))
# 	if dtime == '':
# 		ttime = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
# 		dtime = int(time.mktime(time.strptime(ttime, '%Y-%m-%d')));
# 	s_time = dtime
# 	e_time = s_time+60*60*24
# 	if session['username'] == 'admin':
# 		data = WeeklyInfo.query.filter(WeeklyInfo.time >= s_time, WeeklyInfo.time <= e_time)
# 	elif session['username'] != 'admin':
#       data = WeeklyInfo.query.filter(WeeklyInfo.time >= s_time, WeeklyInfo.time <= e_time, WeeklyInfo.username == session['username'])
# 	print data
# 	return render_template('weeklys/selectWeekly.html', u=session['username'], infos=data, datetime=datetime)


# 周报详情
@testhome.route('/showWDetails/<int:num>', methods=['GET', 'POST'])
def showWDetails(num):
	_n = num
	data = WeeklyInfo.query.filter_by(id=_n).first()
	return render_template('weeklys/showWDetails.html', u=session['username'], info=data)


# -------------------------logging 日志统计--------------------------
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y %H:%M:%S',
					filename='logs/pro.log', filemode='w')


# ---------------------------登录验证--------------------------------
@testhome.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username in session and password in session:
			return render_template('index.html', u=username, title=u'测试中心登录')
		if username is not None or password is not None:
			datas = UserInfo.query.filter_by(username=username).first()
			if datas is not None and werkzeug.security.check_password_hash(datas.password, password):
				timeArray = time.localtime(int(time.time()))
				otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
				logging.debug(username + '登录' + otherStyleTime)
				session['username'] = request.form['username']
				session['password'] = request.form['password']
				resp = make_response(render_template('index.html', foo=42))
				resp.set_cookie('username', 'the username')
				return render_template('index.html', u=username, title=u'测试中心登录')
		else:
			return render_template('login.html', title=u'测试中心登录')
	return render_template('login.html', title=u'测试中心登录')


# ------------------------------用户注册-----------------------------
@testhome.route('/regist', methods=['GET', 'POST'])
def regist():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username is not None or password is not None:
			user = UserInfo(username=username, password=password)
			user.hash_password(password)
			db.session.add(user)
			db.session.commit()
			return render_template('login.html', title=u'测试中心')
		else:
			return render_template('register.html', title=u'测试中心')
	return render_template('register.html', title=u'测试中心')


# -------------------------- index首页 -----------------------------
@testhome.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html', u=session['username'], title=u'测试中心登录')


# -------------------------- Xml and Excel ------------------------
@testhome.route('/Xml_Excel', methods=['GET', 'POST'])
def Xml_Excel():
	return render_template('Xml_Excel.html', u=session['username'], title=u'测试中心登录')


# -----------------------Excel To Xml------------------------------
# Excel 转 Xml方法
_status = {
	"p1": "3",
	"p2": "2",
	"p3": "1"
}

_l = []
_suite = []
_dict = {}
_r = ''

_status2 = {
	"3": "p1",
	"2": "p2",
	"1": "p3"
}


def split_step(r, ty):
	if ty == "step":
		p = re.compile(r'step\d: ')
	else:
		p = re.compile(r'result\d: ')
	_l = []
	for i in p.split(r)[1:]:
		_l.append(i.replace('\n', ''))
	return _l


def set_style(name, height, bold=False):
	style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = name
	font.bold = bold
	font.color_index = 4
	font.height = height
	style.font = font

	return style


def ex(path):
	data = xlrd.open_workbook(path)
	print data
	table = data.sheet_by_index(0)
	print table
	nrows = table.nrows

	for i in range(nrows):
		if i == 0:
			pass
		else:
			if len(table.row_values(i)[0]) != 0:
				_suite.append(table.row_values(i)[0])
	print _suite

	for i in _suite:
		_dict[i] = []

	print _dict
	print "dao zhe le"
	for i in range(nrows):
		_d = {}
		if i == 0:
			pass
		elif i == 1:
			print i
			if len(table.row_values(i)[0]) == 0:
				raise Exception(u'表格错误')
			else:
				_d['suite'] = table.row_values(i)[0]
				_d['name'] = table.row_values(i)[1]
				_d['summary'] = table.row_values(i)[2]
				_d['preconditions'] = ""
				step = split_step(table.row_values(i)[3], "step")
				result = split_step(table.row_values(i)[4], "result")
				_d['step'] = step
				_d['result'] = result
				_d['importance'] = _status[table.row_values(i)[5]]
				_r = _d['suite']
				_l.append(_d)
		else:
			if len(table.row_values(i)[0]) == 0:
				_d['suite'] = _r
				_d['name'] = table.row_values(i)[1]
				_d['summary'] = table.row_values(i)[2]
				_d['preconditions'] = ""
				step = split_step(table.row_values(i)[3], "step")
				result = split_step(table.row_values(i)[4], "result")
				_d['step'] = step
				_d['result'] = result
				_d['importance'] = _status[table.row_values(i)[5]]
				_l.append(_d)
			else:
				_d['suite'] = table.row_values(i)[0]
				_d['name'] = table.row_values(i)[1]
				_d['summary'] = table.row_values(i)[2]
				_d['preconditions'] = ""
				step = split_step(table.row_values(i)[3], "step")
				result = split_step(table.row_values(i)[4], "result")
				_d['step'] = step
				_d['result'] = result
				_d['importance'] = _status[table.row_values(i)[5]]
				_r = _d['suite']
				_l.append(_d)
	print _l

	for j in _l:
		for k in _suite:
			if j['suite'] == k:
				_dict[k].append(j)

	print _dict
	return _dict  # - 上面 实现了  讲excel数据解析


def ex2(path, d):
	doc = Document()
	testsuite = doc.createElement('testsuite')
	doc.appendChild(testsuite)
	for _s in _suite:
		suite = doc.createElement('testsuite')
		suite.setAttribute('name', _s)
		testsuite.appendChild(suite)
		for _t in d[_s]:
			testcase = doc.createElement('testcase')
			print _t['name']
			testcase.setAttribute('name', _t['name'])
			steps = doc.createElement('steps')
			for _x in range(len(_t['step'])):
				step = doc.createElement('step')
				step_number = doc.createElement('step_number')
				step_number_v = doc.createTextNode(str(int(_x) + 1))
				step_number.appendChild(step_number_v)
				step.appendChild(step_number)
				actions = doc.createElement('actions')
				actions_v = doc.createTextNode(_t['step'][_x])
				actions.appendChild(actions_v)
				step.appendChild(actions)
				expectedresults = doc.createElement('expectedresults')
				expectedresults_v = doc.createTextNode(_t['result'][_x])
				expectedresults.appendChild(expectedresults_v)
				step.appendChild(expectedresults)
				execution_type = doc.createElement('execution_type')
				execution_type_v = doc.createTextNode('1')
				execution_type.appendChild(execution_type_v)
				step.appendChild(execution_type)
				steps.appendChild(step)
			summary = doc.createElement("summary")
			summary_v = doc.createTextNode(_t['summary'])
			summary.appendChild(summary_v)
			preconditions = doc.createElement("preconditions")
			preconditions_v = doc.createTextNode(_t['preconditions'])
			preconditions.appendChild(preconditions_v)
			testcase.appendChild(steps)
			testcase.appendChild(summary)
			testcase.appendChild(preconditions)
			suite.appendChild(testcase)

	_filename = path.split('/')[-1] + '.xml'
	print _filename
	f = open('/usr/local/openresty/nginx/html/xml/' + _filename, 'w+')
	f.write(doc.toprettyxml(indent=''))
	print f
	print '-----------'
	f.close()


# Xml 转 Excel方法
def xe(path):
	DOMTree = xml.dom.minidom.parse(path)
	print DOMTree;
	collection = DOMTree.documentElement
	if collection.hasAttribute("shelf"):
		print "Root element : %s" % collection.getAttribute("shelf")

	testsuite = collection.getElementsByTagName("testsuite")
	_f = xlwt.Workbook()
	_sheet1 = _f.add_sheet('total')
	row0 = [u'编号', u'模块', u'名称', u'摘要', u'前提', u'步骤', u'预期结果', u'级别']
	for r in range(len(row0)):
		_sheet1.write(0, r, row0[r], set_style(u'宋体', 220, True))

	_num = 1
	for tc in testsuite:
		for t in tc.getElementsByTagName("testcase"):
			_l = []
			if t.hasAttribute("internalid"):
				_l.append(t.getAttribute("internalid"))
			_l.append(tc.getAttribute("name"))
			if t.hasAttribute("name"):
				_l.append(t.getAttribute("name"))
			summary = t.getElementsByTagName('summary')[0]
			if len(summary.childNodes) != 0:
				_l.append(summary.childNodes[0].data.replace(' ', '').replace('<p>', '').replace('</p>', ' ').strip())
			else:
				_l.append('Null')
			preconditions = t.getElementsByTagName('preconditions')[0]
			if len(preconditions.childNodes) != 0:
				_l.append(
					preconditions.childNodes[0].data.replace(' ', '').replace('<p>', '').replace('</p>', ' ').strip())
			else:
				_l.append('Null')
			steps = t.getElementsByTagName('steps')

			if len(steps) == 1:
				step = steps[0].getElementsByTagName('step')
				_step = ""
				_result = ""
				for j in step:
					num = j.getElementsByTagName('step_number')[0].childNodes[0].data \
						.replace(' ', '').replace('<p>', '').replace('</p>', '').strip()
					actions = j.getElementsByTagName('actions')[0].childNodes[0].data \
						.replace(' ', '').replace('<p>', '').replace('</p>', '').strip()
					expectedresults = j.getElementsByTagName('expectedresults')[0].childNodes[0].data \
						.replace(' ', '').replace('<p>', '').replace('</p>', '').strip()
					_step += "step" + num + ":" + actions + ""
					_result += "result" + num + ":" + expectedresults + ""
				_l.append(_step)
				_l.append(_result)
			status = t.getElementsByTagName('importance')[0]
			if len(status.childNodes) != 0:
				_l.append(_status2[str(status.childNodes[0].data.replace(' ', '').replace('<p>', '').replace('</p>', ' ').strip())])
			else:
				_l.append('Null')
			for j in range(0, len(_l)):
				style = xlwt.easyxf('align: wrap on')
				_sheet1.write(_num, j, _l[j], style)
			_num += 1
	_filename = path.split('/')[-1] + ".xls"
	filepath = '/usr/local/openresty/nginx/html/excel/' + _filename
	_f.save(filepath)


# excel文件上传
@testhome.route('/selupload', methods=['GET', 'POST'])
def selupload():
	return render_template('excel_to_xml.html', u=session['username'], title=u'蜜蜂汇金邮件报警系统')


# xml文件上传
@testhome.route('/seluploadexcel', methods=['GET', 'POST'])
def seluploadexcel():
	return render_template('xml_to_excel.html', u=session['username'], title=u'蜜蜂汇金邮件报警系统')


_p = os.path.abspath('.')
UPLOAD_FOLDER = _p + "/app/upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'xls', 'doc', 'docx', 'xml'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# excel执行转换
@testhome.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		_file = request.files['file']
		print _file
		if _file and allowed_file(_file.filename):
			_file.save(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
			print app.config['UPLOAD_FOLDER']
			_dict = ex(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
			ex2(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename), _dict)
		return redirect('/testhome/show_upload')


# xml执行转换
@testhome.route('/uploadexcel', methods=['GET', 'POST'])
def uploadexcel():
	if request.method == 'POST':
		_file = request.files['file']
		if _file and allowed_file(_file.filename):
			_file.save(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
			xe(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
		return redirect('/testhome/show_uploadx')


# xml上传文件展示
@testhome.route('/show_upload', methods=['GET', 'POST'])
def show_upload():
	UPLOAD_FOLDER = '/usr/local/openresty/nginx/html/xml/'
	pathDir = os.listdir(UPLOAD_FOLDER)
	_file = []
	for allDir in pathDir:
		_content = {}
		_content['name'] = (allDir.split('.')[0] + '.xml')
		_content['filepath'] = UPLOAD_FOLDER
		_content['oldmn'] = allDir
		_file.append(_content)
	return render_template('show_xml.html', filecontents=_file, u=session['username'], title=u'蜜蜂汇金邮件报警系统')


# excel上传文件展示
@testhome.route('/show_uploadx', methods=['GET', 'POST'])
def show_uploadx():
	UPLOAD_FOLDER = '/usr/local/openresty/nginx/html/excel/'
	pathDir = os.listdir(UPLOAD_FOLDER)
	_file = []
	for allDir in pathDir:
		_content = {}
		_content['name'] = (allDir.split('.')[0] + '.excel')
		_content['filepath'] = UPLOAD_FOLDER
		_content['oldmn'] = allDir
		_file.append(_content)
	return render_template('show_excel.html', filecontents=_file, u=session['username'], title=u'蜜蜂汇金邮件报警系统')


# 清空xml文件
@testhome.route('/clearxml', methods=['GET', 'POST'])
def clear():
	rootdir = '/usr/local/openresty/nginx/html/xml/'
	filelist = os.listdir(rootdir)
	for f in filelist:
		filepath = os.path.join(rootdir, f)
		if os.path.isfile(filepath):
			os.remove(filepath)
		elif os.path.isdir(filepath):
			shutil.rmtree(filepath, True)
	return render_template('index.html', u=session['username'], title=u'蜜蜂汇金邮件报警系统')


# 清空excel文件
@testhome.route('/clearexcel', methods=['GET', 'POST'])
def clearexcel():
	rootdir = '/usr/local/openresty/nginx/html/excel/'
	filelist = os.listdir(rootdir)
	for f in filelist:
		filepath = os.path.join(rootdir, f)
		if os.path.isfile(filepath):
			os.remove(filepath)
		elif os.path.isdir(filepath):
			shutil.rmtree(filepath, True)
	return render_template('index.html', u=session['username'], title=u'蜜蜂汇金邮件报警系统')


# 清理一条XML文件
@testhome.route('/clearxmlone/', methods=['GET', 'POST'])
def clearxmlone():
	rootdir = '/usr/local/openresty/nginx/html/xml/'
	filedir = request.form['username']
	filelist = os.listdir(rootdir)
	for f in filelist:
		if f == filedir:
			os.remove('/usr/local/openresty/nginx/html/xml/' + f)
	return redirect('/testhome/show_upload')


# 清理一条EXCEL文件
@testhome.route('/clearexcelone/', methods=['GET', 'POST'])
def clearexcelone():
	rootdir = '/usr/local/openresty/nginx/html/excel/'
	filedir = request.form['username']
	filelist = os.listdir(rootdir)
	for f in filelist:
		if f == filedir:
			os.remove('/usr/local/openresty/nginx/html/excel/' + f)
	return redirect('/testhome/show_uploadx')


# excel to xml使用说明
@testhome.route('/uesxml/', methods=['POST', 'GET'])
def uesxml():
	return render_template('usexml.html', u=session['username'], title=u'蜜蜂汇金QA平台excel to xml使用说明')


# excel to xml使用说明
@testhome.route('/uesexcel/', methods=['POST', 'GET'])
def uesexcel():
	return render_template('useexcel.html', u=session['username'], title=u'蜜蜂汇金QA平台xml to excel使用说明')


# --------------------------邮件统计——分页展示数据方法----------------
@testhome.route('/search', methods=['GET', 'POST'])
def search():
	form = searchForm()
	if request.method == "POST":
		_t1 = form.start_year.data
		_t2 = form.end_year.data
		_t3 = form.start_month.data
		_t4 = form.end_month.data
		_t5 = form.start_day.data
		_t6 = form.end_day.data
		# if int(_t3) < 10:
		# 	_t3 = '0' + _t3
		# if int(_t4) < 10:
		# 	_t4 = '0' + _t4
		if int(_t5) < 10:
			_t5 = '0' + _t5
		if int(_t6) < 10:
			_t6 = '0' + _t6
		start_time = _t1 + '-' + _t3 + '-' + _t5 + ' 00:00:00'
		end_time = _t2 + '-' + _t4 + '-' + _t6 + ' 00:00:00'
		_d1 = int(str(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))).split('.')[0])
		_d2 = int(str(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))).split('.')[0])
		session['start_time'] = _d1
		session['end_time'] = _d2
		return redirect('testhome/info/1')
	return render_template('searchemail.html', u=session['username'], title=u'蜜蜂汇金邮件报警系统', form=form)


@testhome.route('/info/<int:page>')
def show_page(page):
	_g = page
	pagination = EmailInfo.query.filter(
		and_(EmailInfo.emailtime >= session['start_time'], EmailInfo.emailtime <= session['end_time'])).paginate(
		page=_g, per_page=22, error_out=False)
	posts = pagination.items
	_t = {}
	_t['time'] = time.strftime('%Y-%m-%d', time.localtime(posts[0].__dict__['emailtime']))
	_n = {'bj1': 0, 'bj2': 0, 'bj3': 0, 'bj4': 0, 'bj5': 0}
	for i in posts:
		t = time.localtime(float(str(i.emailtime) + '.0'))
		i.newtime = time.strftime('%Y-%m-%d', t)
		_n['bj1'] = _n['bj1'] + i.bj1
		_n['bj2'] = _n['bj2'] + i.bj2
		_n['bj3'] = _n['bj3'] + i.bj3
		_n['bj4'] = _n['bj4'] + i.bj4
		_n['bj5'] = _n['bj5'] + i.bj5
	return render_template('showemail.html', u=session['username'], pagination=pagination, infos=posts, num=_n, _t=_t)


# -----------------------代码发布——展示方法---------------------------
@testhome.route('/search_code', methods=['GET', 'POST'])
def search_code():
	form = codeReleaseForm()
	if request.method == "POST":
		starttime1 = form.startyear.data + '-' + form.startmonth.data + '-' + '01' + ' 00:00:00'
		starttime = int(str(time.mktime(time.strptime(starttime1, '%Y-%m-%d %H:%M:%S'))).split('.')[0])
		endtime1 = form.endyear.data + '-' + form.endmonth.data + '-' + '01' + ' 00:00:00'
		endtime = int(str(time.mktime(time.strptime(endtime1, '%Y-%m-%d %H:%M:%S'))).split('.')[0])
		datas = CodeInfo.query.filter(and_(CodeInfo.emailtime >= starttime, CodeInfo.emailtime < endtime)).all()
		times = db.session.query(distinct(CodeInfo.emailtime)).filter(
			and_(CodeInfo.emailtime >= starttime, CodeInfo.emailtime < endtime)).all()
		_a = []
		for t in times:
			_s = {}
			_l = []
			for i in datas:
				if i.__dict__['emailtime'] == int(t[0]):
					_l.append(i)
			_s['result'] = _l
			t = time.localtime(float(t[0]))
			t = time.strftime('%Y-%m-%d', t)
			_s['name'] = t
			_a.append(_s)
		_n = {}
		_r = []
		info = [
			'jiaoyudai', 'cuishou', 'jisuanhesuan',
			'chedai', 'huixingyewu', 'fengkong',
			'huixingcaiwu', 'yunwei', 'zhifu', 'fangdai', 'wuxingayi'
		]
		for name in info:
			bjsl = db.session.query(func.sum(CodeInfo.bjsl)).filter(
				and_(CodeInfo.emailname == name, CodeInfo.emailtime >= starttime,
					 CodeInfo.emailtime < endtime)).scalar()
			if bjsl is not None:
				_n[name] = str(bjsl)
			else:
				_n[name] = '0'
		for k in info:
			if _n.has_key(k):
				_r.append(_n[k])
		print _r
		return render_template('showcode.html', u=session['username'], infos=_a, hz=_r)
	return render_template('seach_code.html', u=session['username'], title=u'蜜蜂汇金源码报警系统', form=form)


# ---------------------------Jenkins 项目展示------------------------
@testhome.route('/jenkins', methods=['GET', 'POST'])
def show_jenkins():
	return render_template('show_jenkins.html', u=session['username'], title=u'jenlins项目管理模块')


# -----------------------邮件报警——写入数据方法------------------------
@testhome.route('/insert', methods=['POST'])
def insert():
	data = request.json.get('data')
	Email = {
		"zijintongdao": ["gateway.i.beebank.com"],
		"yunwei": ["sa.beebank.com"],
		"wuxingayi": ["www.wuxingayi.com"],
		"jiaoyudai2": ["jydhx.shendenglicai.com"],
		"qianduan": ["js_exception"],
		"jiaoyudaishendeng": ["jiaoyudai.shendenglicai.com"],
		"rds": ["rds.huixinglicai.com"],
		"CFMS": ["CFMS"],
		"huixing-user": ["user.huixinglicai.com"],
		"huixing-contract": ["contract.huixinglicai.com"],
		"huixing-pay": ["pay.huixinglicai.com"],
		"huixing-loans": ["loans.huixinglicai.com"],
		"huixing-core": ["core-huixing-BC"],
		"heziqiche": ["www.heziqiche.com"],
		"fengkong-spider": ["python_risk_spider"],
		"fengkong-manage": ["riskmanage.beebank.com"],
		"fangyadai-Java": ["fangyadai_java"],
		"channel": ["channel.beebank.com"],
		"fangdai-shendeng": ["fanginter.shendenglicai.com"],
		"fangdai-dxh": ["fangdai.dxhbank.com"],
		"CUISHOU": ["collection.huixinglicai.com"],
		"fangdaish": ["fangdaish.shendenglicai.com", "fangdai.m.shendenglicai.com", "assetmanage"]
	}
	newtime = int(str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0])
	for i in Email:
		emailinfo = EmailInfo(emailname=i, emailtime=data['date'], identifier=i + str(data['date']), bj1=data[i][0],
							  bj2=data[i][1], bj3=data[i][2], bj4=data[i][3], bj5=data[i][4], ctime=newtime)
		db.session.add(emailinfo)
		db.session.commit()
	return jsonify({'msg': 'success'})


# -----------------------代码发布数据——写入数据方法---------------------
@testhome.route('/insert2', methods=['POST'])
def insert_code():
	data = request.json.get('data')
	info = [
		'jiaoyudai', 'cuishou', 'jisuanhesuan',
		'chedai', 'huixingyewu', 'fengkong',
		'huixingcaiwu', 'yunwei', 'zhifu', 'fangdai', 'wuxingayi'
	]
	newtime = int(str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0])
	for i in info:
		emailinfo = CodeInfo(emailname=i, identifier=i + str(data['date']), emailtime=data['date'], bjsl=data[i],
							 ctime=newtime)
		db.session.add(emailinfo)
		db.session.commit()
	return jsonify({'msg': 'success'})


# -----------------------Jenkins管理项目——写入数据方法------------------
@testhome.route('/insert3', methods=['POST'])
def insert_jenlins():
	data = request.json.get('data')
	value = ProjectInfo.query.filter_by(projectname=data['projectname']).first()
	if value is None:
		projectinfo = ProjectInfo(projactname=data['projectname'])
		db.session.add(projectinfo)
		db.session.commit()
	return jsonify({'msg': 'success'})


@testhome.app_errorhandler(404)
def page_not_found(e):
	print e
	return render_template('404.html', u=session['username']), 404


@testhome.app_errorhandler(500)
def server_interval(e):
	print e
	return render_template('500.html', u=session['username']), 500
