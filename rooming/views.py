# Create your views here.
import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy

from rooming.models import GRT, Room, Resident
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    all_rooms = Room.objects.order_by('number')
    grt_sections = GRT.objects.order_by('section_name')

    num_available_doubles = 0
    num_half_full_doubles = 0
    num_full_doubles = 0
    num_available_singles = 0
    num_full_singles = 0
    for r in all_rooms:
        if r.max_occupancy == 2:
            num_occupants = r.num_occupants()
            if num_occupants == 0:
                num_available_doubles += 1
            elif num_occupants == 1:
                num_half_full_doubles += 1
            else: # assume full
                num_full_doubles += 1
        else: # assume single
            if r.num_occupants() == 0:
                num_available_singles += 1
            else:
                num_full_singles += 1

    context = {
        'all_rooms': all_rooms,
        'num_available_doubles': num_available_doubles,
        'num_half_full_doubles': num_half_full_doubles,
        'num_full_doubles': num_full_doubles,
        'num_available_singles': num_available_singles,
        'num_full_singles': num_full_singles,
        'grt_sections': grt_sections
    }
    return render(request, 'rooming/index.html', context)

@login_required(login_url='login')
def csvOutput(request):
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="rooming.csv"'

    writer = csv.writer(response)

    residents = Resident.objects.order_by('athena')

    for resident in residents:
        writer.writerow([resident.athena, resident.room.number])

    return response

@login_required(login_url='login')
def data(request):
    all_rooms = Room.objects.order_by('number')
    all_residents = Resident.objects.order_by('athena')
    all_grts = GRT.objects.order_by('section_name')


    grt_min_freshmen = {g.section_name: g.min_freshmen_doubles for g in all_grts}
    grt_occupied = {g.section_name: 0 for g in all_grts}
    grt_total_rooms = {g.section_name: 0 for g in all_grts}
    
    response_data = {}
    for r in all_rooms:
        response_data[r.number] = {'room': 
{'number' : r.number,
 'type' : r.type(),
 'num_occupants' : 0,
 'status': 0,
 'grt':r.grt_section.section_name}, 'residents': []}
        grt_total_rooms[r.grt_section.section_name] += 1

    for res in all_residents:
        response_data[res.room.number]['residents'].append(res.athena)
        response_data[res.room.number]['room']['status'] = 1
        if response_data[res.room.number]['room']['num_occupants'] == 0:
            grt_occupied[res.room.grt_section.section_name] += 1
            if res.room.max_occupancy == 2:
                response_data[res.room.number]['room']['status'] = 3
        response_data[res.room.number]['room']['num_occupants'] += 1
        
            
    for r in response_data:
        grt = response_data[r]['room']['grt']
        num_remain = grt_total_rooms[grt] - (grt_min_freshmen[grt] + grt_occupied[grt] )
        response_data[r]['room']['grtinfo'] = str(num_remain)+"/"+str(grt_total_rooms[grt])
        if num_remain <= 0 and response_data[r]['room']['status'] == 0:
            response_data[r]['residents'] = ['Reserved for incoming freshmen']
            response_data[r]['room']['status'] = 2
        

    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@login_required(login_url='login')
def entry(request):
    # admin login
    all_rooms = Room.objects.order_by('number')
    grt_sections = GRT.objects.order_by('section_name')

    num_available_doubles = 0
    num_half_full_doubles = 0
    num_full_doubles = 0
    num_available_singles = 0
    num_full_singles = 0
    for r in all_rooms:
        if r.max_occupancy == 2:
            num_occupants = r.num_occupants()
            if num_occupants == 0:
                num_available_doubles += 1
            elif num_occupants == 1:
                num_half_full_doubles += 1
            else: # assume full
                num_full_doubles += 1
        else: # assume single
            if r.num_occupants() == 0:
                num_available_singles += 1
            else:
                num_full_singles += 1

    context = {
        'all_rooms': all_rooms,
        'grt_sections': grt_sections,
        'num_available_doubles': num_available_doubles,
        'num_half_full_doubles': num_half_full_doubles,
        'num_full_doubles': num_full_doubles,
        'num_available_singles': num_available_singles,
        'num_full_singles': num_full_singles,
    }
    return render(request, 'rooming/entry.html', context)

@login_required(login_url='login')
def rawentry(request):
    # admin login
    all_rooms = Room.objects.order_by('number')
    grt_sections = GRT.objects.order_by('section_name')
    
    context = {
        'all_rooms': all_rooms,
        'grt_sections': grt_sections
    }
    return render(request, 'rooming/rawentry.html', context)

