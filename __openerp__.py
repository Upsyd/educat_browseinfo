# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
{
    "name" : "Educat Browseinfo",
    "version" : "1.0",
    "depends" : ['base','account','hr','website','smsclient'],
    "author" : "Browseinfo",
    "description": """
    This module is help to print Transe-Cript report of student.
    """,

    "website" : "www.browseinfo.in",

    "data" : [
              'security/security.xml',
              'op_degree/op_degree_view.xml',
              'op_batch/op_batch_view.xml',
              'op_category/op_category_view.xml',
              'op_course/op_course_view.xml',
              'op_division/op_division_view.xml',
              'op_religion/op_religion_view.xml',
              'op_standard/op_standard_view.xml',
#               'op_student/op_select_sem_view.xml',
              'op_roll_number/op_roll_number_view.xml',

              'op_student/op_center_view.xml',
              'op_student/student_sequence.xml',
              'op_student/op_parent_view.xml',
              'op_student/op_student_view.xml',
              'op_subject/op_subject_view.xml',
              'op_faculty/op_faculty_view.xml',
              'op_exam/op_exam_type_view.xml',
              'op_exam/op_exam_view.xml',
              'op_exam/op_exam_workflow.xml',
              'op_exam_attendees/op_exam_attendees_view.xml',
              'op_marksheet_line/op_marksheet_line_view.xml',
              'op_marksheet_register/op_marksheet_register_view.xml',
              
              'op_admission/op_admission_view.xml',
              'op_admission/op_admission_sequence.xml',
              'op_admission/op_admission_workflow_view.xml',
              
              
              'report/student_report_menu.xml',
              'views/student_transcript_report_view.xml',
              'views/addmission.xml',
              'menu/menu_view.xml',
              'menu/student_menu_view.xml',
              
              'security/ir.model.access.csv',
              
              ],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
