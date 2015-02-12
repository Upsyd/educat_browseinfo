# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.tech-receptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time
import datetime
import xlrd 
import tempfile

import openerp
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

class op_exam_session(osv.osv):
    _name = 'op.exam.session'

    _columns = {
			
            'name': fields.char(size=256, string='Exam', required=True),
            'code': fields.char(size=256, string='Code', required=True),
            'state': fields.selection([('draft','Draft'),('in_progress','In Progress'),('done','Done')], string='State'),
            'note': fields.text(string='Note'),
            'responsible_id': fields.many2many('op.faculty', 'exam_faculty_rel', 'op_exam_id', 'op_faculty_id', string='Responsible'),
            'exam_list': fields.one2many('op.exam', 'session_id', 'Exams'),
            'start_date': fields.datetime(string='Start Time', required=True),
            'end_date': fields.datetime(string='End Time', required=True),
            
            }

    _defaults = {
                 'state': 'draft'
                 }
    
    def _check_date_time(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids): 
            if self_obj.start_date > self_obj.end_date:
                return False
        return True
    
    _constraints = [
        (_check_date_time, 'Start Time Should be greater than End Time .', ['start_time','end_time']),
    ]
    def act_in_progress(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'in_progress'})
        return True
    
    def act_done(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'done'})
        return True
    
    def act_draft(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
    

class op_exam(osv.osv):
    
    _name = 'op.exam'
    
    def _get_total_marks(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = 0.00
            total_mark = 0.00
            if self_obj.exam_line:
                for line in self_obj.exam_line:
                    total_mark += line.total_marks
                res[self_obj.id] = total_mark
        
        return res
    
    def _get_total_passing_mark(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = 0.00
            total_pass = 0.00
            if self_obj.exam_line:
                for line in self_obj.exam_line:
                    total_pass += line.min_marks
                res[self_obj.id] = total_pass
        return res
    
        
    _columns = {
                'session_id':fields.many2one('op.exam.session','Exam Session'),
                'name': fields.char('Exam', required=True),
                'code': fields.char(size=8, string='Exam Code', required=True),
                'batch_id': fields.many2one('op.batch', 'Batch', required=True),
#                 'course_id': fields.many2one('op.course', 'Course', required=True),
#                 'standard_id': fields.many2one('op.standard', 'Standard', required=True),
                'division_id': fields.many2one('op.division', string='Division'),
                'exam_type': fields.many2one('op.exam.type', string='Exam Type', required=True),
                'start_time': fields.datetime(string='Start Time', required=True,),
                'end_time': fields.datetime(string='End Time', required=True),
                'total_marks':fields.function(_get_total_marks,string='Total Marks',type='float'),
                'min_marks':fields.function(_get_total_passing_mark,string='Passing Marks',type='float'),
                'state': fields.selection([('n','New Exam'),('h','Held'),('s','Scheduled'),('d','Done'),('c','Cancelled')], string='State', select=True, readonly=True),
                'exam_line': fields.one2many('op.exam.line', 'exam_id', 'Exams'),
                
                'result_generated': fields.boolean('Result Generated'),
                
                
                }
    
    _defaults = {
                 'state':'n',
                 }
    
    def _check_date_time(self, cr, uid, ids, context=None):
        for self_obj in self.browse(cr, uid, ids): 
            if self_obj.start_time > self_obj.end_time:
                return False
        return True
    
    _constraints = [
        (_check_date_time, 'Start Time Should be greater than End Time .', ['start_time','end_time']),
    ]
    
    def act_held(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'h'})
        return True
    
    def act_done(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'d'})
        return True
    
    def act_schedule(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'s'})
        return True

    def act_cancel(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'c'})
        return True

    def act_new_exam(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids,{'state':'n'})
        return True
    
    def generate_result(self, cr, uid, ids, context=None):
        
        marksheet_pool = self.pool.get('op.marksheet')
        marksheet_line_pool = self.pool.get('op.marksheet.line')
        student_list = []
        for self_obj in self.browse(cr, uid, ids):
            for exam_line in self_obj.exam_line:
                for student_mark_line in exam_line.student_exam_marks_line:
                    student_list.append(student_mark_line.student_id.id)
            marksheet_lst = []
            for student in list(set(student_list)):
                dic_marksheet = {}
                dic_marksheet = {
                                 'student_id': student,
                                 'batch_id': self_obj.batch_id.id,
#                                  'course_id': self_obj.course_id.id,
#                                  'standard_id': self_obj.standard_id.id,
                                 'division_id': self_obj.division_id.id,
                                 'exam_id': self_obj.id
                                 }
                marksheet = marksheet_pool.create(cr, uid, dic_marksheet)
                marksheet_lst.append(marksheet)
            
            
            for mark_sheet in marksheet_lst:
                mark_sheet_browse = marksheet_pool.browse(cr, uid, mark_sheet)
                for exam_line in self_obj.exam_line:
                    for student_mark_line in exam_line.student_exam_marks_line:
                        if mark_sheet_browse.student_id.id == student_mark_line.student_id.id:
                            dic_marksheet_line = {
                                                  'marksheet_id': mark_sheet,
                                                  'subject_id': exam_line.subject_id.id,
                                                  'present_absent': student_mark_line.check,
                                                  'marks': student_mark_line.obtain_marks,
                                                  'hours': student_mark_line.hours,
                                                  'grade': student_mark_line.grade,
                                                  }
                            marksheet_line = marksheet_line_pool.create(cr, uid, dic_marksheet_line)
            
            self.write(cr, uid, ids, {'result_generated': True})
            
        return True


