import graphene
from orders.schema.order_schema import OrderQuery, OrderMutation
from orders.schema.payment_schema import PaymentMutation

class Query(OrderQuery, graphene.ObjectType):
    pass

class Mutation(OrderMutation, PaymentMutation, graphene.ObjectType):
    pass
