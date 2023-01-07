from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class OrderToken:
    order_prices = None
    token = None
    user_info = None

    def create_token(self, user, prices):
        self.order_prices = "".join(prices)
        self.user_info = str(user.email) + str(user.id)
        self.token = urlsafe_base64_encode(
            force_bytes(self.order_prices + self.user_info)
        )

    def check_token(self, token):
        if urlsafe_base64_decode(token) == force_bytes(
            self.order_prices + self.user_info
        ):
            self.order_prices = None
            token = None
            return True
        else:
            return False


generate_order_token = OrderToken()
