import graphene
from graphene_django import DjangoObjectType
from users.models import User
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from users.utils import hash_password, verify_password
from common.pagination import PaginationInput, PageInfo, paginate_queryset


# -------------------- GraphQL Type --------------------
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "role", "profile_picture", "created_at", "updated_at")

# -------------------- Paginated Users Type --------------------
class PaginatedUsers(graphene.ObjectType):
    users = graphene.List(UserType)
    page_info = graphene.Field(PageInfo)

# -------------------- Queries --------------------
class Query(graphene.ObjectType):
    all_users = graphene.Field(PaginatedUsers, pagination=PaginationInput())
    user = graphene.Field(UserType, id=graphene.UUID(required=True))

    @login_required
    def resolve_all_users(self, info, pagination=None):
        if pagination is None:
            pagination = PaginationInput()
        users, page_info = paginate_queryset(User.objects.all(), pagination)
        return PaginatedUsers(users=users, page_info=page_info)

    @login_required
    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')

# -------------------- RegisterUser Mutation --------------------
class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String()
        role = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, name, email, password, role="buyer", phone=None, profile_picture=None):
        if User.objects.filter(email=email).exists():
            raise GraphQLError("Email already registered")

        user = User(
            name=name,
            email=email,
            password=hash_password(password),
            role=role,
            phone=phone,
            profile_picture=profile_picture
        )
        user.save()

        return RegisterUser(user=user)

# -------------------- LoginUser Mutation --------------------
class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError('Invalid email or password')

        if not verify_password(password, user.password):
            raise GraphQLError('Invalid email or password')

        token = get_token(user)
        return LoginUser(user=user, token=token)

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

    @login_required
    def mutate(self, info, id, name=None, email=None, password=None, phone=None, role=None, profile_picture=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError("User not found")

        if name: user.name = name
        if email: user.email = email
        if password: user.password = hash_password(password)
        if phone: user.phone = phone
        if role: user.role = role
        if profile_picture: user.profile_picture = profile_picture

        user.save()
        return UpdateUser(user=user)

# -------------------- DeleteUser Mutation --------------------
class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            user = User.objects.get(id=id)
            
            user.delete()
            return DeleteUser(success=True)
        except User.DoesNotExist:
            raise GraphQLError("User not found")
# -------------------- Mutation Class --------------------
class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
