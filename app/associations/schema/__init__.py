import graphene
from associations.schema.artisan_schema import ArtisanQuery, ArtisanMutation
from associations.schema.association_schema import AssociationQuery, AssociationMutation

class Query(ArtisanQuery, AssociationQuery, graphene.ObjectType):
    pass

class Mutation(ArtisanMutation, AssociationMutation, graphene.ObjectType):
    pass
