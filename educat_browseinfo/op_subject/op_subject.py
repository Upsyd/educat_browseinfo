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

class op_subject(osv.osv):
    _name = 'op.subject'
    
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context={}
        res = []
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        for record in reads:
            name =  record['name']+"["+record['code']+"] "
            res.append((record['id'], name))
        return res
    
    _columns = {
            'name': fields.char(size=128, string='Name', required=True),
            'code': fields.char(size=256, string='Code', required=True),
            'grade_waitage': fields.float(string='Grade Waitage'),
            'type': fields.selection([('p','Practial'),('t','Theory'),('pt','Both'),('o','Other')], string='Type'),
            'elective': fields.boolean('Elective'),
            
#             'standard_id': fields.many2one('op.standard','Standard'),
            
            
            
    }

op_subject()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
