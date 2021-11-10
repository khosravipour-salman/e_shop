from django.contrib import admin
from store.models import (BookModel, AuthorModel,
                          CategoryModel, CommentModel,
                          ImageModel, PublisherModel)


class ImageModelAdminInline(admin.TabularInline):
    model = ImageModel
    # readonly_fields = ('title', 'url', 'display_score')
    # fields = ('title', 'url', 'display_score')


class BookModelAdmin(admin.ModelAdmin):
    model = BookModel
    list_display = ('name', 'age_group', 'in_stock', 'page_number', 'price', 'description',)
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
