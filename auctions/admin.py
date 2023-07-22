from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "type")


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "listing_id", 
        "title",
        "price",
        "user",
        "category",
        "winner",
        "active"
    )
    filter_horizontal = ("watchers", )

class BidAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "listing",
        "user"
    )

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "user",
        "description"
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
