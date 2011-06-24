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
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    stock_routing is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Stock Routing',
    'version': '1.0',
    'category': 'Generic Modules/Inventory Control',
    'description': """This module allows to assing rounds to orders to set default locations automatically on moves""",
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'base',
        'sale',
        'stock',
    ],
    'init_xml': [],
    'images': [],
    'update_xml': [
        'security/ir.model.access.csv',
        #'wizard/wizard.xml',
        'stock_round_view.xml',
        'res_partner_view.xml',
        'sale_order_view.xml',
        'stock_picking_view.xml',
    ],
    'demo_xml': [],
    'test': [
        'test/stock_routing_test1.yml',
        'test/stock_routing_test2.yml',
        'test/stock_routing_test3.yml',
        'test/stock_routing_test4.yml',
        'test/stock_routing_test5.yml',
        'test/stock_routing_test6.yml',
        'test/stock_routing_test7.yml',
        'test/stock_routing_test8.yml',
        'test/stock_routing_test9.yml',
        'test/stock_routing_test10.yml',
        'test/stock_routing_test11.yml',
        'test/stock_routing_test12.yml',
        'test/stock_routing_test13.yml',
        'test/stock_routing_test14.yml',
        'test/stock_routing_test15.yml',
        'test/stock_routing_test16.yml',
        'test/stock_routing_test17.yml',
        'test/stock_routing_test18.yml',
        'test/stock_routing_test19.yml',
#        'test/stock_routing_test20.yml',# TODO
#        'test/stock_routing_test21.yml',# TODO
#        'test/stock_routing_test22.yml',# TODO
#        'test/stock_routing_test23.yml',# TODO
        'test/stock_routing_test24.yml',
        'test/stock_routing_test25.yml',
        'test/stock_routing_test26.yml',
        'test/stock_routing_test27.yml',
        'test/stock_routing_test28.yml',
        'test/stock_routing_test29.yml',
#        'test/stock_routing_test30.yml',# TODO
    ],
    #'external_dependancies': {'python': ['kombu'], 'bin': ['which']},
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
