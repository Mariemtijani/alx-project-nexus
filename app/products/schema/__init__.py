import graphene
from products.schema.product_schema import ProductQuery, ProductMutation
from products.schema.favorites_schema import FavoritesQuery, FavoritesMutation
from products.schema.reviews_schema import ReviewsQuery, ReviewsMutation

class Query(ProductQuery, FavoritesQuery, ReviewsQuery, graphene.ObjectType):
    pass

class Mutation(ProductMutation, FavoritesMutation, ReviewsMutation, graphene.ObjectType):
    pass
