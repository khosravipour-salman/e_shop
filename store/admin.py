from django.contrib import admin
from store.models import (
    BookModel, AuthorModel,
    CategoryModel, CommentModel,
    ImageModel, PublisherModel,
    WishListModel, ShopBasketModel,
    OrderModel,
)


class ShopBasketAdmin(admin.ModelAdmin):
    model = ShopBasketModel
    list_display = ('id', 'user', 'book', 'quantity', )


admin.site.register(ShopBasketModel, ShopBasketAdmin)


class OrderAdmin(admin.ModelAdmin):
    model = OrderModel
    list_display = ('id', 'city', 'address', 'delivery_date', 'phone_number', 'postal_code', 'national_code', 'status',)


admin.site.register(OrderModel, OrderAdmin)


class WishListAdmin(admin.ModelAdmin):
    model = WishListModel
    list_display = ('id', )


admin.site.register(WishListModel, WishListAdmin)


class ImageModelAdminInline(admin.TabularInline):
    model = ImageModel
    extra = 2


class BookModelAdmin(admin.ModelAdmin):
    model = BookModel
    list_display = ('id', 'name', 'age_group', 'in_stock', 'page_number', 'price', 'description',)
    inlines = [ImageModelAdminInline, ]


admin.site.register(BookModel, BookModelAdmin)


class AuthorModelAdmin(admin.ModelAdmin):
    model = AuthorModel
    list_display = ('name',)


admin.site.register(AuthorModel, AuthorModelAdmin)


class CategoryModelAdmin(admin.ModelAdmin):
    model = CategoryModel
    list_display = ('name',)


admin.site.register(CategoryModel, CategoryModelAdmin)


class CommentModelAdmin(admin.ModelAdmin):
    model = CommentModel
    list_display = ('email', 'body', 'created_on', 'active',)


admin.site.register(CommentModel, CommentModelAdmin)


class PublisherModelAdmin(admin.ModelAdmin):
    model = PublisherModel
    list_display = ('name', )


admin.site.register(PublisherModel, PublisherModelAdmin)


class ImageModelAdmin(admin.ModelAdmin):
    model = ImageModel
    list_display = ('image',)


admin.site.register(ImageModel, ImageModelAdmin)
