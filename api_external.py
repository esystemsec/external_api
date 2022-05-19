import xmlrpc.client  # library
url = "https://esystemsec-eassist-staging-4903254.dev.odoo.com"  # url database instance
db = "esystemsec-eassist-staging-4903254"  # name database
username = "admin"  # name user
password = "@FYf#!@Zzm$vXK*yG"  # pass user

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})  # login
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))  # instance object model
partners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [
    [['vat', '=', '0301855195']]], {'fields': ['name', 'vat', 'phone'], 'limit': 1})  # search for partners with vat 0301855195

# Since there is no partner, it proceeds to create a partner
if not partners:
    partners = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        'company_type': "person",  # Seleccionar  "company" si es una empresa o "person" si es una persona natural
        'l10n_latam_identification_type_id': 6,  # Seleccionar 4 si es RUC, 5 si es Cédula, 6 Si es Pasaporte u 8 si es Consumidor final
        'name': "Oscar Morocho Lema 2",
        'street': "Av 24 Mayo",
        'street2': "Solano",
        'vat': "0301855195",
        'phone': "0992611108",
        'mobile': "om@prisehub.com",
        'website': "www.esystems.ec",
        'lang': "es_EC",
    }])
    partners = [partners]

# With the obtained partner we can create an invoice


new_invoice = models.execute_kw(db, uid, password, 'account.move', 'create', [{
    'state': "draft",
    'partner_id': partners[0],  # Customer ID
    'move_type': 'out_invoice',
    'l10n_ec_sri_payment_id': 7,
}])

# Create a payment

new_payment = models.execute_kw(db, uid, password, 'account.payment', 'create', [{
    'partner_id': partners[0],  # Customer ID
    'payment_type': 'inbound',
    'amount': 40,  # Value payment
}])
