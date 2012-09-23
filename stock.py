# -*- coding: utf-8 -*-
##############################################################################
#
#    wms_routing module for OpenERP, This module allows to assing rounds to orders to set default locations automatically on moves
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#
#    This file is a part of wms_routing
#
#    wms_routing is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    wms_routing is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields


class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    _columns = {
        'round_id': fields.many2one('stock.round', 'Round', help='Round for this picking'),
    }

    def action_confirm(self, cr, uid, ids, context=None):
        """
        Replaces moves dest location according to the round
        """
        stock_move_obj = self.pool.get('stock.move')
        for picking in self.browse(cr, uid, ids, context=context):
            location_id = False
            # Take the location on the first round we find
            if picking.round_id:
                location_id = picking.round_id.location_id and picking.round_id.location_id.id or False
                # If a location was found, replace the location_dest_id of the moves by this one
                if location_id:
                    move_ids = [move.id for move in picking.move_lines]
                    stock_move_obj.write(cr, uid, move_ids, {'location_dest_id': location_id}, context=context)
        return super(stock_picking, self).action_confirm(cr, uid, ids, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default['round_id'] = False
        return super(stock_picking, self).copy(cr, uid, id, default, context=context)

    def onchange_address_id(self, cr, uid, ids, address_id, round_id, context=None):
        """
        Returns the round_id to put on this sale order
        """
        res = {}
        # If there is a round_id defined, we don't change the value
        if not round_id and address_id:
            res_partner_address_obj = self.pool.get('res.partner.address')
            partner_address_data = res_partner_address_obj.read(cr, uid, address_id, ['partner_id', 'round_id'], context=context)
            if partner_address_data and partner_address_data['round_id']:
                res = {'value': {'round_id': partner_address_data['round_id'][0]}}
            if not res and partner_address_data['partner_id']:
                res_partner_obj = self.pool.get('res.partner')
                partner_data = res_partner_obj.read(cr, uid, partner_address_data['partner_id'][0], ['round_id'], context=context)
                if partner_data and partner_data['round_id']:
                    res = {'value': {'round_id': partner_data['round_id'][0]}}

        # No value found, we return nothing
        return res

stock_picking()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
