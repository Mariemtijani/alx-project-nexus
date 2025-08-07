import graphene
from graphene_django import DjangoObjectType
from orders.models import Order, OrderItem
from users.models import User
from products.models import Product
from graphql import GraphQLError
from common.pagination import PaginationInput, PageInfo, paginate_queryset

# -------- Types --------
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price")

class OrderType(DjangoObjectType):
    items = graphene.List(OrderItemType)

    class Meta:
        model = Order
        fields = ("id", "buyer", "total_amount", "status", "order_date", "shipping_address", "tracking_number", "created_at", "updated_at")

    def resolve_items(self, info):
        return OrderItem.objects.filter(order=self)

# -------- Input Object Type --------
class OrderItemInput(graphene.InputObjectType):
    product_id = graphene.UUID(required=True)
    quantity = graphene.Int(required=True)
    unit_price = graphene.Float(required=True)

# -------- Paginated Orders Type --------
class PaginatedOrders(graphene.ObjectType):
    orders = graphene.List(OrderType)
    page_info = graphene.Field(PageInfo)

# -------- Queries --------
class OrderQuery(graphene.ObjectType):
    all_orders = graphene.Field(PaginatedOrders, pagination=PaginationInput())
    order = graphene.Field(OrderType, id=graphene.UUID(required=True))

    def resolve_all_orders(self, info, pagination=None):
        if pagination is None:
            pagination = PaginationInput()
        queryset = Order.objects.select_related('buyer').all()
        orders, page_info = paginate_queryset(queryset, pagination)
        return PaginatedOrders(orders=orders, page_info=page_info)

    def resolve_order(self, info, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise GraphQLError('Order not found')

# -------- Mutations --------
class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        buyer_id = graphene.UUID(required=True)
        shipping_address = graphene.String(required=True)
        items = graphene.List(OrderItemInput, required=True)

    def mutate(self, info, buyer_id, shipping_address, items):
        try:
            buyer = User.objects.get(id=buyer_id, role='buyer')
        except User.DoesNotExist:
            raise GraphQLError('Buyer not found')

        order = Order(buyer=buyer, shipping_address=shipping_address, total_amount=0, status='pending')
        order.save()

        total_amount = 0
        for item_data in items:
            try:
                product = Product.objects.get(id=item_data.product_id)
            except Product.DoesNotExist:
                raise GraphQLError(f'Product {item_data.product_id} not found')

            item = OrderItem(order=order, product=product, quantity=item_data.quantity, unit_price=item_data.unit_price)
            item.save()
            total_amount += item_data.quantity * item_data.unit_price

        order.total_amount = total_amount
        order.save()
        return CreateOrder(order=order)

class UpdateOrderStatus(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        id = graphene.UUID(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, id, status):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise GraphQLError('Order not found')

        order.status = status
        order.save()
        return UpdateOrderStatus(order=order)

class OrderMutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order_status = UpdateOrderStatus.Field()
