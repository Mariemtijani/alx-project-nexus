import graphene
from graphene_django import DjangoObjectType
from products.models import Category
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from typing import Optional


# ---------------- GraphQL Types ----------------
class CategoryType(DjangoObjectType):
    """GraphQL type for product categories."""
    class Meta:
        model = Category
        fields = ("id", "name")


# ---------------- Queries ----------------
class CategoryQuery(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.UUID(required=True))
    
    def resolve_all_categories(self, info):
        """Fetch all product categories."""
        return Category.objects.all()
    
    def resolve_category(self, info, id: str):
        """Fetch single category by ID."""
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise GraphQLError('Category not found')


# ---------------- Mutations ----------------
class CreateCategory(graphene.Mutation):
    """Mutation to create a new category."""
    category = graphene.Field(CategoryType)
    
    class Arguments:
        name = graphene.String(required=True)
    
    @login_required
    def mutate(self, info, name: str) -> 'CreateCategory':
        """Create new category."""
        new_category = Category(name=name)
        new_category.save()
        return CreateCategory(category=new_category)


class UpdateCategory(graphene.Mutation):
    """Mutation to update a category."""
    category = graphene.Field(CategoryType)
    
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String()
    
    @login_required
    def mutate(self, info, id: str, name: Optional[str] = None) -> 'UpdateCategory':
        """Update category name."""
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise GraphQLError('Category not found')
        
        if name:
            category.name = name
        
        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    """Mutation to delete a category."""
    success = graphene.Boolean()
    
    class Arguments:
        id = graphene.UUID(required=True)
    
    @login_required
    def mutate(self, info, id: str) -> 'DeleteCategory':
        """Delete category."""
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return DeleteCategory(success=True)
        except Category.DoesNotExist:
            raise GraphQLError('Category not found')


# ---------------- Schema Classes ----------------
class CategoryMutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()