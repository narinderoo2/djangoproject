from django.contrib import admin
from .models import Comment
from .models import News,Contact,Message
#from import_export.admin import ImportExportModelAdmin

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Message)
