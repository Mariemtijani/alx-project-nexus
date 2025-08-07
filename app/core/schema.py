
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
    pass

class Mutation(users_schema.Mutation,
               associations_schema.Mutation,
               products_schema.Mutation,
               orders_schema.Mutation, 
               CartMutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
