
import graphene
import graphql_jwt
import users.schema as users_schema
import associations.schema as associations_schema
import products.schema as products_schema
import orders.schema as orders_schema
from cart.schema import CartQuery, CartMutation

class Query(users_schema.Query,
            associations_schema.Query,
            products_schema.Query,
            orders_schema.Query,
            CartQuery, 
            graphene.ObjectType):
    """Root GraphQL query combining all app queries."""
    pass

class Mutation(users_schema.Mutation,
               associations_schema.Mutation,
               products_schema.Mutation,
               orders_schema.Mutation, 
               CartMutation,
               graphene.ObjectType):
    """Root GraphQL mutation combining all app mutations and JWT auth."""
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()  # JWT login
    refresh_token = graphql_jwt.Refresh.Field()  # Token refresh
    verify_token = graphql_jwt.Verify.Field()  # Token verification

schema = graphene.Schema(query=Query, mutation=Mutation)
