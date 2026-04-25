import base64
import io
import csv
import logging
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except ImportError:
    openpyxl = None

class DataImportWizard(models.TransientModel):
    _name = 'nursery.data.import.wizard'
    _description = 'Data Import Wizard'

    file = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')

    def action_import(self):
        self.ensure_one()
        if not self.file:
            raise UserError(_("Please upload a file."))

        file_content = base64.b64decode(self.file)
        
        # Determine file type
        if self.file_name.endswith('.xlsx'):
            if not openpyxl:
                raise UserError(_("The openpyxl python library is not installed. Please upload a CSV file instead."))
            data = self._read_xlsx(file_content)
        elif self.file_name.endswith('.csv'):
            data = self._read_csv(file_content)
        else:
            raise UserError(_("Unsupported file format. Please upload a .xlsx or .csv file."))

        if not data:
            raise UserError(_("The uploaded file is empty or could not be read."))

        # Process data
        # Expected columns: Student Name, Gender, Date of Birth, Class, Parent/Guardian, Parent/Guardian/Email
        
        Student = self.env['nursery.student']
        Class = self.env['nursery.class']
        Partner = self.env['res.partner']
        User = self.env['res.users']
        PortalGroup = self.env.ref('base.group_portal')

        # Skip header row if it exists (check first row for known column names)
        start_idx = 0
        if data and len(data) > 0 and data[0] and str(data[0][0]).strip().lower() in ['student name', 'student']:
            start_idx = 1

        success_count = 0
        for row in data[start_idx:]:
            if not row or len(row) < 6:
                continue # Skip empty or invalid rows
            
            student_name = str(row[0]).strip() if row[0] is not None else ""
            if not student_name:
                continue
                
            gender_raw = str(row[1]).strip().lower() if row[1] is not None else ""
            if gender_raw in ['male', 'm']:
                gender = 'male'
            elif gender_raw in ['female', 'f']:
                gender = 'female'
            else:
                gender = 'other'
                
            # Parse Date of Birth
            dob_raw = row[2]
            dob = False
            if dob_raw:
                if isinstance(dob_raw, datetime):
                    dob = dob_raw.date()
                else:
                    try:
                        # try various formats
                        for fmt in ('%d-%b-%y', '%d-%b-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                            try:
                                dob = datetime.strptime(str(dob_raw).strip(), fmt).date()
                                break
                            except ValueError:
                                pass
                    except Exception as e:
                        _logger.warning("Could not parse DOB %s: %s", dob_raw, e)
            
            class_name = str(row[3]).strip() if row[3] is not None else ""
            parent_name = str(row[4]).strip() if row[4] is not None else ""
            parent_email = str(row[5]).strip() if row[5] is not None else ""

            # Find or create Class
            class_record = False
            if class_name:
                class_record = Class.search([('name', '=ilike', class_name)], limit=1)
                if not class_record:
                    class_record = Class.create({'name': class_name})

            # Find or create Parent
            parent_record = False
            if parent_email:
                parent_record = Partner.search([('email', '=ilike', parent_email)], limit=1)
            elif parent_name:
                parent_record = Partner.search([('name', '=ilike', parent_name)], limit=1)
                
            if not parent_record and parent_name:
                parent_record = Partner.create({
                    'name': parent_name,
                    'email': parent_email or False,
                })
            elif parent_record and not parent_record.email and parent_email:
                parent_record.email = parent_email

            # Create Portal User for Parent if email exists
            if parent_record and parent_email:
                user = User.sudo().search([('partner_id', '=', parent_record.id)], limit=1)
                if not user:
                    existing_login = User.sudo().search([('login', '=', parent_email)], limit=1)
                    if not existing_login:
                        user = User.sudo().create({
                            'name': parent_record.name,
                            'login': parent_email,
                            'partner_id': parent_record.id,
                            'groups_id': [(6, 0, [PortalGroup.id])],
                            'password': parent_email,
                        })
                    else:
                        # Login taken by someone else
                        pass
                else:
                    # Update existing user password and portal group
                    if PortalGroup.id not in user.groups_id.ids:
                        user.sudo().write({'groups_id': [(4, PortalGroup.id)]})
                    user.sudo().write({'password': parent_email})

            # Create Student
            Student.create({
                'name': student_name,
                'gender': gender,
                'dob': dob,
                'class_id': class_record.id if class_record else False,
                'parent_id': parent_record.id if parent_record else False,
            })
            success_count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Successful'),
                'message': _('%s students imported successfully.', success_count),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def _read_xlsx(self, file_content):
        wb = openpyxl.load_workbook(filename=io.BytesIO(file_content), data_only=True)
        sheet = wb.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        return data

    def _read_csv(self, file_content):
        # Decode content, try utf-8 first, then fallback to latin-1
        try:
            decoded_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            decoded_content = file_content.decode('latin-1')
        
        reader = csv.reader(io.StringIO(decoded_content))
        data = list(reader)
        return data
