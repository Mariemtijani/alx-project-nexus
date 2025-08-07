import graphene
from products.schema.product_schema import ProductQuery, ProductMutation
from products.schema.favorites_schema import FavoritesQuery, FavoritesMutation
from products.schema.reviews_schema import ReviewsQuery, ReviewsMutation
from products.schema.category_schema import CategoryQuery, CategoryMutation

class Query(ProductQuery, FavoritesQuery, ReviewsQuery, CategoryQuery, graphene.ObjectType):
    pass

class Mutation(ProductMutation, FavoritesMutation, ReviewsMutation, CategoryMutation, graphene.ObjectType):
    pass
