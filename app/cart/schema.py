import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from cart.models import Cart, CartItem
from products.models import Product
from users.models import User
from graphql import GraphQLError
from common.pagination import PaginationInput, PageInfo, paginate_queryset


# -------------------- GraphQL Types --------------------
class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "user", "created_at", "updated_at", "items")

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity", "price_at_add", "added_at")


# -------------------- Paginated Cart Type --------------------
class PaginatedCartItems(graphene.ObjectType):
    cart_items = graphene.List(CartItemType)
    page_info = graphene.Field(PageInfo)

# -------------------- Queries --------------------
class CartQuery(graphene.ObjectType):
    my_cart = graphene.Field(CartType)
    my_cart_items = graphene.Field(PaginatedCartItems, pagination=PaginationInput())

    @login_required
    def resolve_my_cart(self, info):
        user = info.context.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    @login_required
    def resolve_my_cart_items(self, info, pagination=None):
        if pagination is None:
            pagination = PaginationInput()
        user = info.context.user
        cart, created = Cart.objects.get_or_create(user=user)
        queryset = CartItem.objects.filter(cart=cart)
        cart_items, page_info = paginate_queryset(queryset, pagination)
        return PaginatedCartItems(cart_items=cart_items, page_info=page_info)


# -------------------- Mutations --------------------
class AddToCart(graphene.Mutation):
    cart_item = graphene.Field(CartItemType)

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

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity, 'price_at_add': product.price}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return AddToCart(cart_item=cart_item)


class UpdateCartItem(graphene.Mutation):
    cart_item = graphene.Field(CartItemType)

    class Arguments:
        cart_item_id = graphene.UUID(required=True)
        quantity = graphene.Int(required=True)

    @login_required
    def mutate(self, info, cart_item_id, quantity):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=info.context.user)
        except CartItem.DoesNotExist:
            raise GraphQLError("Cart item not found")

        cart_item.quantity = quantity
        cart_item.save()
        return UpdateCartItem(cart_item=cart_item)


class DeleteCartItem(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        cart_item_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=info.context.user)
            cart_item.delete()
            return DeleteCartItem(success=True)
        except CartItem.DoesNotExist:
            raise GraphQLError("Cart item not found")


# -------------------- Mutation Class --------------------
class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
