# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.website.website_generator import WebsiteGenerator
from hub.hub.utils import autoname_increment_by_field

class HubItem(WebsiteGenerator):
	website = frappe._dict(
		page_title_field = "item_name"
	)

	def autoname(self):
		super(HubItem, self).autoname()
		self.name = autoname_increment_by_field(self.doctype, "item_code", self.name)

	def update_item_details(self, item_dict):
		self.old = None
		if frappe.db.exists('Hub Item', self.name):
			self.old = frappe.get_doc('Hub Item', self.name)
		for field, new_value in item_dict.iteritems():
			old_value = self.old.get(field) if self.old else None
			if(new_value != old_value):
				self.set(field, new_value)
				frappe.db.set_value("Hub Item", self.name, field, new_value)

	def validate(self):
		if not self.route:
			self.route = 'items/' + self.name

	def get_context(self, context):
		context.no_cache = True

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.title = 'Items'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'
