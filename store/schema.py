import graphene
from django.contrib.auth.models import User
from store.types import BookType, UserType
from store.models import (BookModel, CategoryModel, PublisherModel, AuthorModel)
from django.db.models import Q


class Query(graphene.ObjectType):
    books_by = graphene.List(
        BookType,
        age_group=graphene.String(),
        category=graphene.String(),
        publisher=graphene.String(),
    )
    books_between_price_range = graphene.List(BookType, price_from=graphene.Float(), price_to=graphene.Float())
    books_ordered_by_name = graphene.List(BookType, order=graphene.String(required=True))
    books_ordered_by_author = graphene.List(BookType, order=graphene.String(required=True))
    books_by_name = graphene.List(
        BookType,
        name=graphene.String(required=True),
        lookup_method=graphene.String(required=True),
    )
    books_by_author = graphene.List(
        BookType,
        author_name=graphene.String(required=True),
        lookup_method=graphene.String(required=True)
    )
    books_between_page_number_range = graphene.List(
        BookType,
        page_from=graphene.Float(),
        page_to=graphene.Float(),
    )
    books_by_user = graphene.List(BookType, username=graphene.String(required=True))
    staff_users = graphene.List(UserType)
    '''advance_search = graphene.List(
        BookType,
        exact_name=graphene.String(),
        exact_author=graphene.String(),
        name=graphene.String(),
        author=graphene.String(),
        price_from=graphene.Float(),
        price_to=graphene.Float(),
        page_from=graphene.Float(),
        page_to=graphene.Float(),
        book_owner=graphene.String(),
        publisher=graphene.String(),
        category=graphene.String(),
        age_group=graphene.String(),
    )
    '''

    def check_fields(list_of_objects: list, model_obj: object) -> list:
        mylist = []
        for _ in list_of_objects:
            if model_obj.objects.filter(name=_).exists():
                mylist.append(_)
        return mylist

    def check_if_any_object_exists(queryset: object) -> object:
        if queryset.exists():
            return queryset
        else:
            return None
    '''
    def resolve_advance_search(
            root, info, exact_name=None, exact_author=None,
            name=None, author=None, price_from=None, price_to=None,
            page_from=None, page_to=None, book_owner=None,
            publisher=None, category=None, age_group=None,
    ):
        try:
            if not all([price_to, price_from]):
                return None
            elif not all([page_from, page_to]):
                return None

            name = name if name else ''
            price_to, price_from = (price_to, price_from) if price_to and price_from else ('', '')

            category_set = []
            if category is not None:
                for c in category:
                    if CategoryModel.objects.filter(name=c).exists():
                        category_obj = CategoryModel.objects.get(name=c)
                        category_set.append(category_obj.name)

            author_set = []
            if author is not None:
                for a in author:
                    if AuthorModel.objects.filter(name=a).exists():
                        author_obj = AuthorModel.objects.get(name=a)
                        author_set.append(author_obj.name)

            user_obj = ''
            if User.objects.filter(username=book_owner, is_staff=True).exists():
                user_obj = User.objects.get(username=book_owner)
            query = BookModel.objects.filter(
                Q(name__icontains=name), Q(author__name__in=author),
                Q(page_number__gte=page_from, page_number__lte=page_to),
                Q(price__gte=price_from, price__let=price_to),
                Q(owner=user_obj), Q(publisher__name=publisher),
                Q(category__name__in=category_set), Q(age_group=age_group)
            ).distinct()

            if exact_name and exact_author:
                queryset_res = query.filter(
                    Q(name__exact=exact_name), Q(author__name__exact=exact_author)
                )
                return Query.check_if_any_object_exists(queryset_res)

            elif exact_name is not None:
                queryset_res = query.filter(name__exact=exact_name).distinct()
                return Query.check_if_any_object_exists(queryset_res)

            elif exact_author is not None:
                queryset_res = query.filter(author__name__exact=exact_author).distinct()
                return Query.check_if_any_object_exists(queryset_res)

            else:
                return query

        except (BookModel.DoesNotExist, Exception):
            return None
    '''
    def resolve_staff_users(root, info):
        return User.objects.filter(is_staff=True)

    def resolve_books_by_user(root, info, username):
        try:
            if User.objects.filter(username=username, is_staff=True).exists():
                return BookModel.objects.filter(owner__username=username)
            else:
                return None
        except (BookModel.DoesNotExist, User.DoesNotExist):
            return None

    def resolve_books_between_page_number_range(root, info, page_from, page_to):
        try:
            my_query = BookModel.objects.filter(page_number__gte=page_from, page_number__lte=page_to)
            my_query = my_query if my_query.exists() else None
            return my_query
        except BookModel.DoesNotExist:
            return None

    def resolve_books_by_author(root, info, author_name, lookup_method):
        try:
            if lookup_method == 'exact':
                return BookModel.objects.filter(author__name__exact=author_name).distinct()
            elif lookup_method == 'icontains':
                return BookModel.objects.filter(author__name__icontains=author_name).distinct()
            else:
                return None
        except BookModel.DoesNotExist:
            return None

    def resolve_books_by_name(root, info, name, lookup_method):
        try:
            if lookup_method == 'exact':
                return BookModel.objects.filter(name__exact=name).distinct()
            elif lookup_method == 'icontains':
                return BookModel.objects.filter(name__icontains=name).distinct()
            else:
                return None
        except BookModel.DoesNotExist:
            return None

    def resolve_books_ordered_by_author(root, info, order):
        if order == 'a-z':
            return list(set(BookModel.objects.all().order_by('author__name')))
        elif order == 'z-a':
            return list(set(BookModel.objects.all().order_by('-author__name')))
        else:
            return None

    def resolve_books_ordered_by_name(root, info, order):
        if order == 'a-z':
            return BookModel.objects.all().order_by('name')
        elif order == 'z-a':
            return BookModel.objects.all().order_by('-name')
        else:
            return None

    def resolve_books_between_price_range(root, info, price_from, price_to):
        try:
            return BookModel.objects.filter(price__gte=price_from).filter(price__lte=price_to).distinct()
        except BookModel.DoesNotExist:
            return None

    def resolve_books_by(root, info, age_group=None, category=None, publisher=None):
        try:
            if age_group:
                return BookModel.objects.filter(age_group=age_group).distinct()

            elif category and publisher:
                category_list = Query.check_fields(category.split(','), CategoryModel)
                publisher_list = Query.check_fields(publisher.split(','), PublisherModel)

                return BookModel.objects.filter(
                    category__name__in=category_list,
                    publisher__name__in=publisher_list
                ).distinct()

            elif category:
                category_list = Query.check_fields(category.split(','), CategoryModel)
                return BookModel.objects.filter(category__name__in=category_list).distinct()

            elif publisher:
                publisher_list = Query.check_fields(category.split(','), PublisherModel)
                return BookModel.objects.filter(publisher__name__in=publisher_list).distinct()

            else:
                return BookModel.objects.all()

        except BookModel.DoesNotExist:
            return None


