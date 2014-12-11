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
from openerp.osv import osv, fields
import time




class op_select_sem(osv.osv):
    
    _name = 'op.select.sem'
    
    _columns = {
                'course_id': fields.many2one('op.course', string='Course', required=True),
                'select_sem_line': fields.one2many('op.select.sem.line','select_sem_id', 'Select Subject'),
                }
    
class op_select_sem_line(osv.osv):
    
    _name = 'op.select.sem.line'
    
    _columns = {
                'select_sem_id': fields.many2one('op.select.sem', 'Select Semester'),
                'seq': fields.char('Sequence'),
                'name': fields.char('Name'),
                'subject_line': fields.one2many('op.subject','select_sem_id','Subjects'),
                 
                 
                }


    
# class op_select_subject_line(osv.osv):
#     
#     _name = 'op.select.subject.line'
#     
#     _columns = {
#                 'select_sem_line_id': fields.many2one('op.select.sem.line', 'Select Line'),
#                 'select_subject_line_id': fields.many2one('op.select.subject.line', 'Select Subject'),
#                 'subject_id': fields.many2one('op.subject', 'Subject'),
#                 
#                 'elective': fields.boolean('Elective'),
#                 
#                 'subject_line': fields.one2many('op.select.subject.line','select_subject_line_id','Subject'),
#                 
#                 }
    
    
    
    
    