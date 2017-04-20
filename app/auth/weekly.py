from flask import session
from . import testhome
from ..models import WeeklyInfo
from .. import db
from flask import request, render_template, redirect
import time


@testhome.route('/weekly', methods=['GET', 'POST'])
def weekly():
	return render_template('weeklys/weekly.html', u=session['username'], title=u'周报系统')


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
			weekly = WeeklyInfo(weeklyName=weeklyName, weeklyCont=weeklyCont, time=times,
									username=session['username'])
			db.session.add(weekly)
			db.session.commit()
			return redirect('testhome/showWeekly')
		else:
			return render_template('weeklys/addWeekly.html', title=u'测试中心')
	return render_template('weeklys/addWeek.html', title=u'测试中心')