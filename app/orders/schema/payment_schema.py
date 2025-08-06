import graphene
from graphene_django import DjangoObjectType
from orders.models import Payment, Order
from graphql import GraphQLError

# -------- Types --------
class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ("id", "order", "payment_method", "status", "payment_date", "transaction_reference")

# -------- Mutations --------
class CreatePayment(graphene.Mutation):
    payment = graphene.Field(PaymentType)

    class Arguments:
        order_id = graphene.UUID(required=True)
        payment_method = graphene.String(required=True)
        status = graphene.String(required=True)
        payment_date = graphene.DateTime(required=True)
        transaction_reference = graphene.String(required=True)

    def mutate(self, info, order_id, payment_method, status, payment_date, transaction_reference):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise GraphQLError('Order not found')

        payment = Payment(
            order=order,
            payment_method=payment_method,
            status=status,
            payment_date=payment_date,
            transaction_reference=transaction_reference
        )
        payment.save()
        return CreatePayment(payment=payment)

class PaymentMutation(graphene.ObjectType):
    create_payment = CreatePayment.Field()
