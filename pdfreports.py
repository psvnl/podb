'''
POdB: A purchase order management system for small businesses 
Copyright (C) 2016  Paulo S. V. N. Leal

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

Contact: paulosvnleal@gmail.com
'''

import os
import datetime
from PyQt4.QtGui import QMessageBox
from reportlab.platypus import Image, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape
from datavalidation import (validate_num_address_lines, 
                            DATA_VAL_ERROR_MSG_BOX_TITLE)
from messagebox import execute_warning_msg_box

_LEFT_RIGHT_MARGIN_WIDTH = cm*2
_TOP_BOTTOM_MARGIN_WIDTH = cm

class PoPdfPageXofYCanvas(Canvas):
    '''
    Subclass of the Canvas class that saves page states and allows the 
    "Page X of Y" string to be printed in the footer of the page once the  
    document has been built.
    Straight copy from a recipe on ActiveState website:
    http://code.activestate.com/recipes/576832/
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """
        Add "Page X of Y" string to the footer of each page.
        """
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)
        
    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(A4[0] - _LEFT_RIGHT_MARGIN_WIDTH, 
                             _TOP_BOTTOM_MARGIN_WIDTH,
            "Page %d of %d" % (self._pageNumber, page_count))


class PoPdfCompanyDetails(object):
    '''
    A class containing all of the information required to populate the company
    details in the "letterhead" section of the PDF.
    The name property is also used in the footer.
    '''
    
    def __init__(self, name, address, phone, fax="", email="", web="",
                 logo_filename=None):
        # The first three parameters are required. The configuration management
        # should have already confirmed that they are fine.
        if name is None:
            raise ValueError("The name parameter is invalid.")
        if address is None:
            raise ValueError("The address parameter is invalid.")
        if phone is None:
            raise ValueError("The phone parameter is invalid.")
        if logo_filename is None or logo_filename == "":
            # No logo filename. No problem.
            self.logo_filename = None
        else:
            if os.path.exists(logo_filename) != True:
                self.logo_filename = None
                execute_warning_msg_box(DATA_VAL_ERROR_MSG_BOX_TITLE,
                                        ("The configured company logo file "
                                         "could not be found. The PDF will "
                                         "be generated without it."),
                                        QMessageBox.Ok)
            else:
                self.logo_filename = logo_filename
        self.name = name
        self.address_lines = validate_num_address_lines(address)
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.web = web

    
class PoPdfOrderDetails(object):
    '''
    A class containing all of the information about the order. This appears in 
    the "letterhead" section of the PDF.
    '''
    
    def __init__(self, order_number, order_date, order_payment_terms):
        self.order_number = order_number
        self.order_date = order_date
        self.order_payment_terms = order_payment_terms


class PoPdfSupplierDetails(object):
    '''
    A class containing all of the information about the supplier.
    '''

    def __init__(self, name, address, phone, fax="", email="", contact=""):
        if name is None:
            raise ValueError("The name parameter is invalid.")
        if address is None:
            raise ValueError("The address parameter is invalid.")
        if phone is None:
            raise ValueError("The phone parameter is invalid.")
        self.name = name
        # Supplier address lines currently not used.
        self.address_lines = validate_num_address_lines(address)
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.contact = contact

        
class PoPdfDeliveryDetails(object):
    '''
    A class containing all of the information about the delivery.
    '''
    
    def __init__(self, delivery_date, delivery_address, delivery_gps_coords=""):
        if delivery_date is None:
            raise ValueError("The delivery_date parameter is invalid.")
        if delivery_address is None:
            raise ValueError("The delivery_address parameter is invalid.")
        self.delivery_date = delivery_date
        # Delivery address lines currently not used.
        self.address_lines = validate_num_address_lines(delivery_address)
        self.delivery_address = delivery_address
        self.delivery_gps_coords = delivery_gps_coords


class PoPdfSingleLineItemDetail(object):
    '''
    A class containing all of the information that is displayed on the PDF of 
    the purchase order for a single line item.
    '''
    
    def __init__(self, part_number, product_description, unit_price, discount,
                 quantity, total_price):
        self.part_number = part_number
        self.product_description = product_description
        self.unit_price = unit_price
        self.discount = discount
        self.quantity = quantity
        self.total_price = total_price


class PoPdfLineItemDetails(object):
    '''
    A class containing all of the information about the purchase order line 
    items. This includes the total values.
    '''
    
    def __init__(self, line_items, total_excluding_tax, total_tax, 
                 total_including_tax, tax_name):
        self.line_items = line_items
        self.total_excluding_tax = total_excluding_tax
        self.total_tax = total_tax
        self.total_including_tax = total_including_tax
        self.tax_name = tax_name

        
class PoPdfSignatureDetails(object):
    '''
    A class containing all of the information required to build the signature 
    block.
    '''
    
    def __init__(self, signatory_name, signature_filename, draft=False):
        if signatory_name is None:
            raise ValueError("The signatory_name parameter is invalid.")
        if draft is False and os.path.exists(signature_filename) != True:
            raise ValueError("The signature_filename parameter is invalid.")
        self.signatory_name = signatory_name
        self.signature_filename = signature_filename
        self.draft = draft


class PoPdf(object):
    '''
    The PDF report of a purchase order (PO) comprises the following sections:
    - A letterhead showing company logo (or name), company address and contact 
      details, the order number, order date, and payment terms.
    - A supplier information block showing the supplier name, address and contact
      details.
    - A delivery information block showing the delivery address and date. 
    - A table with the items, prices and totals
    - A notes section.
    - A signature block.
    '''
    
    _GAP = Spacer(cm, 0.3*cm)
    _ITEMS_ON_FIRST_PAGE = 23
    
    def __init__(self, filename, company_details, order_details, 
                 supplier_details, delivery_details, line_item_details,
                 notes, signature_details, show_all_grids=False):
        if filename is None:
            raise ValueError("The filename parameter is invalid.")
        self.filename = filename
        if company_details is None:
            raise ValueError("The company_details parameter is invalid.")
        self.company_details = company_details
        if order_details is None:
            raise ValueError("The order_details parameter is invalid.")
        self.order_details = order_details
        if supplier_details is None:
            raise ValueError("The supplier_details parameter is invalid.")
        self.supplier_details = supplier_details
        if delivery_details is None:
            raise ValueError("The delivery_details parameter is invalid.")
        self.delivery_details = delivery_details
        if line_item_details is None:
            raise ValueError("The line_item_details parameter is invalid.")
        self.line_item_details = line_item_details 
        self.notes = notes
        if signature_details is None:
            raise ValueError("The signature_details parameter is invalid.")
        self.signature_details = signature_details
        self.show_all_grids = show_all_grids
        self.pdf = SimpleDocTemplate(self.filename,
                                     leftMargin=_LEFT_RIGHT_MARGIN_WIDTH,
                                     rightMargin=_LEFT_RIGHT_MARGIN_WIDTH,
                                     topMargin=_TOP_BOTTOM_MARGIN_WIDTH,
                                     bottomMargin=_TOP_BOTTOM_MARGIN_WIDTH)
        self.story = []
        self.stylesheet = getSampleStyleSheet()
        
    def build(self):
        self._build_letterhead_section()
        self.story.append(self._GAP)
        self._build_company_and_order_details_section()
        self.story.append(self._GAP)
        self._build_supplier_and_delivery_details_section()
        self.story.append(self._GAP)
        self._build_line_item_details_section()
        self._build_notes_section()
        self.story.append(self._GAP)
        self._build_signature_section()
        self.finalise()
        
    def _build_letterhead_section(self):
        table_data = []
        if self.company_details.logo_filename is None:
            table_data.append([self.company_details.name, 
                               "", 
                               "PURCHASE ORDER"])
        else:
            table_data.append([Image(self.company_details.logo_filename, 
                                     width=self.pdf.width/2, 
                                     height=3*cm, 
                                     kind="proportional"), 
                               "",
                               "PURCHASE ORDER"])
        col_widths = (self.pdf.width * 0.5,
                      self.pdf.width * 0.125,
                      self.pdf.width * 0.375)
        table = Table(table_data, 
                      colWidths=col_widths, 
                      hAlign="LEFT")
        table.setStyle([("FONT",     (0,0), (-1,0), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,0), 16),
                        ("VALIGN",   (-1,0), (-1,0), "MIDDLE")])
        self._show_grid_if_required(table)
        self.story.append(table)
        
    def _get_address_line(self, index):
        if len(self.company_details.address_lines) > index:
            return self.company_details.address_lines[index]
        else:
            return ""
        
    def _build_company_and_order_details_section(self):
        table_data = []
        table_data.append([self._get_address_line(0),
                           "Tel:",
                           self.company_details.phone,
                           "",
                           "Order No.: " + self.order_details.order_number])
        table_data.append([self._get_address_line(1),
                           "Fax:",
                           self.company_details.fax,
                           "",
                           "(This reference to appear on all correspondence.)"])
        col_widths = (self.pdf.width * 0.2,
                      self.pdf.width * 0.05,
                      self.pdf.width * 0.25,
                      self.pdf.width * 0.125,
                      self.pdf.width * 0.375)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN",   (0,0),  (-1,-1), "MIDDLE"),
                        ("FONT",     (-1,0), (-1,0), "Helvetica-Bold"),
                        ("FONTSIZE", (-1,0), (-1,0), 12),
                        ("FONT", (-1,-1), (-1,-1), "Helvetica-Oblique"),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0)])
        self._show_grid_if_required(table)
        self.story.append(table)
        table_data = []
        table_data.append([self._get_address_line(2),
                           "Email:",
                           self.company_details.email,
                           "",
                           "Order Date:",
                           self.order_details.order_date])
        table_data.append([self._get_address_line(3),
                           "Web:",
                           self.company_details.web,
                           "",
                           "Payment Terms:",
                           self.order_details.order_payment_terms])
        table_data.append(["",
                           "",
                           "",
                           "",
                           "",
                           ""])
        col_widths = (self.pdf.width * 0.2,
                      self.pdf.width * 0.05,
                      self.pdf.width * 0.25,
                      self.pdf.width * 0.125,
                      self.pdf.width * 0.1875,
                      self.pdf.width * 0.1875)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN",   (0,0),  (-1,-1), "MIDDLE"),
                        ("LINEBELOW", (0,-1), (-1,-1), 0.5, colors.black),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0)])
        self._show_grid_if_required(table)
        self.story.append(table)

    def _build_supplier_and_delivery_details_section(self):
        table_data = []
        table_data.append([self.supplier_details.name, 
                           "", 
                           "Delivery Details:"])
        col_widths = (self.pdf.width * 0.49,
                      self.pdf.width * 0.02,
                      self.pdf.width * 0.49)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONT", (0,0), (-1,-1), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,-1), 8),
                        ("FONTSIZE", (0,0), (0,0), 10),
                        ("LINEABOVE", (0,0), (0,0), 0.5, colors.black),
                        ("LINEABOVE", (-1,0), (-1,0), 0.5, colors.black),
                        ("LINEBEFORE", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEBEFORE", (-1,0), (-1,-1), 0.5, colors.black),
                        ("LINEAFTER", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEAFTER", (-1,0), (-1,-1), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        table_data = []
        table_data.append([self.supplier_details.address,
                           "",
                           "Delivery Address:",
                           self.delivery_details.delivery_address])
        col_widths = (self.pdf.width * 0.49,
                      self.pdf.width * 0.02,
                      self.pdf.width * 0.14,
                      self.pdf.width * 0.35)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0,0), (-1,-1), 8),
                        ("VALIGN", (0,0), (-1,-1), "TOP"),
                        ("LINEBEFORE", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEBEFORE", (-2,0), (-2,-1), 0.5, colors.black),
                        ("LINEAFTER", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEAFTER", (-1,0), (-1,-1), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        table_data = []
        table_data.append(["Tel:",
                           self.supplier_details.phone,
                           "Fax:",
                           self.supplier_details.fax,
                           "",
                           "Delivery Date:",
                           self.delivery_details.delivery_date])
        col_widths = (self.pdf.width * 0.07,
                      self.pdf.width * 0.15,
                      self.pdf.width * 0.07,
                      self.pdf.width * 0.20,
                      self.pdf.width * 0.02,
                      self.pdf.width * 0.14,
                      self.pdf.width * 0.35)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                        ("LINEBEFORE", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEBEFORE", (-2,0), (-2,-1), 0.5, colors.black),
                        ("LINEAFTER", (3,0), (3,-1), 0.5, colors.black),
                        ("LINEAFTER", (-1,0), (-1,-1), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        table_data = []
        table_data.append(["Email:",
                           self.supplier_details.email,
                           "",
                           "GPS Coords:",
                           self.delivery_details.delivery_gps_coords])
        table_data.append(["Contact:",
                           self.supplier_details.contact,
                           "",
                           "",
                           ""])
        col_widths = (self.pdf.width * 0.07,
                      self.pdf.width * 0.42,
                      self.pdf.width * 0.02,
                      self.pdf.width * 0.14,
                      self.pdf.width * 0.35)
        table = Table(table_data,
                      colWidths=col_widths,
                      hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                        ("LINEBEFORE", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEBEFORE", (-2,0), (-2,-1), 0.5, colors.black),
                        ("LINEAFTER", (1,0), (1,-1), 0.5, colors.black),
                        ("LINEAFTER", (-1,0), (-1,-1), 0.5, colors.black),
                        ("LINEBELOW", (0,-1), (1,-1), 0.5, colors.black),
                        ("LINEBELOW", (3,-1), (-1,-1), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        
    def _build_line_item_details_section(self):
        table_data = []
        table_data.append(["Part No.", 
                           "Description", 
                           "Unit Price", 
                           "Discount",
                           "Quantity",
                           "Total Price"])
        for item in self.line_item_details.line_items:
            table_data.append(item)
        blank_rows = 0
        if len(self.line_item_details.line_items) < self._ITEMS_ON_FIRST_PAGE:
            blank_rows = self._ITEMS_ON_FIRST_PAGE - \
                            len(self.line_item_details.line_items)
        for count in range(blank_rows):
            table_data.append(["",
                               "",
                               "",
                               "",
                               "",
                               ""])
        table_data.append(["",
                           "",
                           "",
                           "",
                           "Sub-total:",
                           self.line_item_details.total_excluding_tax])
        table_data.append(["",
                           "",
                           "",
                           "",
                           self.line_item_details.tax_name + ":",
                           self.line_item_details.total_tax])
        table_data.append(["",
                           "",
                           "",
                           "",
                           "Total:",
                           self.line_item_details.total_including_tax])
        col_widths = (self.pdf.width * 0.15,
                      self.pdf.width * 0.35,
                      self.pdf.width * 0.15,
                      self.pdf.width * 0.09,
                      self.pdf.width * 0.10,
                      self.pdf.width * 0.16)
        table = Table(table_data, colWidths=col_widths, hAlign="LEFT")
        table.setStyle([("FONT", (0,0), (-1,0), "Helvetica-Bold"),
                        ("FONT", (-2,-3), (-2,-1), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,-1), 8),
                        ("BOX", (0,0), (-1,-4), 0.5, colors.black),
                        ("GRID", (0,0), (-1,0), 0.5, colors.black),
                        ("GRID", (-2,-3), (-1,-1), 0.5, colors.black),
                        ("LINEAFTER", (0,0), (0,-4), 0.5, colors.black),
                        ("LINEAFTER", (1,0), (1,-4), 0.5, colors.black),
                        ("LINEAFTER", (2,0), (2,-4), 0.5, colors.black),
                        ("LINEAFTER", (3,0), (3,-4), 0.5, colors.black),
                        ("LINEAFTER", (4,0), (4,-4), 0.5, colors.black),
                        ("ALIGN", (2,0), (2,0),  "CENTER"),
                        ("ALIGN", (2,1), (2,-4), "RIGHT"),
                        ("ALIGN", (3,1), (3,-4), "CENTER"),
                        ("ALIGN", (4,0), (4,0),  "CENTER"),
                        ("ALIGN", (4,1), (4,-4), "CENTER"),
                        ("ALIGN", (5,0), (5,0),  "CENTER"),
                        ("ALIGN", (5,1), (5,-1), "RIGHT"),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                        ("TOPPADDING", (0,1), (-1,1), 5),
                        ("BOTTOMPADDING", (0,-4), (-1,-4), 5)])
        self.story.append(table)
        
    def _build_notes_section(self):
        table_data = []
        if len(self.notes) != 0:
            notes_lines = self.notes.split('\n')
            num_lines = len(notes_lines)
            if num_lines > 4:
                raise ValueError("Notes are longer than four lines.")
            buf_string = ""
            for i in range(4 - num_lines):
                buf_string += "\n"
            table_data.append(["Notes:", self.notes + buf_string])
        else:
            table_data.append(["Notes:", "None.\n\n"])
        col_widths = (self.pdf.width * 0.07,
                      self.pdf.width * 0.43)
        table = Table(table_data, colWidths=col_widths, hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN", (0,0), (-1,-1), "TOP"),
                        ("FONT", (0, 0), (0, 0), "Helvetica-Bold"),
                        ("LINEABOVE", (0,0), (-1,0), 0.5, colors.black),
                        ("LINEBEFORE", (0,0), (0,-1), 0.5, colors.black),
                        ("LINEAFTER", (-1,0), (-1,-1), 0.5, colors.black),
                        ("LINEBELOW", (0,-1), (-1,-1), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        
    def _build_signature_section(self):
        table_data = [] 
        if not self.signature_details.signature_filename:
            table_data.append(["Authorised By:",
                               Spacer(cm, 1.5*cm)])
        else:
            table_data.append(["Authorised By:",
                               Image(self.signature_details.signature_filename,
                                     width=self.pdf.width/2,
                                     height=1.5*cm,
                                     kind="proportional")])
        table_data.append(["",
                           "Signature"])
        table_data.append(["",
                           self.signature_details.signatory_name])
        table_data.append(["",
                           "Print Name"])
        col_widths = (self.pdf.width * 0.15,
                      self.pdf.width * 0.3)
        table = Table(table_data, colWidths=col_widths, hAlign="LEFT")
        table.setStyle([("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                        ("ALIGN",  (1, 0), (1, -1), "CENTER"),
                        ("FONT",   (0, 0), (0, 0), "Helvetica-Bold"),
                        ("FONT",   (1, 1), (1, 1), "Helvetica-Bold"),
                        ("FONT",   (1, -1), (1, -1), "Helvetica-Bold"),
                        ("LINEBELOW", (1,0), (1,0), 0.5, colors.black),
                        ("LINEBELOW", (1,2), (1,2), 0.5, colors.black)])
        self._show_grid_if_required(table)
        self.story.append(table)
        
    def add_footer_text(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(_LEFT_RIGHT_MARGIN_WIDTH, 
                          _TOP_BOTTOM_MARGIN_WIDTH,
                          self.company_details.name)
        canvas.drawCentredString(A4[0]/2,
                                 _TOP_BOTTOM_MARGIN_WIDTH,
                                 "Purchase Order " + \
                                 self.order_details.order_number)
        canvas.restoreState()
        
    def finalise(self):
        self.pdf.build(self.story, 
                       onFirstPage=self.add_footer_text,
                       onLaterPages=self.add_footer_text,
                       canvasmaker=PoPdfPageXofYCanvas)
        
    def _show_grid_if_required(self, table):
        if self.show_all_grids is True:
            table.setStyle([("GRID", (0,0), (-1,-1), 0.5, colors.black)])


class ReportPdfPageXofYCanvas(Canvas):
    '''
    Subclass of the Canvas class that saves page states and allows the 
    "Page X of Y" string to be printed in the footer of the page once the  
    document has been built.
    Straight copy from a recipe on ActiveState website:
    http://code.activestate.com/recipes/576832/
    '''
    
    _LEFT_RIGHT_MARGIN_WIDTH = cm
    _TOP_BOTTOM_MARGIN_WIDTH = cm
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        """
        Add "Page X of Y" string to the footer of each page.
        """
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)
        
    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(landscape(A4)[0] - self._LEFT_RIGHT_MARGIN_WIDTH,
                             landscape(A4)[1] - self._TOP_BOTTOM_MARGIN_WIDTH,
            "Page %d of %d" % (self._pageNumber, page_count))


class ReportPdfSingleLineItemDetail(object):
    '''
    A class containing all of the information that is displayed on the PDF of 
    the report for a single line item.
    '''
    
    def __init__(self, order_number, order_date, order_status, 
                 project, supplier, part_number, product_description, 
                 unit_price, discount, quantity, total_price):
        self.order_number = order_number
        self.order_date = order_date
        self.order_status = order_status
        self.project = project
        self.supplier = supplier
        self.part_number = part_number
        self.product_description = product_description
        self.unit_price = unit_price
        self.discount = discount
        self.quantity = quantity
        self.total_price = total_price


class ReportPdfLineItemDetails(object):
    '''
    A class containing all of the information about the report line items. 
    This includes the total value.
    '''
    
    def __init__(self, line_items, total_value):
        self.line_items = line_items
        self.total_value = total_value


class ReportPdf(object):
    
    _LEFT_RIGHT_MARGIN_WIDTH = cm
    _TOP_BOTTOM_MARGIN_WIDTH = cm
    _HALF_CM = 0.5*cm
    
    def __init__(self, filename, report_type, report_filter, start_date, 
                 end_date, line_item_details, company_name, 
                 show_all_grids=False):
        if filename is None:
            raise ValueError("The filename parameter is invalid.")
        self.filename = filename
        self.report_type = report_type
        self.report_filter = report_filter
        self.start_date = start_date
        self.end_date = end_date 
        if line_item_details is None:
            raise ValueError("The line_item_details parameter is invalid.")
        self.line_item_details = line_item_details
        self.company_name = company_name 
        self.show_all_grids = show_all_grids
        self.date = datetime.date.today()
        self.pdf = SimpleDocTemplate(self.filename,
                                     pagesize=landscape(A4),
                                     leftMargin=self._LEFT_RIGHT_MARGIN_WIDTH,
                                     rightMargin=self._LEFT_RIGHT_MARGIN_WIDTH,
                                     topMargin=2.5*self._TOP_BOTTOM_MARGIN_WIDTH,
                                     bottomMargin=self._TOP_BOTTOM_MARGIN_WIDTH)
        self.story = []
        self.stylesheet = getSampleStyleSheet()
        
    def build(self):
        self._build_line_item_table()
        self.finalise()
        
    def _build_line_item_table(self):
        table_data = []
        table_data.append(["Order No.",
                           "Order Date",
                           "Status",
                           "Project",
                           "Supplier",
                           "Part No.", 
                           "Description", 
                           "Unit Price", 
                           "Discount",
                           "Quantity",
                           "Total Price"])
        for item in self.line_item_details.line_items:
            table_data.append(item)
        table_data.append(["",
                           "",
                           "",
                           "",
                           "",
                           "",
                           "",
                           "",
                           "",
                           "Total:",
                           self.line_item_details.total_value])
        col_widths = (self.pdf.width * 0.06,
                      self.pdf.width * 0.08,
                      self.pdf.width * 0.06,
                      self.pdf.width * 0.1,
                      self.pdf.width * 0.1,
                      self.pdf.width * 0.1,
                      self.pdf.width * 0.2,
                      self.pdf.width * 0.09,
                      self.pdf.width * 0.06,
                      self.pdf.width * 0.06,
                      self.pdf.width * 0.09)
        table = Table(table_data, 
                      colWidths=col_widths,
                      repeatRows=1, 
                      hAlign="LEFT")
        table.setStyle([("FONT", (0,0), (-1,0), "Helvetica-Bold"),
                        ("FONT", (-2,-1), (-1,-1), "Helvetica-Bold"),
                        ("FONTSIZE", (0,0), (-1,-1), 8),
                        ("BOX", (0,0), (-1,-2), 0.5, colors.black),
                        ("GRID", (0,0), (-1,0), 0.5, colors.black),
                        ("GRID", (-2,-1), (-1,-1), 0.5, colors.black),
                        ("LINEAFTER", (0,0), (0,-2), 0.5, colors.black),
                        ("LINEAFTER", (1,0), (1,-2), 0.5, colors.black),
                        ("LINEAFTER", (2,0), (2,-2), 0.5, colors.black),
                        ("LINEAFTER", (3,0), (3,-2), 0.5, colors.black),
                        ("LINEAFTER", (4,0), (4,-2), 0.5, colors.black),
                        ("LINEAFTER", (5,0), (5,-2), 0.5, colors.black),
                        ("LINEAFTER", (6,0), (6,-2), 0.5, colors.black),
                        ("LINEAFTER", (7,0), (7,-2), 0.5, colors.black),
                        ("LINEAFTER", (8,0), (8,-2), 0.5, colors.black),
                        ("LINEAFTER", (9,0), (9,-2), 0.5, colors.black),
                        ("LINEAFTER", (10,0), (10,-2), 0.5, colors.black),
                        ("LINEBELOW", (0,"splitlast"), (-1,"splitlast"), 0.5, colors.black),
                        ("ALIGN", (1,0), (1,-1),  "CENTER"),
                        ("ALIGN", (2,0), (2,-1),  "CENTER"),
                        ("ALIGN", (7,0), (7,-1),  "RIGHT"),
                        ("ALIGN", (8,0), (8,-1),  "CENTER"),
                        ("ALIGN", (9,0), (9,-1),  "CENTER"),
                        ("ALIGN", (10,0), (10,-1),  "RIGHT"),
                        ("TOPPADDING", (0,0), (-1,-1), 0),
                        ("BOTTOMPADDING", (0,0), (-1,-1), 0)])
        self.story.append(table)
        
    def _make_landscape_and_add_header(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(landscape(A4))
        canvas.setFont("Helvetica", 8)
        canvas.drawString(self._LEFT_RIGHT_MARGIN_WIDTH, 
                          landscape(A4)[1] - self._TOP_BOTTOM_MARGIN_WIDTH,
                          self.company_name)
        canvas.drawString(self._LEFT_RIGHT_MARGIN_WIDTH, 
                          landscape(A4)[1] - self._TOP_BOTTOM_MARGIN_WIDTH - self._HALF_CM,
                          self.report_type + ": " + self.report_filter)
        canvas.drawRightString(landscape(A4)[0] - self._LEFT_RIGHT_MARGIN_WIDTH,
                               landscape(A4)[1] - self._TOP_BOTTOM_MARGIN_WIDTH - self._HALF_CM,
                               str(self.date))
        canvas.drawString(self._LEFT_RIGHT_MARGIN_WIDTH, 
                          landscape(A4)[1] - self._TOP_BOTTOM_MARGIN_WIDTH - 2*self._HALF_CM,
                          "Start Date: " + str(self.start_date) + "  End Date: " + str(self.end_date))
        canvas.restoreState()
        
    def finalise(self):
        self.pdf.build(self.story, 
                       onFirstPage=self._make_landscape_and_add_header,
                       onLaterPages=self._make_landscape_and_add_header,
                       canvasmaker=ReportPdfPageXofYCanvas)