@login_required(login_url='login')
def text(request):
    all_rooms = Room.objects.order_by('number')
    grt_sections_orig = GRT.objects.order_by('section_name')
    grt_sections = {g.section_name: {'grt':g, 'total':0, 'freshmen':g.min_freshmen_doubles, 'occupied':0} for g in grt_sections_orig}
    empty_rooms = []
    occupied_rooms = []
    for room in all_rooms:
        if room.full():
            occupied_rooms.append(room)
        else:
            empty_rooms.append(room)


    all_residents = Resident.objects.order_by('athena')
    all_grts = GRT.objects.order_by('section_name')

    response_data = {}
    for r in all_rooms:
        response_data[r.number] = {'room': 
{'number' : r.number,
 'type':r.type,
 'num_occupants' : 0,
 'available' : True,
 'residents' : [],
 'grt':r.grt_section.section_name}, 'residents': []}
        grt_sections[r.grt_section.section_name]['total'] += 1

    for res in all_residents:
        response_data[res.room.number]['room']['residents'].append(res.athena)
        if response_data[res.room.number]['room']['num_occupants'] +1 == res.room.max_occupancy:            
            response_data[res.room.number]['room']['available'] = False
        if response_data[res.room.number]['room']['num_occupants'] == 0:            
            grt_sections[res.room.grt_section.section_name]['occupied'] += 1
        response_data[res.room.number]['room']['num_occupants'] += 1
    
    for (k,v) in grt_sections.iteritems():
        v['remain'] = v['total'] - v['occupied'] - v['freshmen']


    for r in response_data:
        grt = response_data[r]['room']['grt']
        num_remain = grt_sections[grt]['remain']
        if num_remain <= 0:
            response_data[r]['room']['available'] = False

    avail_rooms = [v['room'] for (k,v) in response_data.iteritems() if v['room']['available']]
    avail_rooms.sort(key=lambda r: r['number'])


    num_available_doubles = 0
    for r in all_rooms:
        if r.max_occupancy == 2 and r.empty():
            num_available_doubles += 1

    grt_output = [grt_sections[k] for k in grt_sections]
    grt_output.sort(key=lambda g: g['grt'].section_name)
    context = {
        'empty_rooms': empty_rooms,
        'avail_rooms': avail_rooms,
        'occupied_rooms': occupied_rooms,
        'grt_sections': grt_output,
        'num_available_doubles': num_available_doubles,
        "msg": str(grt_sections)+'hi',
    }
    return render(request, 'rooming/text.html', context)

@login_required(login_url='login')
def return_failure(fail_msg):
    response_data = {}
    response_data['status'] = 1
    response_data['msg']    = fail_msg
    return HttpResponse(fail_msg)
    # TODO: fix this
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@login_required(login_url='login')
def return_success(msg, data={}):
    response_data = data
    response_data['status'] = 0
    response_data['msg']    = msg
    return HttpResponse(msg)
    # TODO: fix this
    return HttpResponse(simple.dumps(response_data), mimetype="application/json")
    

@login_required(login_url='login')
def update(request):
    # admin login
    roomnum = request.POST['roomnum']
    name = request.POST['name']
    if name == "":
        return return_failure("Empty name")

    # Get Room
    try:
        room = Room.objects.filter(number=roomnum)[0]
    except:
        return return_failure("No such room with number "+ roomnum)

    # Check that GRT has min number of doubles available
    if room.grt_section.filled():
        return return_failure("Did not add resident. Not enough freshman doubles in "+room.grt_section.section_name)

    # Get Resident
    existed = False
    try:
        resident = Resident.objects.filter(athena=name)[0]
        existed = True
    except:
        resident = Resident(athena=name, room = room)
        #return_failure("No such user with athena "+ name)

    
    # Change Resident's room
    old_room = resident.room
    resident.room = room

    # Check new room
    num_occupants = len(room.resident_set.all())
    if num_occupants + 1 > room.max_occupancy:
        return return_failure("Did not add resident. Too many occupants for "+room.type())

    # Valid change. Save room
    resident.save()
    
    if existed and old_room != room:
        return return_success(name + " was moved from room "+old_room.number+" to room "+roomnum+"!")
    else:
        return return_success(name + " was assigned to room "+roomnum+"!")

@login_required(login_url='login')
def removeresident(request):
    # admin login
    athena = request.POST["athena"]
    resident = Resident.objects.all().filter(athena=athena)[0]
    room_num = resident.room.number
    resident.delete()
    return return_success(athena + " was deleted from room " + room_num)
