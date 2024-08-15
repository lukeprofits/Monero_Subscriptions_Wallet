import factory
import monerorequest
from datetime import datetime
from src.subscription import Subscription

class SubscriptionFactory(factory.Factory):
    class Meta:
        model = Subscription

    custom_label = factory.Sequence(lambda n: 'Subscription %s' % n)
    sellers_wallet = '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S'
    currency = 'USD'
    amount = '10'
    payment_id = monerorequest.make_random_payment_id()
    start_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    days_per_billing_cycle = 7
    number_of_payments = 10