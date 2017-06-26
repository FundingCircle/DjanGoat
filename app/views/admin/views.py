import pytz
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from app.models.User.user import User
from app.models.Analytics.analytics import Analytics
from app.views import utils
from app.decorators import user_is_authenticated



@require_http_methods(["GET"])
@user_is_authenticated
def admin_dashboard(request, selected_id):
    user = utils.current_user(request)
    return render(request, 'admin/dashboard.html',
                  context={'current_user': user})


@require_http_methods(["GET"])
@user_is_authenticated
def admin_get_user(request, selected_id):
    success = True
    user = None
    try:
        user = User.objects.get(user_id=int(selected_id))
    except User.DoesNotExist:
        success = False

    if user is None:
        other_is_admin_val = False
    else:
        other_is_admin_val = not user.is_admin

    return render(request, 'admin/modal.html',
                  {'user': user, 'other_admin_val': other_is_admin_val})


@require_http_methods(["POST"])
@user_is_authenticated
def admin_delete_user(request, selected_id):
    success = True
    try:
        user = User.objects.get(user_id=int(selected_id))
        user.delete()
    except User.DoesNotExist:
        success = False

    msg = "success" if success else "failure"
    return JsonResponse({'msg': msg})


@require_http_methods(["POST", "PATCH"])
@user_is_authenticated
def admin_update_user(request, selected_id):
    success = True
    try:
        user = User.objects.get(user_id=int(selected_id))
        data = request.POST.dict().copy()
        if data:
            password = data['password']
            data.pop('password')
            data.pop('password_confirmation')
            data['updated_at'] = pytz.utc.localize(datetime.datetime.now())
            if password != '':
                user.password = password
                user.save()
        User.objects.filter(user_id=int(selected_id)).update(**data)
    except User.DoesNotExist:
        success = False

    msg = "success" if success else "failure"
    return JsonResponse({'msg': msg})


@require_http_methods(["GET"])
@user_is_authenticated
def admin_get_all_users(request, selected_id):
    users = User.objects.all()
    # render appropriately
    users2 = ['dsds', 'f', 'f', 'f']
    return render(request, 'admin/table.html',
                  {'users': users, 'users2': users2})


@require_http_methods(["GET"])
@user_is_authenticated
def admin_analytics(request, selected_id):
    user = utils.current_user(request)
    data = request.GET.dict().copy()
    show_user_agent = False
    show_ip_address = False
    show_referrer = False
    col = []
    for key in data:
        if key != 'ip':
            col.append(key)
    col = ', '.join(col)

    if request.GET.get('ip', '') != '':
        if len(col) == 0:
            col = "*"
        analytics = Analytics.hits_by_ip(request.GET['ip'], col=col)

    else:
        analytics = Analytics.objects_in_list()
    cols = [key for key in analytics]
    values = analytics.values()
    num_data = range(len(values[0]))
    return render(request, 'admin/analytics.html',
                  {'cols': cols, 'values': values, 'num_data': num_data,
                   'current_user': user})
