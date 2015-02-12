# -*- coding: utf-8 -*-
import werkzeug
from openerp.addons.web import controllers
import openerp.http as http
from openerp.http import request
import cStringIO
import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET

import logging
import re

import werkzeug.utils
import urllib2
import werkzeug.wrappers
from PIL import Image

import openerp
from openerp.addons.web import http
from openerp.tools import ustr, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.http import request, STATIC_CACHE
from openerp.tools import image_save_for_web
class educat_browseinfo(http.Controller):

    @http.route(['/addmission/<country_id>'], type='json', auth="public", website=True)
    def get_state(self , country_id=None, **post):
        cr, uid, context, registry = request.cr, openerp.SUPERUSER_ID, request.context, request.registry

        if country_id:
            domain = [('country_id', '=', int(country_id))]

            state_obj = registry ['res.country.state']
            state_ids = state_obj.search(cr, uid, domain, context=context)
            state = state_obj.read(cr, uid, state_ids, ['id','name'], context=context)

        return state



    @http.route('/addmission/', type='http', auth="public", website=True)
    def addmission(self,**post):
        cr, uid, context, registry = request.cr, openerp.SUPERUSER_ID, request.context, request.registry

        category_obj = registry['op.category']
#         course_obj = registry['op.course']
        batch_obj = registry['op.batch']
#         standard_obj = registry['op.standard']
        country_obj = registry['res.country']

        category_ids = category_obj.search(cr, uid, [], context=context)
#         course_ids = course_obj.search(cr, uid, [], context=context)
        batch_ids = batch_obj.search(cr, uid, [], context=context)
#         standard_ids = standard_obj.search(cr, uid, [], context=context)
        country_ids = country_obj.search(cr, uid, [], context=context)

        categories = category_obj.browse(cr, uid, category_ids, context=context)
#         course = course_obj.browse(cr, uid, course_ids, context=context)
        batch = batch_obj.browse(cr, uid, batch_ids, context=context)
