from store.models import OrderModel
from django.contrib.auth.models import User


class CookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before rendering view
        response = self.get_response(request)
        # After rendering view
        if request.user.is_authenticated:
            if not getattr(request, "user_id", None):
                response.set_cookie("user_id", request.user.pk)
            if not getattr(request, "user_basket", None):
                response.set_cookie("user_basket", dict())

            # get current user object
            user_obj = User.objects.get(username=request.user.username)
            user_orders = OrderModel.objects.filter(user=user_obj)

            flag = False
            for order in user_orders:
                if order.status == "inprocess" or not order.status == "prepayment":
                    flag = True

            if not flag:
                OrderModel.objects.create(
                    user=user_obj,
                )

        return response
