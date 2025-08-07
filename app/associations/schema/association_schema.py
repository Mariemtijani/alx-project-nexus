
# type: ignore
import graphene
from graphene_django import DjangoObjectType
from associations.models import Association
from users.models import User
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from common.pagination import PaginationInput, PageInfo, paginate_queryset

# ---------------- Association GraphQL Type ----------------
class AssociationType(DjangoObjectType):
    class Meta:
        model = Association
        fields = ("id", "name", "description", "logo_url", "email", "phone", "admin")

# ---------------- Paginated Associations Type ----------------
class PaginatedAssociations(graphene.ObjectType):
    associations = graphene.List(AssociationType)
    page_info = graphene.Field(PageInfo)

# ---------------- Queries ----------------
class AssociationQuery(graphene.ObjectType):
    all_associations = graphene.Field(PaginatedAssociations, pagination=PaginationInput())
    association = graphene.Field(AssociationType, id=graphene.UUID(required=True))

    def resolve_all_associations(self, info, pagination=None):
        if pagination is None:
            pagination = PaginationInput()
        queryset = Association.objects.select_related('admin').all()
        associations, page_info = paginate_queryset(queryset, pagination)
        return PaginatedAssociations(associations=associations, page_info=page_info)

    def resolve_association(self, info, id):
        try:
            return Association.objects.select_related('admin').get(id=id)
        except Association.DoesNotExist:
            raise GraphQLError('Association not found')

# ---------------- Mutations ----------------
class CreateAssociation(graphene.Mutation):
    association = graphene.Field(AssociationType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        logo_url = graphene.String()
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        admin_id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, name, email, phone, admin_id, description="", logo_url=None):
        try:
            admin = User.objects.get(id=admin_id, role='association_admin')
        except User.DoesNotExist:
            raise GraphQLError('Admin user not found or role invalid')

        association = Association(
            name=name,
            description=description,
            logo_url=logo_url,
            email=email,
            phone=phone,
            admin=admin
        )
        association.save()
        return CreateAssociation(association=association)

class UpdateAssociation(graphene.Mutation):
    association = graphene.Field(AssociationType)

    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
        description = graphene.String()
        logo_url = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    @login_required
    def mutate(self, info, id, name=None, description=None, logo_url=None, email=None, phone=None):
        try:
            association = Association.objects.get(id=id)
        except Association.DoesNotExist:
            raise GraphQLError('Association not found')

        if name: association.name = name
        if description: association.description = description
        if logo_url: association.logo_url = logo_url
        if email: association.email = email
        if phone: association.phone = phone

        association.save()
        return UpdateAssociation(association=association)

class DeleteAssociation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            association = Association.objects.get(id=id)
            association.delete()
            return DeleteAssociation(success=True)
        except Association.DoesNotExist:
            raise GraphQLError('Association not found')

# ---------------- Mutation Class ----------------
class AssociationMutation(graphene.ObjectType):
    create_association = CreateAssociation.Field()
    update_association = UpdateAssociation.Field()
    delete_association = DeleteAssociation.Field()
