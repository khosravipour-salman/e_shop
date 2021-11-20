from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import graphene
from store.types import (
    BookType, UserType,
    CommentType, WishListType,
    ShopBasketType, OrderType
)
from store.models import (
    BookModel, CategoryModel, PublisherModel, AuthorModel, OrderModel,
    ImageModel, CommentModel, WishListModel, ShopBasketModel,
)
from graphene_file_upload.scalars import Upload


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
    get_user_info = graphene.Field(UserType, )

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

    def resolve_get_user_by_id(root, info):
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=user_id)
        return user_obj

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
        if not User.objects.filter(username=owner).exists() or User.objects.filter(is_staff=False):
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

        return CreateBook(book_obj=book_obj)


class UpdateBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        name = graphene.String()
        publisher = graphene.String()
        age_group = graphene.String()
        page_number = graphene.Int()
        price = graphene.Float()
        description = graphene.String()
        in_stock = graphene.Boolean()

    book_obj = graphene.Field(BookType)

    def mutate(
            root, info, book_id, name=None, publisher=None, age_group=None,
            page_number=None, price=None, description=None, in_stock=None
    ):
        user_id = info.context.COOKIES['user_id']
        if User.objects.filter(pk=user_id, is_staff=False).exists():
            return None

        if not BookModel.objects.filter(pk=book_id).exists():
            return None
        if not PublisherModel.objects.filter(name=publisher).exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)

        book_obj.name = name if name is not None else book_obj.name
        book_obj.age_group = age_group if age_group is not None else book_obj.age_group
        book_obj.page_number = page_number if page_number is not None else book_obj.page_number
        book_obj.price = price if price is not None else book_obj.price
        book_obj.description = description if description is not None else book_obj.description
        book_obj.in_stock = in_stock if in_stock is not None else book_obj.in_stock

        book_obj.publisher = PublisherModel.objects.get(name=publisher) if publisher is not None else book_obj.publisher

        book_obj.save()
        return UpdateBook(book_obj=book_obj)


class UpdateBookAuthor(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        author_list = graphene.List(graphene.String)
        procedure = graphene.String()

    book_obj = graphene.Field(BookType)

    def mutate(root, info, book_id, author_list, procedure):
        if not BookModel.objects.filter(pk=book_id).exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)

        author_set = []
        for author in author_list[0].split(','):
            if AuthorModel.objects.filter(name=author).exists():
                author_obj = AuthorModel.objects.get(name=author)
                author_set.append(author_obj)

        if procedure == "add":
            book_obj.author.add(*author_set)
        elif procedure == "remove":
            book_obj.author.remove(*author_set)

        book_obj.save()
        return UpdateBookAuthor(book_obj=book_obj)


class UpdateBookCategory(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        category_list = graphene.List(graphene.String)
        procedure = graphene.String()

    book_obj = graphene.Field(BookType)

    def mutate(root, info, book_id, category_list, procedure):
        if not BookModel.objects.filter(pk=book_id).exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)

        category_set = []
        for category in category_list[0].split(','):
            if CategoryModel.objects.filter(name=category).exists():
                category_obj = CategoryModel.objects.get(name=category)
                category_set.append(category_obj)

        if procedure == "add":
            book_obj.category.add(*category_set)
        elif procedure == "remove":
            book_obj.category.remove(*category_set)

        book_obj.save()
        return UpdateBookCategory(book_obj=book_obj)


class UploadBookCover(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        book_cover = Upload(required=True, description="book cover")

    book_obj = graphene.Field(BookType)

    def mutate(root, info, book_id, book_cover):
        if not BookModel.objects.filter(pk=book_id).exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)
        img_obj = ImageModel.objects.create(book=book_obj, image=book_cover)

        return UploadBookCover(book_obj=book_obj)


class AddComment(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        user = graphene.String()
        email = graphene.String()
        body = graphene.String()
        active = graphene.Boolean()

    comment_obj = graphene.Field(CommentType)

    def mutate(root, info, book_id, user, email, body, active):
        if not BookModel.objects.filter(pk=book_id).exists():
            return None
        if not User.objects.filter().exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)
        comment_obj = CommentModel.objects.create(
            book=book_obj,
            user=User.objects.get(username=user),
            email=email,
            body=body,
            active=active,
        )

        return AddComment(comment_obj=comment_obj)


class DeleteBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()

    book_obj = graphene.Field(BookType)

    def mutate(root, info, book_id):
        if not BookModel.objects.filter(pk=book_id).exists():
            return None

        book_obj = BookModel.objects.get(pk=book_id)
        book_obj.delete()
        return DeleteBook(book_obj=book_obj)


