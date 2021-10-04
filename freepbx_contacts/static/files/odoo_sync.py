# ©️ OdooPBX by Odooist, Odoo Proprietary License v1.0, 2020
#!/usr/bin/env python
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import mysql.connector as mysql
import requests


class OdooSync:
    def load_config(self):
        # Read config
        config = ConfigParser.ConfigParser()
        config.readfp(open('odoo_sync.cfg'))
        self.config = config

    def get_odoo_partners(self):
        data = requests.get(
            '{}/{}'.format(
                self.config.get('odoo', 'url'), 'freepbx_contacts'),
            json={'token': self.config.get('odoo', 'token'),
                  'db': self.config.get('odoo', 'db')},
            headers={'Content-type': 'application/json'})
        data.raise_for_status()
        return data.json()['result']

    def connect_mysql(self):
        self.db = mysql.connect(
            host=self.config.get('mysql', 'host'),
            user=self.config.get('mysql', 'user'),
            passwd=self.config.get('mysql', 'passwd'),
            database=self.config.get('mysql', 'db')
        )

    def create_odoo_group(self):
        c = self.db.cursor()
        c.execute("SELECT id FROM contactmanager_groups WHERE name = 'Odoo'")
        group_id = c.fetchone()
        if not group_id:
            c.execute("""INSERT INTO contactmanager_groups (name, owner, type)
                         VALUES ('Odoo', -1, 'external')""")
            self.db.commit()
            group_id = (c.lastrowid,)
        # Set contact group for future use
        self.odoo_group_id = group_id[0]

    # Get all partners
    def sync_partners(self):
        partners = self.get_odoo_partners()
        for partner in partners:
            self.sync_partner(partner)

    def sync_partner(self, partner):
       # Find an existing record or create it.
        c = self.db.cursor()
        p = partner
        c.execute("""SELECT id FROM contactmanager_group_entries
                 WHERE displayname = %s""", (p['name'],))
        contact_id = c.fetchone()
        if not contact_id:
            # New contact
            if not (p['phone'] or p['mobile']):
                # No phones for the contact just ommit.
                return
            # New record, create.
            address = '{} {} {} {}'.format(
                p['street'] or '', p['street2'] or '', p['zip'] or '', p['city'] or '')
            c.execute("""INSERT INTO contactmanager_group_entries
                (groupid, displayname, title, address, uuid)
                VALUES(%s, %s, %s, %s, UUID())""", (self.odoo_group_id,
                                            partner['name'],
                                            partner['title'] or '', address))
            contact_id = (c.lastrowid,)
            self.db.commit()
        if True:
            # Delete existing entries
            c.execute("""DELETE FROM contactmanager_entry_numbers
                      WHERE entryid = {}""".format(contact_id[0]))
            # Create numbers
            if p['phone']:
               c.execute("""INSERT INTO contactmanager_entry_numbers
                         (entryid, number, type)
                   VALUES(%s, %s, %s)""", (contact_id[0], p['phone'], 'work'))
            if p['mobile']:
               c.execute("""INSERT INTO contactmanager_entry_numbers
                         (entryid, number, type)
                   VALUES(%s, %s, %s)""", (contact_id[0], p['mobile'], 'cell'))
            # Create email
            if p['email']:
               c.execute("""INSERT INTO contactmanager_entry_emails
                         (entryid, email) VALUES(%s, %s)""",
                   (contact_id[0], p['email']))
            # Create website
            if p['website']:
               c.execute("""INSERT INTO contactmanager_entry_websites
                         (entryid, website) VALUES(%s, %s)""",
                   (contact_id[0], p['website']))
            # Commit changes
            self.db.commit()

if __name__ == '__main__':
    odoo_sync = OdooSync()
    odoo_sync.load_config()
    odoo_sync.connect_mysql()
    odoo_sync.create_odoo_group()
    odoo_sync.sync_partners()
