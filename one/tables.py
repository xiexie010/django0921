import django_tables2 as tables
from .models import UserInfo






class UserInfoTable(tables.Table):

    class Meta:
        model = UserInfo
        sequence=('username','password')
        exclude=('id',)
        template_name = 'django_tables2/bootstrap.html'

class TableView(tables.SingleTableView):
    table_class = UserInfoTable
    queryset = UserInfo.objects.all()
    template_name = "simple_list.html"