class op_exam_line(osv.osv):
    
    _name = 'op.exam.line'
    
    def _get_hour(self,cr,uid,ids,field,arg,context=None):
        res = {}
        for record in self.browse(cr,uid,ids):
            
            
            end_time = datetime.datetime.strptime(record.end_time, "%Y-%m-%d %H:%M:%S")
            start_time = datetime.datetime.strptime(record.start_time, "%Y-%m-%d %H:%M:%S")
            res[record.id] = (end_time - start_time).total_seconds()/60/60
        return res
    
    _columns = {
                'exam_id':fields.many2one('op.exam','Exam'),
                'subject_id': fields.many2one('op.subject', string='Subject', required=True),
                'venue': fields.many2one('res.partner', string='Venue'),
                'start_time': fields.datetime(string='Start Time', required=True),
                'end_time': fields.datetime(string='End Time', required=True),
                'total_marks':fields.float('Total Marks'),
                'min_marks':fields.float('Passing Marks'),
                'venue': fields.many2one('res.partner', string='Venue'),
                'student_exam_marks_line': fields.one2many('op.student.exam.marks', 'exam_line_id', 'Exam Line'),
                'hour':fields.function(_get_hour,type='float',string='Exam Hours'),
                'subject_mark_sheet':fields.binary('Add Subject Mark sheet', filters='*.xls,*.xlsx'),
                }
    def _check_date_time(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids): 
            if line.exam_id.id:
                if line.start_time > line.exam_id.start_time and line.end_time < line.exam_id.end_time:
                    return True
                return False
    
    _constraints = [
        (_check_date_time, 'Start and End Time select a between Session Start and End time.', ['start_time','end_time']),
    ]
    
    
    def load_marks(self,  cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids)
        student_marks_pool = self.pool.get('op.student.exam.marks')
        
        if obj.subject_mark_sheet:
            
            #for delete old entry when user click multiple time this button
            line_search = self.pool.get('op.student.exam.marks').search(cr, uid, [('exam_line_id','=',obj.id)])
            if line_search:
                self.pool.get('op.student.exam.marks').unlink(cr, uid, line_search)
            
            file_path = tempfile.gettempdir() +'/file.xls'
            data = obj.subject_mark_sheet
            f = open(file_path,'workbook')
            f.write(data.decode('base64'))
            f.close()
            workbook = xlrd.open_workbook(file_path)
            worksheet = workbook.sheet_by_name('Sheet1')
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = 0
            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)
                print 'Row:', curr_row
                curr_cell = -1
                student_list = []
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_type = worksheet.cell_type(curr_row, curr_cell)
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    print '    ',cell_type,':', cell_value
                
                    student_list.append(cell_value)
                #search student by student ID number
                student_search = self.pool.get('op.student').search(cr, uid, [('roll_number','=',student_list[0])])
                
                if student_search:
                    student_name = student_search[0]
                    dic = {}
                    dic = {
                           'exam_line_id': obj.id,
                           'hours':obj.hour,
                           'student_id': student_name,
                           'student_id_no': student_list[0],
                           'check':student_list[1],
                           'obtain_marks':student_list and student_list[2] or '',
                           'grade':student_list[3],
                           
                           }
                    student_marks_pool.create(cr, uid, dic)
                else:
                    raise osv.except_osv(('Student Not Found'), ('Can not find student having ID %s.') %(student_list[0]))
        else:
            raise osv.except_osv(('Fill Data'), ('Enter Subject Mark Sheet.'))
        return True

    def load_student(self, cr, uid, ids, context=None):
        student_marks_pool = self.pool.get('op.student.exam.marks')
        for self_obj in self.browse(cr, uid, ids):
            student_search = self.pool.get('op.student').search(cr, uid, [('batch_id','=',self_obj.exam_id.batch_id.id),
                                                                          ('division_id','=',self_obj.exam_id.division_id.id),
                                                                          ])
            for student in student_search:
                dic = {}
                dic = {
                       'student_id': student,
                       'exam_line_id': self_obj.id,
                       'hours':self_obj.hour
                       }
                line = student_marks_pool.create(cr, uid, dic)
        return True
    
    
    
class op_student_exam_marks(osv.osv):
    
    _name = 'op.student.exam.marks'
    
    _columns = {
                'exam_line_id': fields.many2one('op.exam.line', 'Student Marks'),
                
                'student_id': fields.many2one('op.student', 'Student Name'),
                'student_id_no': fields.char('Student ID'),
                'present_absent': fields.boolean('Present/Absent'),
                'obtain_marks': fields.float('Obtain Marks'),
                
                'check': fields.boolean('Present/Absent'),
                'hours': fields.float('Exam Hours'),
                'grade': fields.char('Grade'),                
                }
    _defaults = {
                 'check': True,
                 }
    
    
    
    
    def button_present(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'check': True})
        return True
    
    def button_absent(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'check': False})
        return True
        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
