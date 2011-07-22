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


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def _replace_location(self, cr, uid, picking_id, context=None):
        """
        Replaces the location_dest_id in the values dict
        Replaces the location_id of the move_dest_id in the values dict
        """
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
        location_id = self._replace_location(cr, uid, values.get('picking_id', False), context=context)
        if location_id:
            # Modify the location_dest_id
            values['location_dest_id'] = location_id

            # Modify the location_id of the move_dest_id if filled
            if values.get('move_dest_id', False):
                self.write(cr, uid, [values['move_dest_id']], {'location_id': location_id}, context=context)

        id = super(stock_move, self).create(cr, uid, values, context=context)
        return id

    def write(self, cr, uid, ids, values, context=None):
        """
        Replaces location_dest_id by the one from round of the picking
        """
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

        res = super(stock_move, self).write(cr, uid, ids, values, context=context)
        return res

stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
