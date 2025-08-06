# type: ignore
import graphene
from graphene_django import DjangoObjectType
from associations.models import Artisan, Association
from users.models import User
from graphql import GraphQLError

# ---------------- Artisan GraphQL Type ----------------
class ArtisanType(DjangoObjectType):
    class Meta:
        model = Artisan
        fields = ("user", "association", "bio")

# ---------------- Queries ----------------
class ArtisanQuery(graphene.ObjectType):
    all_artisans = graphene.List(ArtisanType)
    artisan = graphene.Field(ArtisanType, user_id=graphene.UUID(required=True))

    def resolve_all_artisans(self, info):
        return Artisan.objects.select_related('user', 'association').all()

    def resolve_artisan(self, info, user_id):
        try:
            return Artisan.objects.select_related('user', 'association').get(user_id=user_id)
        except Artisan.DoesNotExist:
            raise GraphQLError('Artisan not found')

# ---------------- Mutations ----------------
class CreateArtisan(graphene.Mutation):
    artisan = graphene.Field(ArtisanType)

    class Arguments:
        user_id = graphene.UUID(required=True)
        association_id = graphene.UUID(required=False)
        bio = graphene.String()

    def mutate(self, info, user_id, association_id=None, bio=""):
        try:
            user = User.objects.get(id=user_id, role='artisan')
        except User.DoesNotExist:
            raise GraphQLError('User not found or is not an artisan')

        association = None
        if association_id:
            try:
                association = Association.objects.get(id=association_id)
            except Association.DoesNotExist:
                raise GraphQLError('Association not found')

        artisan = Artisan(user=user, association=association, bio=bio)
        artisan.save()
        return CreateArtisan(artisan=artisan)

class UpdateArtisan(graphene.Mutation):
    artisan = graphene.Field(ArtisanType)

    class Arguments:
        user_id = graphene.UUID(required=True)
        association_id = graphene.UUID()
        bio = graphene.String()

    def mutate(self, info, user_id, association_id=None, bio=None):
        try:
            artisan = Artisan.objects.get(user_id=user_id)
        except Artisan.DoesNotExist:
            raise GraphQLError('Artisan not found')

        if association_id:
            try:
                association = Association.objects.get(id=association_id)
                artisan.association = association
            except Association.DoesNotExist:
                raise GraphQLError('Association not found')

        if bio is not None:
            artisan.bio = bio

        artisan.save()
        return UpdateArtisan(artisan=artisan)

class DeleteArtisan(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        user_id = graphene.UUID(required=True)

    def mutate(self, info, user_id):
        try:
            artisan = Artisan.objects.get(user_id=user_id)
            artisan.delete()
            return DeleteArtisan(success=True)
        except Artisan.DoesNotExist:
            raise GraphQLError('Artisan not found')

# ---------------- Mutation Class ----------------
class ArtisanMutation(graphene.ObjectType):
    create_artisan = CreateArtisan.Field()
    update_artisan = UpdateArtisan.Field()
    delete_artisan = DeleteArtisan.Field()
