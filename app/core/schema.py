# type: ignore
import graphene
import users.schema as users_schema
import associations.schema as associations_schema
import products.schema as products_schema
import orders.schema as orders_schema

class Query(users_schema.Query,
            associations_schema.Query,
            products_schema.Query,
            orders_schema.Query, 
            graphene.ObjectType):
    pass

class Mutation(users_schema.Mutation,
               associations_schema.Mutation,
               products_schema.Mutation,
               orders_schema.Mutation, 
               graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
