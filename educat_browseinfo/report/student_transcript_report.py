import time
from openerp.osv import osv
from openerp.report import report_sxw


class student_transcript_report(report_sxw.rml_parse):


    def __init__(self, cr, uid, name, context=None):
        super(student_transcript_report, self).__init__(cr, uid, name, context=context)
        self.total_point = 0.0
        self.total_hour = 0.0
        self.localcontext.update({
            'time': time,
             'get_sub_total_hour':self.get_sub_total_hour,
             'get_sub_total_point':self.get_sub_total_point,
             'get_total_hour' : self.get_total_hour,
             'get_total_point' : self.get_total_point,
             'get_gpa' : self.get_gpa,
             'get_cgpa' : self.get_cgpa,
             'get_hour' : self.get_hour,
            })

    def get_sub_total_hour(self, obj):
         
         hours = 0.0
         for obj in obj:
             hours = hours + obj.hours
         self.total_hour = self.total_hour + hours
         return hours
    
    def get_sub_total_point(self, obj):
         marks = 0.0
         for obj in obj:
            marks = marks + obj.marks
         self.total_point = self.total_point + marks
         return marks
    def get_total_hour(self):
        return self.total_hour
    def get_total_point(self):
        return self.total_point

    def get_gpa(self, obj):
        marks = 0.0
        hours = 0.0
        for obj in obj:
            marks = marks + obj.marks
            hours = hours + obj.hours
        return (marks/hours)
        
    def  get_cgpa(self):
        return (self.get_total_point()/self.get_total_hour())

    def get_hour(self, obj):
        hours = 0.0
        for obj in obj:
             hours = hours + obj.hours
        return hours

class golf_report_template_id(osv.AbstractModel):
    _name = 'report.educat_browseinfo.student_transcript_report_template_id'
    _inherit = 'report.abstract_report'
    _template = 'educat_browseinfo.student_transcript_report_template_id'
    _wrapped_report_class = student_transcript_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: