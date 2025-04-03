from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from stores.models import Store, Item
from orders.models import Order, OrderItem, OrderBatch

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='customer', password='password123')
        self.agent = User.objects.create_user(username='agent', password='password123')
        self.store = Store.objects.create(name='Test Store')
        self.item = Item.objects.create(name='Test Item', price=10.00, store=self.store, stock=10)
        self.order = Order.objects.create(
            user=self.user,
            store=self.store,
            total_amount=20.00,
            status='PENDING',
            payment_method='COD',
            address='123 Street',
            city='Test City',
            state='Test State',
            pincode='123456',
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            item=self.item,
            quantity=2,
            price=10.00
        )

    def test_order_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.total_amount, 20.00)
        self.assertEqual(self.order.status, 'PENDING')

    def test_order_item_creation(self):
        self.assertEqual(self.order.items.count(), 1)
        self.assertEqual(self.order.items.first().subtotal, 20.00)
    
    def test_order_status_update(self):
        self.order.status = 'DELIVERED'
        self.order.save()
        self.assertEqual(Order.objects.get(id=self.order.id).status, 'DELIVERED')

    def test_order_payment_method(self):
        self.assertEqual(self.order.payment_method, 'COD')

    def test_order_address_details(self):
        self.assertEqual(self.order.address, '123 Street')
        self.assertEqual(self.order.city, 'Test City')
        self.assertEqual(self.order.state, 'Test State')
        self.assertEqual(self.order.pincode, '123456')

    def test_order_item_quantity(self):
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 10.00)
        self.assertEqual(self.order_item.item.name, 'Test Item')

    def test_order_store_link(self):
        self.assertEqual(self.order.store.name, 'Test Store')
        self.assertEqual(self.order_item.item.store.name, 'Test Store')

    def test_order_total_amount_calculation(self):
        expected_total = sum(item.subtotal for item in self.order.items.all())
        self.assertEqual(self.order.total_amount, expected_total)

class OrderBatchTest(TestCase):
    def setUp(self):
        self.agent = User.objects.create_user(username='agent', password='password123')
        self.batch = OrderBatch.objects.create(
            delivery_agent=self.agent,
            status='PENDING',
            date=now().date(),
        )

    def test_batch_creation(self):
        self.assertEqual(OrderBatch.objects.count(), 1)
        self.assertEqual(self.batch.status, 'PENDING')
