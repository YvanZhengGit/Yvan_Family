# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import datetime


class searchForm(Form):
	start_year = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[0])
	end_year = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[0])
	start_month = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[1])
	end_month = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[1])
	start_day = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default='1')
	end_day = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default='2')
	submit = SubmitField(u'查询')


class codeReleaseForm(Form):
	startyear = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[0])
	startmonth = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[1])
	month = int(str(datetime.datetime.now()).split('-')[1])
	if month is 12:
		endyear = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(int(str(datetime.datetime.now()).split('-')[0]) + 1))
		endmonth = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default='1')
	else:
		endyear = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default=str(datetime.datetime.now()).split('-')[0])
		endmonth = StringField(u'查询条件', validators=[DataRequired(), Length(1, 64)], default="0" + str(int(str(datetime.datetime.now()).split('-')[1]) + 1))
	submit = SubmitField(u'查询')


class Permission():
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80