class AddToWishlist(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()

    wishlist_obj = graphene.Field(WishListType)

    def mutate(root, info, book_id):
        if not BookModel.objects.filter().exists():
            return None
        book_obj = BookModel.objects.get(pk=book_id)

        user_id = info.context.COOKIES["user_id"]
        user_obj = User.objects.get(pk=int(user_id))

        if not user_obj.wishlist_books.exists():
            wishlist_obj = WishListModel.objects.create(user=user_obj)
            wishlist_obj.books.add(book_obj)
        else:
            wishlist_obj = WishListModel.objects.get(user=user_obj)
            wishlist_obj.books.add(book_obj)

        return AddToWishlist(wishlist_obj=wishlist_obj)


class CreateBasket(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()

    shop_basket_obj = graphene.Field(ShopBasketType)

    def mutate(root, info, book_id):
        book_obj = BookModel.objects.get(pk=book_id)
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=int(user_id))
        user_basket_exist = True if ShopBasketModel.objects.filter(user=user_obj, book=book_obj).exists() else False

        if not user_basket_exist:
            basket_obj = ShopBasketModel.objects.create(user=user_obj, book=book_obj, quantity=1)
        else:
            return None

        return CreateBasket(shop_basket_obj=basket_obj)


class DeleteBasket(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()

    book_obj = graphene.Field(BookType)

    def mutate(root, info, book_id):
        book_obj = BookModel.objects.get(pk=book_id)
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=int(user_id))
        user_basket_exist = True if ShopBasketModel.objects.filter(user=user_obj, book=book_obj).exists() else False

        if user_basket_exist:
            ShopBasketModel.objects.get(user=user_obj, book=book_obj).delete()
        else:
            return None

        return DeleteBasket(book_obj=book_obj)


class UpdateBasket(graphene.Mutation):
    class Arguments:
        book_id = graphene.ID()
        method = graphene.String()

    basket_obj = graphene.Field(ShopBasketType)

    def mutate(root, info, book_id, method):
        book_obj = BookModel.objects.get(pk=book_id)
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=int(user_id))
        user_basket_exist = True if ShopBasketModel.objects.filter(user=user_obj, book=book_obj).exists() else False

        if user_basket_exist:
            basket_obj = ShopBasketModel.objects.get(user=user_obj, book=book_obj)
            if method == "increase":
                basket_obj.quantity += 1

            elif method == "decrease":
                if basket_obj.quantity == 1:
                    pass
                elif basket_obj.quantity > 1:
                    basket_obj.quantity -= 1

            basket_obj.save()
            return UpdateBasket(basket_obj=basket_obj)

        else:
            return None


class Checkout(graphene.Mutation):
    class Arguments:
        city = graphene.String()
        address = graphene.String()
        delivery_date = graphene.Date()
        phone_number = graphene.String()
        postal_code = graphene.String()
        national_code = graphene.String()

    order_obj = graphene.Field(OrderType)

    def mutate(root, info, city, address, delivery_date, phone_number, postal_code, national_code):

        from ipdb import set_trace

        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=int(user_id))
        # set_trace()
        order_obj = OrderModel.objects.get(user=user_obj, status="Prepayment")

        order_obj.city = city
        order_obj.address = address
        order_obj.delivery_date = delivery_date
        order_obj.phone_number = phone_number
        order_obj.postal_code = postal_code
        order_obj.national_code = national_code
        order_obj.status = "Inprocess"

        order_obj.save()

        return Checkout(order_obj=order_obj)


class CancelOrder(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID()

    order_obj = graphene.Field(OrderType)

    def mutate(root, info, order_id):
        order_obj = OrderModel.objects.get(pk=order_id)
        order_obj.delete()

        return CancelOrder(order_obj=order_obj)


class UserSignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user_obj = graphene.Field(UserType)

    def mutate(root, info, username, password, email, first_name=None, last_name=None):
        user_obj = User.objects.create(
            username=username,
            email=email,
        )
        user_obj.set_password(password)

        if first_name is not None:
            user_obj.first_name = first_name
        if last_name is not None:
            user_obj.last_name = last_name

        user_obj.save()
        return UserSignUp(user_obj=user_obj)


class UserSignIn(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
    user_obj = graphene.Field(UserType)

    def mutate(root, info, username, password):
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(info.context, user_obj)
            return UserSignIn(user_obj=user_obj)
        else:
            return None


class UserSignOut(graphene.Mutation):
    class Arguments:
        pass
    user_obj = graphene.Field(UserType)

    def mutate(root, info):
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=user_id)
        logout(user_obj)
        return UserSignOut(user_obj=user_obj)


class CompleteUserInformation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    user_obj = graphene.Field(UserType)

    def mutate(root, info, first_name, last_name, email):
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=user_id)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = email

        user_obj.save()


class StaffSignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    user_obj = graphene.Field(UserType)

    def mutate(root, info, username, password, email, first_name=None, last_name=None):
        user_obj = User.objects.create(
            username=username,
            email=email,
            is_staff=True,
        )
        user_obj.set_password(password)
        if first_name is not None:
            user_obj.first_name = first_name
        if last_name is not None:
            user_obj.last_name = last_name

        user_obj.save()
        return StaffSignUp(user_obj=user_obj)


class StaffSignIn(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user_obj = graphene.Field(UserType)

    def mutate(root, info, username, password):
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(user_obj)
            return StaffSignIn(user_obj=user_obj)

        else:
            return None


class StaffSignOut(graphene.Mutation):
    class Arguments:
        pass
    user_obj = graphene.Field(UserType)

    def mutate(root, info):
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=user_id)
        logout(info.context)
        return StaffSignOut(user_obj=user_obj)


class CompleteStaffInfo(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    user_obj = graphene.Field(UserType)

    def mutate(root, info, first_name, last_name):
        user_id = info.context.COOKIES['user_id']
        user_obj = User.objects.get(pk=user_id)
        user_obj.first_name = first_name
        user_obj.last_name = last_name

        return CompleteStaffInfo(user_obj=user_obj)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    update_book_author = UpdateBookAuthor.Field()
    upload_book_cover = UploadBookCover.Field()
    add_comment = AddComment.Field()
    delete_book = DeleteBook.Field()
    add_to_wishlist = AddToWishlist.Field()
    create_basket = CreateBasket.Field()
    delete_basket = DeleteBasket.Field()
    update_basket = UpdateBasket.Field()
    checkout_order = Checkout.Field()
    cancel_order = CancelOrder.Field()
    user_signup = UserSignUp.Field()
    user_signin = UserSignIn.Field()
    user_signout = UserSignOut.Field()
    complete_user_info = CompleteUserInformation.Field()
    staff_signup = StaffSignUp.Field()
    staff_signin = StaffSignIn.Field()
    staff_signout = StaffSignOut.Field()
    complete_staff_info = CompleteStaffInfo.Field()
