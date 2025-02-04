# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Customer and Supplier Loan Management',
    'version' : '1.1.6',
    'category': 'Accounting',
    'depends' : ['account', 
                 'portal',
#                  'website_portal',
                'website',
                 ],
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'images': ['static/description/im2.jpg'],
    'price': 99.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': 'This module allow to manage loan of your Customers/Suppliers/Partners.',
    'website': 'www.probuse.com',
    'live_test_url': 'https://youtu.be/DwmI-R_au4Y',
    'description': ''' 
loan detail report should be verify
Loan management Integrated with payroll
This module allow HR department to manage loan of employees
Loan Request
Loan Approval
Loan Disburse
Loan Repayment
Loan Policy
Loan proof
customer loan
loan management
loan
loan request
loan supplier
odoo loan
loan for customer
loan disburse
loan given
customer loan receive
loan proofs
customer loan
supplier loan
employee loan
vendor loan
external loan
agent loan
bank loan
loan
loan module
loan app
odoo loan
loan odoo
loan app odoo
loan to customer
loan to supplier
loan defaulter
loan management
loan software
Disburse Loan
loan Disburse
loan journal entry
loan accounting
loan accounting entry
loan account
loan interest
loan data
loan manager
loan user
loan request
loan module odoo
Allowed Loan Manager to add Loan Proofs/Required Documents List.
Allowed Loan Manager to add Loan Types.
Allowed Loan Manager to add Loan Policies.
Allowed Loan User and Manager to create Loan Request.
Allowed Loan Manager to Approve Loan Request.
Unique Sequence for Loan Request.
Allowed Accountant to Loan Disburse.
Create Disburse Accounting Journal Entry.
Create Interest Receivable on Loan Accounting Journal Entry.
Allowed Accountant to Receive Loan Installments.
Book Interest for Installment Accounting Entry.
Pay Installment Accounting Journal Entry.
It will Create Interest on Loan Journal Entry and Loan Installment Accounting Entry.
Allowed you to Print Loan Report.
Allowed your Customers to see their Loans in Portal My Account Page.

 ''',
    'demo' : [
            #'views/loan_payroll_demo.xml'
              ],
    'data' : [
        'security/loan_security.xml',
        'security/ir.model.access.csv',
        'views/loan_payroll.xml',
        #'views/prepayment_writeoff_view.xml',  #dd
#         'views/loan_payroll_workflow.xml',
        'data/loan_payroll_sequence.xml',
#         'report/loan_payroll_report_view.xml',  #dd
#         'wizard/loan_report_wiz_view.xml',  #dd
#         'loan_details_report_view.xml',  #dd
        'views/payment.xml',#todoprobuse
        'views/loan_proof.xml',
        'report/loan_detail_reg.xml',
        'report/loan_detail_view.xml',
        'views/my_loan.xml',
        'views/account_views.xml',
#         'views/hr_salary_rule_view.xml', #todo check
#        comment by probuse 'report/loan_report_view.xml'   #dd
    ],
    'installable': True,
    'application': False,
}
