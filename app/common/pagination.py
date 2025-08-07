import graphene
from django.core.paginator import Paginator

class PaginationInput(graphene.InputObjectType):
    page = graphene.Int(default_value=1)
    page_size = graphene.Int(default_value=10)

class PageInfo(graphene.ObjectType):
    has_next_page = graphene.Boolean()
    has_previous_page = graphene.Boolean()
    current_page = graphene.Int()
    total_pages = graphene.Int()
    total_count = graphene.Int()

def paginate_queryset(queryset, pagination_input):
    paginator = Paginator(queryset, pagination_input.page_size)
    page = paginator.get_page(pagination_input.page)
    
    page_info = PageInfo(
        has_next_page=page.has_next(),
        has_previous_page=page.has_previous(),
        current_page=page.number,
        total_pages=paginator.num_pages,
        total_count=paginator.count
    )
    
    return page.object_list, page_info