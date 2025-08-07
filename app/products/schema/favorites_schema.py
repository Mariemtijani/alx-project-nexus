import graphene
from graphene_django import DjangoObjectType
from products.favorite_model import Favorite
from products.models import Product
from products.review_model import Review
from users.models import User
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


# -------- Type --------
class FavoriteType(DjangoObjectType):
    class Meta:
        model = Favorite
        fields = ("id", "buyer", "product")

# -------- Queries --------
class FavoritesQuery(graphene.ObjectType):
    all_favorites = graphene.List(FavoriteType, buyer_id=graphene.UUID(required=True))

    def resolve_all_favorites(self, info, buyer_id):
        try:
            buyer = User.objects.get(id=buyer_id, role='buyer')
        except User.DoesNotExist:
            raise GraphQLError('Buyer not found')

        return Favorite.objects.filter(buyer=buyer).select_related('product')

# -------- Mutations --------
class AddFavorite(graphene.Mutation):
    favorite = graphene.Field(FavoriteType)

    class Arguments:
        buyer_id = graphene.UUID(required=True)
        product_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, buyer_id, product_id):
        try:
            buyer = User.objects.get(id=buyer_id, role='buyer')
            product = Product.objects.get(id=product_id)
        except (User.DoesNotExist, Product.DoesNotExist):
            raise GraphQLError('Buyer or Product not found')

        favorite, created = Favorite.objects.get_or_create(buyer=buyer, product=product)
        return AddFavorite(favorite=favorite)

class RemoveFavorite(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        buyer_id = graphene.UUID(required=True)
        product_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, buyer_id, product_id):
        try:
            favorite = Favorite.objects.get(buyer_id=buyer_id, product_id=product_id)
            favorite.delete()
            return RemoveFavorite(success=True)
        except Favorite.DoesNotExist:
            raise GraphQLError('Favorite not found')

class FavoritesMutation:
    add_favorite = AddFavorite.Field()
    remove_favorite = RemoveFavorite.Field()
