import graphene
from graphene_django import DjangoObjectType
from products.models import Product, Category, ProductTranslation, ProductImage
from associations.models import Artisan, Association
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from common.pagination import PaginationInput, PageInfo, paginate_queryset
from django.db.models import Q, QuerySet
from typing import Optional


# ---------------- GraphQL Types ----------------
class CategoryType(DjangoObjectType):
    """GraphQL type for product categories."""
    class Meta:
        model = Category
        fields = ("id", "name")

class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ("id", "image_url")

class ProductTranslationType(DjangoObjectType):
    class Meta:
        model = ProductTranslation
        fields = ("id", "language_code", "title", "description")

class ProductType(DjangoObjectType):
    """GraphQL type for products with dynamic owner resolution."""
    owner = graphene.String()  # Dynamic Field (Artisan or Association)

    class Meta:
        model = Product
        fields = ("id", "title", "description", "price", "stock_quantity", "owner_type", "category", "status", "translations", "images")

    def resolve_owner(self, info):
        """Resolve product owner name based on owner_type.
        
        Returns artisan name or association name depending on owner_type.
        """
        if self.owner_type == 'artisan':
            try:
                artisan = Artisan.objects.select_related('user').get(user_id=self.owner_id)
                return artisan.user.name
            except Artisan.DoesNotExist:
                return None
        elif self.owner_type == 'association':
            try:
                association = Association.objects.get(id=self.owner_id)
                return association.name
            except Association.DoesNotExist:
                return None
        return None

# ---------------- Paginated Products Type ----------------
class PaginatedProducts(graphene.ObjectType):
    products = graphene.List(ProductType)
    page_info = graphene.Field(PageInfo)

# ---------------- Queries ----------------
class ProductQuery(graphene.ObjectType):
    all_products = graphene.Field(
        PaginatedProducts, 
        pagination=PaginationInput(),
        category_id=graphene.UUID(),
        sort_by=graphene.String()
    )
    product = graphene.Field(ProductType, id=graphene.UUID(required=True))

    def resolve_all_products(self, info, pagination: Optional[PaginationInput] = None, 
                           category_id: Optional[str] = None, sort_by: Optional[str] = None) -> PaginatedProducts:
        """Fetch products with filtering and sorting options.
        
        Args:
            pagination: Pagination parameters
            category_id: Filter by category UUID
            sort_by: Sort options (price_asc, price_desc, newest, oldest)
        """
        if pagination is None:
            pagination = PaginationInput()
        
        # Build optimized base queryset
        base_queryset = self._get_optimized_product_queryset()
        
        # Apply filters
        filtered_queryset = self._apply_category_filter(base_queryset, category_id)
        
        # Apply sorting
        sorted_queryset = self._apply_product_sorting(filtered_queryset, sort_by)
        
        # Paginate results
        paginated_products, page_info = paginate_queryset(sorted_queryset, pagination)
        return PaginatedProducts(products=paginated_products, page_info=page_info)
    
    def _get_optimized_product_queryset(self) -> QuerySet:
        """Get optimized product queryset with related data."""
        return Product.objects.select_related('category').prefetch_related('translations', 'images').all()
    
    def _apply_category_filter(self, queryset: QuerySet, category_id: Optional[str]) -> QuerySet:
        """Apply category filter if provided."""
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset
    
    def _apply_product_sorting(self, queryset: QuerySet, sort_by: Optional[str]) -> QuerySet:
        """Apply sorting to product queryset."""
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'newest': '-created_at',
            'oldest': 'created_at'
        }
        
        if sort_by and sort_by in sort_options:
            return queryset.order_by(sort_options[sort_by])
        return queryset

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')

# ---------------- Mutations ----------------
class CreateProduct(graphene.Mutation):
    """Mutation to create a new product."""
    product = graphene.Field(ProductType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock_quantity = graphene.Int(required=True)
        owner_type = graphene.String(required=True)
        owner_id = graphene.UUID(required=True)
        category_id = graphene.UUID(required=False)

    @login_required
    def mutate(self, info, title: str, description: str, price: float, stock_quantity: int, 
              owner_type: str, owner_id: str, category_id: Optional[str] = None) -> 'CreateProduct':
        """Create new product with validation.
        
        Validates owner exists and category is valid before creation.
        """
        # Validate input parameters
        self._validate_owner_type(owner_type)
        self._validate_owner_exists(owner_type, owner_id)
        validated_category = self._validate_and_get_category(category_id)

        # Create new product
        new_product = Product(
            title=title,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            owner_type=owner_type,
            owner_id=owner_id,
            category=validated_category
        )
        new_product.save()
        return CreateProduct(product=new_product)
    
    def _validate_owner_type(self, owner_type: str) -> None:
        """Validate owner type is either artisan or association."""
        valid_owner_types = ['artisan', 'association']
        if owner_type not in valid_owner_types:
            raise GraphQLError('Invalid owner type')
    
    def _validate_owner_exists(self, owner_type: str, owner_id: str) -> None:
        """Validate that the specified owner exists."""
        if owner_type == 'artisan' and not Artisan.objects.filter(user_id=owner_id).exists():
            raise GraphQLError('Artisan owner not found')
        if owner_type == 'association' and not Association.objects.filter(id=owner_id).exists():
            raise GraphQLError('Association owner not found')
    
    def _validate_and_get_category(self, category_id: Optional[str]) -> Optional['Category']:
        """Validate and return category if provided."""
        if not category_id:
            return None
        
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise GraphQLError('Category not found')

class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.UUID(required=True)
        title = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        stock_quantity = graphene.Int()
        category_id = graphene.UUID()
        status = graphene.String()

    @login_required
    def mutate(self, info, id, title=None, description=None, price=None, stock_quantity=None, category_id=None, status=None):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')

        if title: product.title = title
        if description: product.description = description
        if price: product.price = price
        if stock_quantity: product.stock_quantity = stock_quantity
        if status: product.status = status

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                product.category = category
            except Category.DoesNotExist:
                raise GraphQLError('Category not found')

        product.save()
        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    @login_required
    def mutate(self, info, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return DeleteProduct(success=True)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')

# ---------------- Mutation Class ----------------
class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
