import graphene
from graphene_django import DjangoObjectType
from products.models import Review, Product
from users.models import User
from graphql import GraphQLError

# -------- Type --------
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("id", "buyer", "product", "rating", "comment", "created_at")

# -------- Queries --------
class ReviewsQuery(graphene.ObjectType):
    all_reviews = graphene.List(ReviewType, product_id=graphene.UUID(required=True))

    def resolve_all_reviews(self, info, product_id):
        return Review.objects.filter(product_id=product_id).select_related('buyer')

# -------- Mutations --------
class AddReview(graphene.Mutation):
    review = graphene.Field(ReviewType)

    class Arguments:
        buyer_id = graphene.UUID(required=True)
        product_id = graphene.UUID(required=True)
        rating = graphene.Int(required=True)
        comment = graphene.String()

    def mutate(self, info, buyer_id, product_id, rating, comment=None):
        try:
            buyer = User.objects.get(id=buyer_id, role='buyer')
            product = Product.objects.get(id=product_id)
        except (User.DoesNotExist, Product.DoesNotExist):
            raise GraphQLError('Buyer or Product not found')

        review = Review.objects.create(buyer=buyer, product=product, rating=rating, comment=comment)
        return AddReview(review=review)

class DeleteReview(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        review_id = graphene.UUID(required=True)

    def mutate(self, info, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return DeleteReview(success=True)
        except Review.DoesNotExist:
            raise GraphQLError('Review not found')

class ReviewsMutation:
    add_review = AddReview.Field()
    delete_review = DeleteReview.Field()
