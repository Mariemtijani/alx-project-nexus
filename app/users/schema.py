
# type: ignore
import graphene
from graphene_django import DjangoObjectType
from users.models import User
from graphql import GraphQLError

# -------------------- GraphQL Type --------------------
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "role", "profile_picture", "created_at", "updated_at")

# -------------------- Query --------------------
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.UUID(required=True))

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')

# -------------------- Mutations --------------------
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String()
        role = graphene.String(required=True)
        profile_picture = graphene.String()

    def mutate(self, info, name, email, password, role, phone=None, profile_picture=None):
        user = User(
            name=name,
            email=email,
            password=password,  # In production, hash this!
            role=role,
            phone=phone,
            profile_picture=profile_picture
        )
        user.save()
        return CreateUser(user=user)
# Existing imports...
from graphql import GraphQLError

# -------------------- UpdateUser Mutation --------------------
class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()
        phone = graphene.String()
        role = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, id, name=None, email=None, password=None, phone=None, role=None, profile_picture=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError("User not found")

        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = password  # Hash later!
        if phone:
            user.phone = phone
        if role:
            user.role = role
        if profile_picture:
            user.profile_picture = profile_picture

        user.save()
        return UpdateUser(user=user)

# -------------------- DeleteUser Mutation --------------------
class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError("User not found")

        user.delete()
        return DeleteUser(success=True)

# -------------------- Extend Mutation Class --------------------
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
