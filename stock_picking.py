# -*- coding: utf-8 -*-
##############################################################################
#
#    stock_routing module for OpenERP, This module allows to assing rounds to orders to set default locations automatically on moves
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#
#    This file is a part of stock_routing
#
#    stock_routing is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    stock_routing is distributed in the hope that it will be useful,
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

    def create(self, cr, uid, values, context=None):
        """
        Redefine create method to use the round_id field
        """
        # If there is no round_id defined, we take this on the other objects
        if not values.get('round_id', False):
            # Take the value on the sale order, if there is one
            if values.get('sale_id', False):
                sale_order_obj = self.pool.get('sale.order')
                sale_order_data = sale_order_obj.read(cr, uid, values['sale_id'], ['round_id'], context=context)
                values['round_id'] = sale_order_data and sale_order_data['round_id']and sale_order_data['round_id'][0] or False
            # Take the value on the partner address, if there is one and if round_id is not defined
            if not values.get('round_id', False) and values.get('address_id', False):
                res_partner_address_obj = self.pool.get('res.partner.address')
                partner_address_data = res_partner_address_obj.read(cr, uid, values['address_id'], ['round_id', 'partner_id'], context=context)
                values['round_id'] = partner_address_data and partner_address_data['round_id'] and partner_address_data['round_id'][0] or False
                # Take the value on the partner, if there is one and if round_id is not defined
                if not values.get('round_id', False) and partner_address_data.get('partner_id', False):
                    res_partner_obj = self.pool.get('res.partner')
                    partner_data = res_partner_obj.read(cr, uid, partner_address_data['partner_id'][0], ['round_id'], context=context)
                    values['round_id'] = partner_data and partner_data['round_id'] and partner_data['round_id'][0] or False

        id = super(stock_picking, self).create(cr, uid, values, context=context)
        return id

    def action_confirm(self, cr, uid, ids, context=None):
        """
        Replaces moves dest location according to the round
        """
        res = super(stock_picking, self).action_confirm(cr, uid, ids, context=context)

        stock_move_obj = self.pool.get('stock.move')

        for picking in self.browse(cr, uid, ids, context=context):
            location_id = False

            # Take the location on the first round we find
            if picking.round_id:
                location_id = picking.round_id.location_id and picking.round_id.location_id.id or False
            elif picking.address_id and picking.address_id.round_id:
                location_id = picking.address_id.round_id.location_id and picking.address_id.round_id.location_id.id or False
            elif picking.address_id and picking.address_id.partner_id and picking.address_id.partner_id.round_id:
                location_id = picking.address_id.partner_id.round_id.location_id and picking.address_id.partner_id.round_id.location_id.id or False

            # If a location was found, replace the location_dest_id of the moves by this one
            if location_id:
                move_ids = [move.id for move in picking.move_lines]
                stock_move_obj.write(cr, uid, move_ids, {'location_dest_id': location_id}, context=context)

        return res

stock_picking()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