class CreateBook(graphene.Mutation):
    class Arguments:
        author = graphene.List(graphene.String)
        category = graphene.List(graphene.String)
        owner = graphene.String()
        publisher = graphene.String()
        name = graphene.String()
        age_group = graphene.String()
        in_stock = graphene.Boolean()
        page_number = graphene.Int()
        description = graphene.String()
        price = graphene.Float()

    book_obj = graphene.Field(BookType)

    def mutate(
            root, info, author, category, owner,
            publisher, name, age_group, in_stock,
            page_number, description, price,
    ):
        if not PublisherModel.objects.filter(name=publisher).exists():
            return None
        if not User.objects.filter(username=owner).exists():
            return None

        book_obj = BookModel.objects.create(
            name=name, age_group=age_group,
            in_stock=in_stock, page_number=page_number,
            description=description, price=price,
            publisher=PublisherModel.objects.get(name=publisher),
            owner=User.objects.get(username=owner),
        )
        category_set = []

        for c in category[0].split(','):
            if CategoryModel.objects.filter(name=c).exists():
                category_obj = CategoryModel.objects.get(name=c)
                category_set.append(category_obj)
        book_obj.category.set(category_set)

        author_set = []
        for a in author[0].split(','):
            if AuthorModel.objects.filter(name=a).exists():
                author_obj = AuthorModel.objects.get(name=a)
                author_set.append(author_obj.id)
        book_obj.author.add(*author_set)
        book_obj.save()
        # import pdb;
        # pdb.set_trace()

        return CreateBook(book_obj=book_obj)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
