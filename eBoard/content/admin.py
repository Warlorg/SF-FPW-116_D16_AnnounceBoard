from django.contrib import admin
from .models import Announce, UserReaction


class UserReactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'announce', 'text', 'dateCreation', 'status')
    list_filter = ('status', 'dateCreation',)
    search_fields = ('author', 'text', 'announce')


admin.site.register(Announce)
admin.site.register(UserReaction, UserReactionAdmin)
