import random
#using random choice to make a dummy gateway to get response True/False for processing retries

payment_processed_status = (True, False)
availability_status = (True, False)

class Gateway:
	def __init__(self, CreditCard=None, max_retries=0):
		self.cc = CreditCard
		self.max_retries = max_retries
		self.gateway_charges = 0

	def checkout(self):
		for retry in range(self.max_retries+1):
			is_processed = random.choice(payment_processed_status)
			if is_processed:
				break
		return is_processed

	def isavailable(self):
		return random.choice(availability_status)

	def set_gateway_charges(self, amount):
		self.gateway_charges = amount


class PremiumPaymentGateway(Gateway):
	def _init__(self, max_retries=0):
		self.set_gateway_charges(20)
		self.max_retries = max_retries

class ExpensivePaymentGateway(Gateway):
	def _init__(self, max_retries=0):
		self.set_gateway_charges(5)
		self.max_retries = max_retries

class CheapPaymentGateway(Gateway):
	def _init__(self, max_retries=0):
		self.set_gateway_charges(1)
		self.max_retries = max_retries