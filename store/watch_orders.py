import time
from store.models import OrderModel
from datetime import date
import schedule


def is_delivery_time() -> None:
    orders = OrderModel.objects.filter(status="Inprocess")
    today = date.today()
    delivery_dates = {order.id: order.delivery_date for order in orders}

    for order_id, order_delivery_date in delivery_dates.items():
        if order_delivery_date == today:
            order_obj = OrderModel.objects.get(pk=order_id, delivery_date=order_delivery_date)
            order_obj.status = "Delivered"
            order_obj.save()


schedule.every().day.at("12:00").do(is_delivery_time)

while True:
    schedule.run_pending()
    time.sleep(1)