#         standard = standard_obj.browse(cr, uid, standard_ids, context=context)
        countries = country_obj.browse(cr, uid, country_ids, context=context)

        state_obj = registry ['res.country.state']
        state_ids = state_obj.search(cr, uid, [], context=context)
        state = state_obj.browse(cr, uid, state_ids, context=context)

        value = {
                'categories':categories,
#                 'course':course,
                'batch':batch,
#                 'standard':standard,
                'countries':countries,
                'state':state,
                 }

        return request.website.render("educat_browseinfo.addmission",value)

    @http.route('/addmission/success_login/', type='http', auth="public", website=True)
    def success_login(self,**form_data):
        #Start code for send E-mail to user at time of submit admission form.
        cr, uid, context, registry = request.cr, openerp.SUPERUSER_ID, request.context, request.registry
        orm_partner = registry.get('op.admission')
        birthdate = form_data.get('birth_date') or False
        if birthdate:
        	birthdate = datetime.datetime.strptime(birthdate, DEFAULT_SERVER_DATE_FORMAT)
        join_date = form_data.get('join_date') or False
    	if join_date:
        	join_date = datetime.datetime.strptime(form_data.get('join_date'), DEFAULT_SERVER_DATE_FORMAT)
        quali_date = form_data.get('quali_date') or False
    	if quali_date:
        	quali_date = datetime.datetime.strptime(form_data.get('quali_date'), DEFAULT_SERVER_DATE_FORMAT)

        vals = {
                    'name': form_data.get('name'),
                    'middle_name': form_data.get('middle_name'),
                    'last_name': form_data.get('last_name'),
                    'email': form_data.get('email'),
                    'phone': form_data.get('phone'),
                    'citizen_zambia': form_data.get('citizen'),
                    'country_citizenchip': form_data.get('country_citizenchip'),
                    'nrc_no': form_data.get('NRC'),
                    'passport_number': form_data.get('passport'),
                    'birth_date': birthdate,
                    'gender': form_data.get('gender'),
                    'street': form_data.get('address'),
                    'city': form_data.get('city'),
                    'state_id': form_data.get('state'),
                    'zip': form_data.get('zip'),
                    'country_id': form_data.get('country_id'),
                    'payment_method': form_data.get('bank_type'),
                    'payment_detail': form_data.get('payment_detail'),
                    'currently_working': form_data.get('work'),
                    'employed_teacher': form_data.get('teacher'),
                    'name_of_school': form_data.get('school'),
                    'attach_id': form_data.get('file_name'),
                    'date_first_appoint': join_date,
                    'ts_number': form_data.get('ts_number'),
                    'district': form_data.get('district'),
                    'province': form_data.get('province'),
                    'last_school': form_data.get('last_school'),
                    'what_type_employee': form_data.get('emp_type'),
                    'subject': form_data.get('subject'),
                    'grade': form_data.get('grade'),
                    'institution': form_data.get('institute'),
                    'qualification': form_data.get('qualification'),
                    'date': quali_date,
                    'course_select':form_data.get('programe'),
                    'course_a': form_data.get('course'),
                    'table1_eng': form_data.get('table1_eng'),
                    'table1_hist': form_data.get('table1_hist'),
                    'table1_maths': form_data.get('table1_maths'),
                    'table2_civics': form_data.get('table2_civics'),
                    'table2_re': form_data.get('table2_re'),
                    'table2_zl': form_data.get('table2_zl'),
                    'table2_geo': form_data.get('table2_geo'),
                    'special_education': form_data.get('special'),
                    'vision': form_data.get('vision'),
                    'hearing': form_data.get('hearing'),
                    'mobility': form_data.get('mobility'),
                    'speech': form_data.get('speech'),
                    'other': form_data.get('other'),
                    'lst_other': form_data.get('list'),

 #                   'category_id': form_data.get('category_id'),
 #                   'course_id': form_data.get('course_id'),
 #                   'batch_id': form_data.get('batch_id'),
 #                   'standard_id': form_data.get('standard_id'),

                    }

        new_addmission = orm_partner.create(cr, uid, vals, context=context)
        name = form_data.get('name')
        mail_mail = registry.get('mail.mail')
        mail_to = form_data.get('email')
        mail_ids=[]
        admin_email = registry.get('res.company').browse(cr, uid, [1])[0].email
        sub = 'email'
        body = """Hello,
                 Thank you!
                    Your Admission application has been successfully registered, we will get back to you soon."""
        if mail_to:
            vals = {
                    'state': 'outgoing',
                    'subject': sub,
                    'body_html': body,
                    'email_to': mail_to,
                    'email_from': admin_email,
                    }

        mail_ids.append(mail_mail.create(cr, uid, vals, context=context))
        mail_mail.send(cr, uid, mail_ids, auto_commit=True, context=context)
        #End code for send E-mail to user at time of submit admission form.

        #start code for send SMS to user at time of submit admission form.
        message = "Hello ur admission submit."
        cont={
                'name':form_data.get('name'),
               'mobile': form_data.get('phone'), #form_data.get('number_1'),
               'msg':message,
               }
        print"___________________",cont
        sms_obj = registry.get('sms.smsclient.queue')
        sms_obj.create(cr,uid,cont,context=None)
        #end for send SMS to user at time of submit admission form.
        return request.website.render("educat_browseinfo.success_login")

controllers.main.html_template = """<!DOCTYPE html>
<html style="height: 100%%">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>OpenEduCat</title>
        <link rel="shortcut icon" href="/educat_browseinfo/static/src/img/openeducat_favicon.png" type="image/x-icon"/>
        <link rel="stylesheet" href="/web/static/src/css/full.css" />
        %(css)s
        %(js)s
        <script type="text/javascript">
            $(function() {
                var s = new openerp.init(%(modules)s);
                %(init)s
            });
        </script>
    </head>
    <body>
        <!--[if lte IE 8]>
        <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>
        <script>CFInstall.check({mode: "overlay"});</script>
        <![endif]-->
    </body>
</html>
"""











