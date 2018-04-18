from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from rest_framework.decorators import api_view
import os, sys
import urllib
import requests, json
from crontab import CronTab
import datetime
from shutil import rmtree

INSTAPY_ROOT = '/home/tianwang/Data/InstaPy'
LOG_ROOT = os.path.join(INSTAPY_ROOT, 'logs')
CRON_USER = 'tianwang'
PYTHON = '/home/tianwang/Data/anaconda3/bin/python'

@api_view(['GET'])
def startInsBot(request):
	try:
		username = request.GET.get('username')
		password = request.GET.get('password')

		if username is None or password is None:
			return HttpResponseBadRequest('please double check the request content. (need both username and password)')

		tag = request.GET.get('tag')
		if tag is None or tag == '':
			tag = 'portrait_photography_newyork'

		follow = request.GET.get('follow')
		if follow is None:
			follow = False

		# create log folder for username
		log_folder = os.path.join(LOG_ROOT, username)
		if not os.path.exists(log_folder):
			os.makedirs(log_folder)
		else:
			# if folder exists mean robot is running.
			return HttpResponse('instRobot is already running for user: {}'.format(username))


		my_cron = CronTab(user=CRON_USER)
		timenow = str(datetime.datetime.now())
		timenow = timenow.replace(' ', '')
		timenow = timenow[:timenow.find('.')]



		log_path = os.path.join(LOG_ROOT, username, timenow) + '.txt'

		print('{} {}/quickstart.py {} {} {} >> {} 2>&1'.format(PYTHON, INSTAPY_ROOT, username, password, tag, log_path))

		job = my_cron.new(command='{} {}/quickstart.py {} {} {} {} >> {} 2>&1'.format(PYTHON, INSTAPY_ROOT, username, password, tag, follow, log_path), comment=username)
		job.minute.on(55)
		my_cron.write()
		return HttpResponse('insBot started for user {}.'.format(username))
	except Exception as e:
		print(e)
		return HttpResponseServerError(e)

@api_view(['GET'])
def stopInsBot(request):

	try:
		username = request.GET.get('username')

		if username is None:
			return HttpResponseBadRequest('please double check the request content. (need username to delete the robot)')

		log_folder = os.path.join(LOG_ROOT, username)
		if os.path.exists(log_folder):
			rmtree(log_folder)
		else:
			return HttpResponse('there is not running robot for user: {}'.format(username))

		my_cron = CronTab(user=CRON_USER)
		my_cron.remove_all(comment=username)
		my_cron.write()
		return HttpResponse('insBot stopped for user {}.'.format(username))
	except Exception as e:
		print(e)
		return HttpResponseServerError(e)










