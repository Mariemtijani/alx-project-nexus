import graphene
from django.core.paginator import Paginator
from django.db.models import QuerySet
from typing import Tuple, Any

class PaginationInput(graphene.InputObjectType):
    """GraphQL input type for pagination parameters."""
    page = graphene.Int()
    page_size = graphene.Int()

class PageInfo(graphene.ObjectType):
    """GraphQL type for pagination metadata."""
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    current_page = graphene.Int()
    total_pages = graphene.Int()
    total_count = graphene.Int()

def paginate_queryset(queryset: QuerySet, pagination_input: PaginationInput) -> Tuple[Any, PageInfo]:
    """Paginate Django queryset and return results with page info.
    
    Args:
        queryset: Django QuerySet to paginate
        pagination_input: PaginationInput with page and page_size
        
    Returns:
        Tuple of (paginated_objects, page_info)
    """
    page = pagination_input.page or 1
    page_size = pagination_input.page_size or 10
    
    paginator = Paginator(queryset, page_size)
    current_page = paginator.get_page(page)
    
    page_info = PageInfo(
        has_next_page=current_page.has_next(),
        has_previous_page=current_page.has_previous(),
        current_page=current_page.number,
        total_pages=paginator.num_pages,
        total_count=paginator.count
    )
    
    return current_page.object_list, page_info