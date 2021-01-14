from marshmallow import Schema, fields, validates, validate, ValidationError
import datetime as dt
from gateways import * 

class PaymentSchema(Schema):
    CreditCardNumber =  fields.String(
                            required=True, 
                            error_messages={"required": "CreditCardNumber is required."})
    CardHolder = fields.String(
                            required=True, 
                            error_messages={"required": "CardHolder is required."})
    ExpirationDate = fields.DateTime(
                            required=True, 
                            error_messages={"required": "ExpirationDate is required."})
    Amount = fields.Decimal(
                            required=True, 
                            error_messages={"required": "Amount is required."},
                            validate=validate.Range(min=0.0))
    SecurityCode = fields.String(
                            required=False,
                            validate=validate.Length(equal=3))


    @validates("CreditCardNumber")
    def validate_CreditCardNumber(self, card_no):
        isvalid = False

        if len(card_no.strip()) > 10 and card_no.isnumeric():
            #double every second digit from right to left: luhn Algo
            sum_=0
            crd_no = card_no[::-1]
            for i in range(len(crd_no)):
                if i%2==1:
                    double_it = int(crd_no[i])*2
                    #if not single digit add two digits
                    if len(str(double_it))==2:
                        sum_ += sum([int(i) for i in str(double_it)])
                    else:
                        sum_+=double_it
                else:
                    sum_+=int(crd_no[i])
            if sum_%10!=0:
                raise ValidationError("Not a Valid Credit Card Number")
        else:
            raise ValidationError("Not a Valid Credit Card Number")

    @validates("ExpirationDate")
    def validate_ExpirationDate(self, exp_date):
        if exp_date<dt.datetime.now():
            raise ValidationError("Card Expired!")

def choose_gateway(amount):
    gateway = None
    retries = 0

    if amount <= 20:
        gateway = CheapPaymentGateway
    elif 21<= amount <=50:
        if ExpensivePaymentGateway().isavailable():
            gateway = ExpensivePaymentGateway
        else:
           gateway = CheapPaymentGateway
           retries = 1
    else:
        gateway = PremiumPaymentGateway
        retries = 3
    return gateway, retries

# class CreditCard:
#     def __init__(self,card_no):
#         self.card_no = card_no

#     @property
#     def company(self):
#         comp =None
#         if str(self.card_no).startswith('4'):
#              comp = 'Visa Card'
#         elif str(self.card_no).startswith('5'):
#             comp = 'Master Card'
#         elif str(self.card_no).startswith('37'):
#             comp = 'American Express Card'
#         elif str(self.card_no).startswith('6'):
#             comp = 'Discover Card'
#         elif str(self.card_no).startswith('35'):
#             comp = 'JCB Card'
#         elif str(self.card_no).startswith('50' or '67'or '58'or'63'):
#             comp = 'Maestro Card'
#         elif str(self.card_no).startswith('7'):
#             comp = 'Gasoline Card'

#         return 'Company : '+comp

#     def first_check(self):
#         if 13<=len(self.card_no)<=19:
#             message = "First check : Valid in terms of length."
#         else:
#             message = "First check : Check Card number once again it must be of 13 or 16 digit long."
#         return message

#     def validate(self):
#         isvalid = False
#         #double every second digit from right to left
#         sum_=0
#         crd_no = self.card_no[::-1]
#         for i in range(len(crd_no)):
#             if i%2==1:
#                 double_it = int(crd_no[i])*2
#                 #if not single digit add two digits
#                 if len(str(double_it))==2:
#                     sum_ += sum([int(i) for i in str(double_it)])
#                 else:
#                     sum_+=double_it
#             else:
#                 sum_+=int(crd_no[i])
#         if sum_%10==0:
#             isvalid =True
#         return isvalid

#     @property
#     def checksum(self):
#         return '#CHECKSUM# : '+self.card_no[-1]

#     @classmethod
#     def set_card(cls,card_to_check):
#         return cls(card_to_check)