# -*- coding: utf-8 -*-
##############################################################################
#
#    stock_routing module for OpenERP, This module allows to assing rounds to orders to set default locations automatically on moves
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#              Sebastien LANGE <sebastien.lange@syleam.fr>
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
        if context is None:
            context = {}
        # If there is no round_id defined, we take this on the other objects
        if not values.get('round_id', False):
            # Take the value on the sale order, if there is one
            if values.get('sale_id', False):
                sale_order_obj = self.pool.get('sale.order')
                sale_order_data = sale_order_obj.read(cr, uid, values['sale_id'], ['round_id'], context=context)
                values['round_id'] = sale_order_data and sale_order_data['round_id']and sale_order_data['round_id'][0] or False

        return super(stock_picking, self).create(cr, uid, values, context=context)

    def onchange_address_id(self, cr, uid, ids, address_id, round_id, context=None):
        """
        Returns the round_id to put on this sale order
        """
        if context is None:
            context = {}
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


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def _replace_location(self, cr, uid, picking_id, context=None):
        """
        Replaces the location_dest_id in the values dict
        Replaces the location_id of the move_dest_id in the values dict
        """
        if context is None:
            context = {}
        location_id = False
        if picking_id:
            picking_data = self.pool.get('stock.picking').read(cr, uid, picking_id, ['round_id'], context=context)
            if picking_data and picking_data.get('round_id'):
                round_data = self.pool.get('stock.round').read(cr, uid, picking_data['round_id'][0], ['location_id'], context=context)
                if round_data and round_data.get('location_id', False):
                    location_id = round_data['location_id'][0]
        return location_id

    def create(self, cr, uid, values, context=None):
        """
        Replaces location_dest_id by the one from round of the picking
        """
        if context is None:
            context = {}
        location_id = self._replace_location(cr, uid, values.get('picking_id', False), context=context)
        if location_id:
            # Modify the location_dest_id
            values['location_dest_id'] = location_id

            # Modify the location_id of the move_dest_id if filled
            if values.get('move_dest_id', False):
                self.write(cr, uid, [values['move_dest_id']], {'location_id': location_id}, context=context)

        return super(stock_move, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        """
        Replaces location_dest_id by the one from round of the picking
        """
        if context is None:
            context = {}
        if values.get('picking_id', False):
            # Retrieve the location_id from the picking
            location_id = self._replace_location(cr, uid, values.get('picking_id'), context=context)

            if location_id:
                # Modify the location_dest_id to write
                values['location_dest_id'] = location_id

                # Search for the move_dest_ids to modify
                move_dest_ids = []
                if values.get('move_dest_id', False):
                    move_dest_ids = [values.get('move_dest_id')]
                else:
                    stock_move_data = self.read(cr, uid, ids, ['move_dest_id'], context=context)
                    move_dest_ids = [data['move_dest_id'][0] for data in stock_move_data if data['move_dest_id']]

                self.write(cr, uid, move_dest_ids, {'location_id': location_id}, context=context)

        return super(stock_move, self).write(cr, uid, ids, values, context=context)

stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
