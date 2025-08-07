import graphene
from graphene_django import DjangoObjectType
from users.models import User
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from users.utils import hash_password, verify_password
from common.pagination import PaginationInput, PageInfo, paginate_queryset
from typing import Optional


# -------------------- GraphQL Type --------------------
class UserType(DjangoObjectType):
    """GraphQL type for User model."""
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "role", "profile_picture", "created_at", "updated_at")

# -------------------- Paginated Users Type --------------------
class PaginatedUsers(graphene.ObjectType):
    """Paginated response for user queries."""
    users = graphene.List(UserType)
    page_info = graphene.Field(PageInfo)

# -------------------- Queries --------------------
class Query(graphene.ObjectType):
    all_users = graphene.Field(PaginatedUsers, pagination=PaginationInput())
    user = graphene.Field(UserType, id=graphene.UUID(required=True))

    @login_required
    def resolve_all_users(self, info, pagination: Optional[PaginationInput] = None) -> PaginatedUsers:
        """Fetch all users with pagination."""
        if pagination is None:
            pagination = PaginationInput()
        paginated_users, page_info = paginate_queryset(User.objects.all(), pagination)
        return PaginatedUsers(users=paginated_users, page_info=page_info)

    @login_required
    def resolve_user(self, info, id: str) -> User:
        """Fetch single user by ID."""
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')

# -------------------- RegisterUser Mutation --------------------
class RegisterUser(graphene.Mutation):
    """Mutation to register a new user."""
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        phone = graphene.String()
        role = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, name: str, email: str, password: str, role: str = "buyer", 
              phone: Optional[str] = None, profile_picture: Optional[str] = None) -> 'RegisterUser':
        """Create new user account with hashed password."""
        # Check for existing email
        if User.objects.filter(email=email).exists():
            raise GraphQLError("Email already registered")

        # Create new user with hashed password
        new_user = User(
            name=name,
            email=email,
            password=hash_password(password),  # Hash password for security
            role=role,
            phone=phone,
            profile_picture=profile_picture
        )
        new_user.save()

        return RegisterUser(user=new_user)

# -------------------- LoginUser Mutation --------------------
class LoginUser(graphene.Mutation):
    """Mutation to authenticate user and return JWT token."""
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email: str, password: str) -> 'LoginUser':
        """Authenticate user and generate JWT token."""
        try:
            authenticated_user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError('Invalid email or password')

        # Verify password using bcrypt
        if not verify_password(password, authenticated_user.password):
            raise GraphQLError('Invalid email or password')

        # Generate JWT token
        auth_token = get_token(authenticated_user)
        return LoginUser(user=authenticated_user, token=auth_token)

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
