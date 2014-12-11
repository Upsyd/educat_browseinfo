# -*- coding: utf-8 -*-
import werkzeug
from openerp.addons.web import controllers
import openerp.http as http
from openerp.http import request

class educat_browseinfo(http.Controller):

    def form_value(self):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        category_obj = pool['op.category']
        course_obj = pool['op.course']
        batch_obj = pool['op.batch']
        standard_obj = pool['op.standard']

        category_ids = category_obj.search(cr, uid, [], context=context)
        course_ids = course_obj.search(cr, uid, [], context=context)
        batch_ids = batch_obj.search(cr, uid, [], context=context)
        standard_ids = standard_obj.search(cr, uid, [], context=context)

        categories = category_obj.browse(cr, uid, category_ids, context=context)
        course = course_obj.browse(cr, uid, course_ids, context=context)
        batch = batch_obj.browse(cr, uid, batch_ids, context=context)
        standard = standard_obj.browse(cr, uid, standard_ids, context=context)

        value = {
                'categories':categories,
                'course':course,
                'batch':batch,
                'standard':standard,
                 }
        return value


    @http.route('/addmission/', type='http', auth="public", website=True)
    def addmission(self,**post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        values = self.form_value()
        return request.website.render("educat_browseinfo.addmission",values)

    @http.route('/addmission/success_login/', type='http', auth="public", website=True)
    def success_login(self,**form_data):
        #Start code for send E-mail to user at time of submit admission form.
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        orm_partner = registry.get('op.admission')
        vals = {
                    'name': form_data.get('name'),
                    'middle_name': form_data.get('middle_name'),
                    'last_name': form_data.get('last_name'),
                    'birth_date':form_data.get('birth_date'),
                    'gender': form_data.get('gender'),
                    'category_id': form_data.get('category_id'),
                    'course_id': form_data.get('course_id'),
                    'batch_id': form_data.get('batch_id'),
                    'standard_id': form_data.get('standard_id'),

                    'street': form_data.get('street'),
                    'phone': form_data.get('code_1'),
                    'city': form_data.get('city'),
                    'country_id':form_data.get('country_id'),
                    'state_id': form_data.get('state_id'),
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
               'mobile': form_data.get('number_1'),
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











