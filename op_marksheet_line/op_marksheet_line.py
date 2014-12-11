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


class op_marksheet(osv.osv):
    _name = 'op.marksheet'
    _rec_name ='student_id'
    _columns = {
                'student_id': fields.many2one('op.student','Student', required=True),
                'batch_id': fields.many2one('op.batch', 'Batch', required=True),
                'course_id': fields.many2one('op.course', 'Course', required=True),
                'standard_id': fields.many2one('op.standard', 'Standard', required=True),
                'division_id': fields.many2one('op.division', string='Division', required=True),
                
                'marksheet_line': fields.one2many('op.marksheet.line', 'marksheet_id', 'Marksheet Line'),
                'exam_id': fields.many2one('op.exam','Exam', required=True),
                
                }
    
    def print_marksheet(self, cr, uid, ids, context=None):
        
        return self.pool['report'].get_action(cr, uid, ids, 'openeducat_erp.marksheet_report', context=context)
    

class op_marksheet_line(osv.osv):
    _name = 'op.marksheet.line'
    
    
    _columns = {
                
                'marksheet_id': fields.many2one('op.marksheet','MarkSheet'),
                'subject_id': fields.many2one('op.subject', 'Subject', required=True),
                'present_absent': fields.boolean('Present/Absent'),
                'marks': fields.float('Obtain Marks'),
                
                'hours': fields.float('Exam Hours'),
                'grade': fields.char('Grade'),
                
                
                }
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
