from django.contrib import admin
from .models import Hero, HeroImage, Comment, CommentLike

# Register your models here.
class HeroimagesInline(admin.TabularInline):
    model = HeroImage
    extra = 1

class HeroAdmin(admin.ModelAdmin):
    inlines = [HeroimagesInline]
    list_display = ('name', 'nationality', 'year_of_birth', 'year_of_death', 'user')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Hero)
admin.site.register(HeroImage)
admin.site.register(Comment)
admin.site.register(CommentLike)