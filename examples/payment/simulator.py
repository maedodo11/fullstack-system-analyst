"""Sequential educational model; no bank, persistence, locks or TTL."""
from dataclasses import dataclass

STATUSES = {'PENDING', 'UNKNOWN', 'SUCCESS', 'FAILED', 'CANCELLED'}
TRANSITIONS = {
    'PENDING': {'UNKNOWN', 'SUCCESS', 'FAILED', 'CANCELLED'},
    'UNKNOWN': {'SUCCESS', 'FAILED'},
    'SUCCESS': set(), 'FAILED': set(), 'CANCELLED': set(),
}

class Conflict(ValueError):
    pass

@dataclass
class Payment:
    payment_id: str
    order_id: str
    status: str = 'PENDING'
    dispatched: bool = False

class PaymentModel:
    def __init__(self):
        self.orders = {'O123': {'owner': 'buyer-A', 'amount_minor': 150000, 'paid': False}}
        self.payments = {}
        self.keys = {}
        self.events = {}

    def create(self, owner, key, order_id, token):
        if not key or not token:
            raise ValueError('INVALID_REQUEST')
        order = self.orders.get(order_id)
        if order is None or order['owner'] != owner:
            raise PermissionError('NOT_FOUND')
        scoped = (owner, 'FULL_PAYMENT', key)
        request = (order_id, token)
        if scoped in self.keys:
            previous, payment_id = self.keys[scoped]
            if request != previous:
                raise Conflict('IDEMPOTENCY_CONFLICT')
            return self.payments[payment_id]
        if order['paid']:
            raise Conflict('ORDER_PAID')
        if any(p.order_id == order_id and p.status in {'PENDING','UNKNOWN'}
               for p in self.payments.values()):
            raise Conflict('PAYMENT_ACTIVE')
        payment = Payment(f'P{len(self.payments)+1}', order_id)
        self.payments[payment.payment_id] = payment
        self.keys[scoped] = (request, payment.payment_id)
        return payment

    def transition(self, payment_id, target):
        payment = self.payments[payment_id]
        if target not in STATUSES:
            raise ValueError('INVALID_STATUS')
        if target == payment.status:
            return payment
        if target not in TRANSITIONS[payment.status]:
            raise Conflict('INVALID_TRANSITION')
        if target == 'CANCELLED' and payment.dispatched:
            raise Conflict('PROVIDER_RESULT_REQUIRED')
        payment.status = target
        if target == 'SUCCESS':
            self.orders[payment.order_id]['paid'] = True
        return payment

    def webhook(self, event_id, payment_id, target):
        # Signature/schema/amount validation is assumed to have happened upstream.
        payload = (payment_id, target)
        if event_id in self.events:
            if self.events[event_id] != payload:
                raise Conflict('EVENT_ID_CONFLICT')
            return self.payments[payment_id]
        payment = self.transition(payment_id, target)
        self.events[event_id] = payload
        return payment
