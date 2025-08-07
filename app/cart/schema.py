# cart/schema/cart_schema.py
# type: ignore
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from cart.models import Cart
from products.models import Product
from users.models import User
from graphql import GraphQLError


# -------------------- GraphQL Type --------------------
class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "user", "product", "quantity", "created_at", "updated_at")


# -------------------- Queries --------------------
class CartQuery(graphene.ObjectType):
    my_cart = graphene.List(CartType)

    @login_required
    def resolve_my_cart(self, info):
        user = info.context.user
        return Cart.objects.filter(user=user)


# -------------------- Mutations --------------------
class AddToCart(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        product_id = graphene.UUID(required=True)
        quantity = graphene.Int(required=True)

    @login_required
    def mutate(self, info, product_id, quantity):
        user = info.context.user
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise GraphQLError("Product not found")

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return AddToCart(cart=cart_item)


class UpdateCartItem(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        cart_id = graphene.UUID(required=True)
        quantity = graphene.Int(required=True)

    @login_required
    def mutate(self, info, cart_id, quantity):
        try:
            cart_item = Cart.objects.get(id=cart_id, user=info.context.user)
        except Cart.DoesNotExist:
            raise GraphQLError("Cart item not found")

        cart_item.quantity = quantity
        cart_item.save()
        return UpdateCartItem(cart=cart_item)


class DeleteCartItem(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        cart_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, cart_id):
        try:
            cart_item = Cart.objects.get(id=cart_id, user=info.context.user)
            cart_item.delete()
            return DeleteCartItem(success=True)
        except Cart.DoesNotExist:
            raise GraphQLError("Cart item not found")


# -------------------- Mutation Class --------------------
class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
