import math, datetime, time, json, json as json_util
from django.db import connection
from django.db.models.expressions import Window
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from .models import meters, meterserials, meterserials_details
from .forms import meterForm, meterserialsForm, serialsdetailsForm

from django.views.generic import CreateView, FormView, RedirectView, ListView
from django.utils.dateparse import parse_datetime

# Create your views here.

datetoday = datetime.date.today()

header = 'Dashboard'


class RRViews(ListView):
    model = meters
    html = 'meters/meter_list.html'
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.filter(
            serialnos__icontains=self.request.GET.get('filter'),
            rrnumber__icontains=self.request.GET.get('filter'),).values('id', 'dateforwarded', 'brand',  'serialnos','metertype', 'units','rrnumber',  'active', 'userid').order_by( self.request.GET.get('order_by') )

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            start = int(request.GET.get('start'))
            limit = int(request.GET.get('limit'))
            filter = request.GET.get('filter')
            # order_by = request.GET.get('order_by')
            list_data = []
            for index, item in enumerate(self.get_queryset()[start:start+limit], start):
                list_data.append(item)
            data = {
                'length': self.get_queryset().count(),
                'objects': list_data,
            }
            return HttpResponse(json.dumps(data, default=default), 'application/json')
        else:
            return render(request, self.html, {'header': 'Meters'})


def delete_meters(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        meterinfo = meters.objects.get(pk=id)
        meterinfo.delete()
        json_response = {json.dumps('deleted')}
    return HttpResponse(json_response, content_type='application/json')

# Meter Serials


# class MeterList(CreateView):
def seriallist(request, id):
    return render(request, 'meters/list_serials.html', {'idmeters': id, 'header':'List of Meter Serial'})

def seriallist_data(request, id):
    if request.is_ajax():
        start = int(request.GET.get('start'))
        limit = int(request.GET.get('limit'))
        filter = request.GET.get('filter')
        order_by = request.GET.get('order_by')
        query = meterserials.objects.select_related('meters').filter(idmeters=id,
            serialno__icontains=filter,).values('id', 'idmeters', 'serialno', 'ampheres',
                                            'accuracy', 'wms_status', 'status', 'active', 'userid', 'idmeters__brand').order_by(order_by)
        list_data = []
        for index, item in enumerate(query[start:start+limit], start):
            list_data.append(item)
        data = {
            'length': query.count(),
            'objects': list_data,
        }
        return HttpResponse(json.dumps(data, default=default), 'application/json')


def selected_serial(request):
    if request.is_ajax():
        id = request.GET.get('id')
        idmeters = request.GET.get('idmeters')
        queryset = meterserials_details.objects.filter(idmeterserials=id).order_by('idmeterserials')
        html = 'meters/list_serials_ext.html'
        context = {'trans': queryset, 'id': id, 'idmeters': idmeters}
        return render(request, html, context)


def calibrate_meter(request, id, idmeters):
    if request.method == "POST":
        form = serialsdetailsForm(request.POST)
        if form.is_valid():
            form.save()
            idmeterserials = request.POST['idmeterserials']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute(
                'update zanecometerpy.meter_serials set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(idmeterserials) + '"')
            cursor.fetchall()
        return redirect("../../")
            # html = 'meters/calibrate.html'
            # context = {'save': 'save'}
        # return render(request, html, context)
    else:
        serials = meterserials.objects.get(id=id)
        form = serialsdetailsForm(request.POST)
        html = 'meters/calibrate.html'
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': idmeters}
        return render(request, html, context)


def edit_meters(request, id, idmeters):
    if request.method == "POST":
        queryset = meterserials_details(pk=id)
        form = serialsdetailsForm(request.POST, instance=queryset)
        if form.is_valid():
            created = request.POST.get('created_at')
            print(parse_datetime(created))
            rec = form.save(commit=False)
            rec.created_at = datetoday
            rec.save()

            cursor = connection.cursor()
            idmeterserials = request.POST['idmeterserials']
            average = request.POST['gen_average']
            cursor.execute(
                'update zanecometerpy.meter_serials set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(idmeterserials) + '"')
            cursor.fetchall()
        return redirect("../../")
    else:
        queryset = meterserials_details.objects.get(pk=id)
        serials = meterserials.objects.get(id=idmeters)
        # serials = meterserials.objects.select_related(
        #     "meter_serials").filter(id=idmeters)
        context = {'form': queryset, 'datetoday': datetoday, 'serials': serials}
        return render(request, 'meters/calibration_edit.html', context)

# multiple calibration
def multiple_calibration(request, id):
    html = 'meters/calibration_multiple.html'
    serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
    form = serialsdetailsForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            idmeterserials = request.POST['idmeterserials']
            average = request.POST['gen_average']
            cursor = connection.cursor()
            cursor.execute(
                'update zanecometerpy.meter_serials set wms_status=1, status = if("' + str(average) + '" >= 98,1,2), accuracy="' + str(average) + '" where id = "' + str(idmeterserials) + '"')
            cursor.fetchall()
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id, 'save': 'save'}
        return render(request, html, context)
    else:
        form = serialsdetailsForm(request.POST)
        # serials = meterserials.objects.filter(idmeters=id).filter(wms_status__exact=0)
        context = {'form': form, 'datetoday': datetoday,
                   'serials': serials, 'idmeters': id}
        return render(request, html, context)


def delete_serials(request, id):
    if request.is_ajax():
        id = request.GET.get('id')
        serialinfo = meterserials_details.objects.get(pk=id)
        serialinfo.delete()
        json_response = {json.dumps('deleted')}
    return HttpResponse(json_response, content_type='application/json')


def meter_test_report(request, id, idmeters):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute('SELECT brand, serialno, ampheres, accuracy, msd.* FROM zanecometerpy.meter_serials_details msd ' +
	                   'left join meter_serials ms on ms.id = msd.idmeterserials ' +
                       'left join meters m on m.id=ms.idmeters ' +
                       'where msd.id = "' + str(id) + '";')
        form = cursor.fetchall()
        html = 'meters/meter_test_report.html'
        context = {'form': form, 'datetoday': datetoday}
    return render(request, html, context)


def save_selectedTable(request):
    if request.is_ajax():
        id = request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute('update zanecometerpy.meter_serials set wms_status=2 where id = "'+ str(id) +'" ')
        cursor.fetchall()
        html = 'meters/meter_list.html'
        return render(request, html)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()














        # form = serialsdetailsForm(request.POST, instance=queryset)

        # cursor = connection.cursor()
        # cursor.execute('select idmeterserials ' +
        #                '   from zanecometerpy.meter_serials_details ' +
        #             #    '   where idmeterserials like "' + str(id) + '" ' +
        #                '    ;')
        # result = cursor.fetchall()
