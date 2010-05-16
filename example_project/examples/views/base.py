import logging

from django.views.generic import simple
from django.views.generic import list_detail
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from examples.forms import ContactForm
from examples.forms import TaskForm
from examples.forms import TaskFilter
from examples.forms import UserForm
from examples.forms import MultipleChoicesForm
from examples.models import Task, Project
from richtemplates.forms import UserProfileForm
from richtemplates.skins import SkinDoesNotExist, set_skin_at_request

def messages_view(request, template_name='examples/messages.html'):
    tags = ['debug', 'info', 'success', 'warning', 'info']
    for tag in tags:
        getattr(messages, tag)(request, "This is global message tagged as '%s'"
            % tag)

    context = {
        'tags': tags,
    }
    return render_to_response(template_name, context, RequestContext(request))

def colors(request, template_name='examples/color_tables.html'):
    extra_context = {'colors': SortedDict(COLORS)}
    return simple.direct_to_template(request, template_name, extra_context)

def contact(request, template_name='examples/contact.html'):

    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        msg = u"Form submitted."
        messages and messages.info(request, msg)
        logging.info(msg)
        if form.is_valid():
            success_msg = u"Submission successfully completed"
            messages and messages.success(request, success_msg)
            logging.info(success_msg)
        else:
            error_msg = u"Submission failed"
            messages and messages.error(request, error_msg)
            logging.error(error_msg)

    context = {
        'form': form,
    }
    return render_to_response(template_name, context, RequestContext(request))

def multiple_choices(request, template_name='examples/multiplechoices.html'):
    form = MultipleChoicesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            messages and messages.success(request, u'Submission succeeded')
        else:
            messages and messages.error(u'Submission failed')
    context = {'form': form}
    return render_to_response(template_name, context, RequestContext(request))

def manage_user_groups(request, username,
    template_name='examples/manage_user_groups.html'):
    """
    View to show usage of FilteredSelectMultiple admin's widget. Permissions
    are not the case here.
    """
    user = get_object_or_404(User, username=username)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
    context = {
        'form': form,
    }
    return render_to_response(template_name, context, RequestContext(request))

def task_list(request, template_name='examples/projects/task_list.html'):
    """
    Returns ``Task`` objects list.
    """
    task_list_info = {
        'queryset': Task.objects\
            .select_related('status', 'project', 'priority'),
        'template_object_name': 'task',
        'template_name': template_name,
    }
    return list_detail.object_list(request, **task_list_info)

def task_detail(request, task_id,
        template_name='examples/projects/task_detail.html'):
    """
    Returns single ``Task`` details.
    """
    task_detail_info = {
        'queryset': Task.objects\
            .select_related('status', 'project', 'priority'),
        'object_id': task_id,
        'template_name': template_name,
        'template_object_name': 'task',
    }
    return list_detail.object_detail(request, **task_detail_info)

def project_list(request,
    template_name='examples/projects/project_list.html'):
    """
    Returns ``Project`` objects list.
    """
    project_list_info = {
        'queryset': Project.objects.all().annotate(Count('task')),
        'template_name': template_name,
        'template_object_name': 'project',
    }
    return list_detail.object_list(request, **project_list_info)

def project_detail(request, project_id,
    template_name='examples/projects/project_detail.html'):
    """
    Returns single ``Project`` details.
    """
    project_info = {
        'queryset': Project.objects.all(),
        'template_name': template_name,
        'template_object_name': 'project',
        'object_id': project_id,
    }
    return list_detail.object_detail(request, **project_info)

#@csrf_exempt
def project_task_list(request, project_id,
    template_name='examples/projects/project_task_list.html'):
    """
    Returns ``Task`` objects list for chosen ``Project``.
    """
    project = get_object_or_404(Project, id=project_id)
    task_list = project.task_set\
        .select_related('status', 'priority')\
        .defer('content')
    filter = TaskFilter(request.GET,
        queryset=task_list, project=project)

    context = {
        'project': project,
        'filter': filter,
    }
    return render_to_response(template_name, context, RequestContext(request))

def task_edit(request, task_id,
    template_name='examples/projects/task_form.html'):
    """
    Edits ``Task`` object.
    """
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, "Task updated successfully.")
            return HttpResponseRedirect(task.get_absolute_url())
    else:
        form = TaskForm(instance=task)

    context = {
        'form' : form,
    }

    return render_to_response(template_name, context, RequestContext(request))

def forbidden(request):
    """
    Always returns HttpResponseForbidden, even for superuser.
    """
    return HttpResponseForbidden()

def set_skin(request, skin):
    """
    Set skin for user from given request.
    """
    try:
        set_skin_at_request(request, skin)
        message = _("Skin set to %s" % skin)
        messages.info(request, message)
    except SkinDoesNotExist:
        message = _("Skin %s does not exist")
        messages.error(request, message)
    return redirect('/')

def userprofile(request, username, template_name='richtemplates/accounts/profile.html'):
    """
    Basic user profile view.
    """
    user = get_object_or_404(User, username=username)
    context = {
        'profile': user.get_profile(),
    }
    return simple.direct_to_template(request, template_name, extra_context=context)

def userprofile_edit(request, username, template_name='richtemplates/accounts/profile_edit.html'):
    """
    Edit profile view.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        raise PermissionDenied
    form = UserProfileForm(request.POST or None, instance=user.get_profile())
    if request.method == 'POST' and form.is_valid():
        form.save()
        message = _("Profile updated successfully")
        messages.success(request, message)
        #return redirect(user.get_absolute_url())
    context = {
        'form': form,
    }
    return simple.direct_to_template(request, template_name, extra_context=context)

# Colors dict taken from http://www.computerhope.com/htmcolor.htm

COLORS = {
    'Black': '#000000',
    'COLOR NAME': 'CODE',
    'Cadet Blue3': '#77BFC7',
    'Cadet Blue4': '#4C787E',
    'Chartreuse': '#8AFB17',
    'Chartreuse2': '#7FE817',
    'Chartreuse3': '#6CC417',
    'Chartreuse4': '#437C17',
    'Chocolate': '#C85A17',
    'Coral': '#F76541',
    'Coral2': '#E55B3C',
    'Coral3': '#C34A2C',
    'Cornflower Blue': '#151B8D',
    'Cyan': '#00FFFF',
    'Cyan1': '#57FEFF',
    'Cyan2': '#50EBEC',
    'Cyan3': '#46C7C7',
    'Cyan4': '#307D7E',
    'Dark Goldenrod': '#AF7817',
    'Dark Goldenrod1': '#FBB117',
    'Dark Goldenrod2': '#E8A317',
    'Dark Goldenrod3': '#C58917',
    'Dark Goldenrod4': '#7F5217',
    'Dark Green': '#254117',
    'Dark Olive Green1': '#CCFB5D',
    'Dark Olive Green2': '#BCE954',
    'Dark Olive Green3': '#A0C544',
    'Dark Olive Green4': '#667C26',
    'Dark Orange': '#F88017',
    'Dark Orange1': '#F87217',
    'Dark Orange2': '#E56717',
    'Dark Orange3': '#7E3117',
    'Dark Orchid': '#7D1B7E',
    'Dark Orchid1': '#B041FF',
    'Dark Orchid2': '#A23BEC',
    'Dark Orchid3': '#8B31C7',
    'Dark Orchid4': '#571B7e',
    'Dark Salmon': '#E18B6B',
    'Dark Sea Green': '#8BB381',
    'Dark Sea Green1': '#C3FDB8',
    'Dark Sea Green2': '#B5EAAA',
    'Dark Sea Green3': '#99C68E',
    'Dark Sea Green4': '#617C58',
    'Dark Slate Blue': '#2B3856',
    'Dark Slate Gray': '#25383C',
    'Dark Slate Gray1': '#9AFEFF',
    'Dark Slate Gray2': '#8EEBEC',
    'Dark Slate Gray3': '#78c7c7',
    'Dark Slate Gray4': '#4C7D7E',
    'Dark Turquoise': '#3B9C9C',
    'Dark Violet': '#842DCE',
    'Deep Pink': '#F52887',
    'Deep Pink2': '#E4287C',
    'Deep Pink3': '#C12267',
    'Deep Pink4': '#7D053F',
    'Deep Sky Blue': '#3BB9FF',
    'Deep Sky Blue2': '#38ACEC',
    'Deep Sky Blue3': '#3090C7',
    'Deep Sky Blue4': '#25587E',
    'Dim Gray': '#463E41',
    'Dodger Blue': '#1589FF',
    'Dodger Blue2': '#157DEC',
    'Dodger Blue3': '#1569C7',
    'Dodger Blue4': '#153E7E',
    'Firebrick': '#800517',
    'Firebrick1': '#F62817',
    'Firebrick2': '#E42217',
    'Firebrick3': '#C11B17',
    'Forest Green': '#4E9258',
    'Gold': '#D4A017',
    'Gold1': '#FDD017',
    'Gold2': '#EAC117',
    'Gold3': '#C7A317',
    'Gold4': '#806517',
    'Goldenrod': '#EDDA74',
    'Goldenrod1': '#FBB917',
    'Goldenrod2': '#E9AB17',
    'Goldenrod3': '#C68E17',
    'Goldenrod4': '#805817',
    'Gray': '#736F6E',
    'Gray0': '#150517',
    'Gray18': '#250517',
    'Gray21': '#2B1B17',
    'Gray23': '#302217',
    'Gray24': '#302226',
    'Gray25': '#342826',
    'Gray26': '#34282C',
    'Gray27': '#382D2C',
    'Gray28': '#3b3131',
    'Gray29': '#3E3535',
    'Gray30': '#413839',
    'Gray31': '#41383C',
    'Gray32': '#463E3F',
    'Gray34': '#4A4344',
    'Gray35': '#4C4646',
    'Gray36': '#4E4848',
    'Gray37': '#504A4B',
    'Gray38': '#544E4F',
    'Gray39': '#565051',
    'Gray40': '#595454',
    'Gray41': '#5C5858',
    'Gray42': '#5F5A59',
    'Gray43': '#625D5D',
    'Gray44': '#646060',
    'Gray45': '#666362',
    'Gray46': '#696565',
    'Gray47': '#6D6968',
    'Gray48': '#6E6A6B',
    'Gray49': '#726E6D',
    'Gray50': '#747170',
    'Green': '#00FF00',
    'Green Yellow': '#B1FB17',
    'Green1': '#5FFB17',
    'Green2': '#59E817',
    'Green3': '#4CC417',
    'Green4': '#347C17',
    'Hot Pink': '#F660AB',
    'Hot Pink1': '#F665AB',
    'Hot Pink2': '#E45E9D',
    'Hot Pink3': '#C25283',
    'Hot Pink4': '#7D2252',
    'Indian Red1': '#F75D59',
    'Indian Red2': '#E55451',
    'Indian Red3': '#C24641',
    'Indian Red4': '#7E2217',
    'Khaki': '#ADA96E',
    'Khaki1': '#FFF380',
    'Khaki2': '#EDE275',
    'Khaki3': '#C9BE62',
    'Khaki4': '#827839',
    'Lavender': '#E3E4FA',
    'Lavender Blush': '#FDEEF4',
    'Lavender Blush2': '#EBDDE2',
    'Lavender Blush3': '#C8BBBE',
    'Lavender Blush4': '#817679',
    'Lawn Green': '#87F717',
    'Lemon Chiffon': '#FFF8C6',
    'Lemon Chiffon2': '#ECE5B6',
    'Lemon Chiffon3': '#C9C299',
    'Lemon Chiffon4': '#827B60',
    'Light Blue': '#ADDFFF',
    'Light Blue1': '#BDEDFF',
    'Light Blue2': '#AFDCEC',
    'Light Blue3': '#95B9C7',
    'Light Blue4': '#5E767E',
    'Light Coral': '#E77471',
    'Light Cyan': '#E0FFFF',
    'Light Cyan2': '#CFECEC',
    'Light Cyan3': '#AFC7C7',
    'Light Cyan4': '#717D7D',
    'Light Golden2': '#ECD672',
    'Light Goldenrod': '#ECD872',
    'Light Goldenrod Yellow': '#FAF8CC',
    'Light Goldenrod1': '#FFE87C',
    'Light Goldenrod3': '#C8B560',
    'Light Goldenrod4': '#817339',
    'Light Pink': '#FAAFBA',
    'Light Pink1': '#F9A7B0',
    'Light Pink2': '#E799A3',
    'Light Pink3': '#C48189',
    'Light Pink4': '#7F4E52',
    'Light Salmon': '#F9966B',
    'Light Salmon2': '#E78A61',
    'Light Salmon3': '#C47451',
    'Light Salmon4': '#7F462C',
    'Light Sea Green': '#3EA99F',
    'Light Sky Blue': '#82CAFA',
    'Light Sky Blue2': '#A0CFEC',
    'Light Sky Blue3': '#87AFC7',
    'Light Sky Blue4': '#566D7E',
    'Light Slate Blue': '#736AFF',
    'Light Slate Gray': '#6D7B8D',
    'Light Steel Blue': '#728FCE',
    'Light Steel Blue1': '#C6DEFF',
    'Light Steel Blue2': '#B7CEEC',
    'Light Steel Blue4': '#646D7E',
    'Lime Green': '#41A317',
    'Magenta': '#FF00FF',
    'Magenta1': '#F433FF',
    'Magenta2': '#E238EC',
    'Magenta3': '#C031C7',
    'Maroon': '#810541',
    'Maroon1': '#F535AA',
    'Maroon2': '#E3319D',
    'Maroon3': '#C12283',
    'Maroon4': '#7D0552',
    'Medium Aquamarine': '#348781',
    'Medium Forest Green': '#347235',
    'Medium Orchid': '#B048B5',
    'Medium Orchid1': '#D462FF',
    'Medium Orchid2': '#C45AEC',
    'Medium Orchid3': '#A74AC7',
    'Medium Orchid4': '#6A287E',
    'Medium Purple': '#8467D7',
    'Medium Purple1': '#9E7BFF',
    'Medium Purple2': '#9172EC',
    'Medium Purple3': '#7A5DC7',
    'Medium Purple4': '#4E387E',
    'Medium Sea Green': '#306754',
    'Medium Slate Blue': '#5E5A80',
    'Medium Spring Green': '#348017',
    'Medium Turquoise': '#48CCCD',
    'Medium Violet Red': '#CA226B',
    'Midnight Blue': '#151B54',
    'Pale Turquoise3': '#92C7C7',
    'Pale Turquoise4': '#5E7D7E',
    'Pale Violet Red': '#D16587',
    'Pale Violet Red1': '#F778A1',
    'Pale Violet Red2': '#E56E94',
    'Pale Violet Red3': '#C25A7C',
    'Pale Violet Red4': '#7E354D',
    'Pink': '#FAAFBE',
    'Pink2': '#E7A1B0',
    'Pink3': '#C48793',
    'Pink4': '#7F525D',
    'Plum': '#B93B8F',
    'Plum1': '#F9B7FF',
    'Plum2': '#E6A9EC',
    'Plum3': '#C38EC7',
    'Plum4': '#7E587E',
    'Purple': '#8E35EF',
    'Purple1': '#893BFF',
    'Purple2': '#7F38EC',
    'Purple3': '#6C2DC7',
    'Purple4': '#461B7E',
    'Red': '#FF0000',
    'Red1': '#F62217',
    'Red2': '#E41B17',
    'Rosy Brown': '#B38481',
    'Rosy Brown1': '#FBBBB9',
    'Rosy Brown2': '#E8ADAA',
    'Rosy Brown3': '#C5908E',
    'Rosy Brown4': '#7F5A58',
    'Royal Blue': '#2B60DE',
    'Royal Blue1': '#306EFF',
    'Royal Blue2': '#2B65EC',
    'Royal Blue3': '#2554C7',
    'Royal Blue4': '#15317E',
    'Salmon1': '#F88158',
    'Salmon2': '#E67451',
    'Salmon3': '#C36241',
    'Salmon4': '#7E3817',
    'Sandy Brown': '#EE9A4D',
    'Sea Green': '#4E8975',
    'Sea Green1': '#6AFB92',
    'Sea Green2': '#64E986',
    'Sea Green3': '#54C571',
    'Sea Green4': '#387C44',
    'Sienna': '#8A4117',
    'Sienna1': '#F87431',
    'Sienna2': '#E66C2C',
    'Sienna3': '#C35817',
    'Sienna4': '#7E3517',
    'Sky Blue': '#6698FF',
    'Sky Blue2': '#79BAEC',
    'Sky Blue3': '#659EC7',
    'Sky Blue4': '#41627E',
    'Slate Blue': '#737CA1',
    'Slate Blue2': '#6960EC',
    'Slate Blue4': '#342D7E',
    'Slate Gray': '#657383',
    'Slate Gray1': '#C2DFFF',
    'Slate Gray2': '#B4CFEC',
    'Slate Gray3': '#98AFC7',
    'Slate Gray4': '#616D7E',
    'Spring Green': '#4AA02C',
    'Spring Green1': '#5EFB6E',
    'Spring Green2': '#57E964',
    'Spring Green3': '#4CC552',
    'Spring Green4': '#347C2C',
    'Steel Blue': '#4863A0',
    'Steel Blue1': '#5CB3FF',
    'Steel Blue2': '#56A5EC',
    'Steel Blue3': '#488AC7',
    'Steel Blue4': '#2B547E',
    'Thistle': '#D2B9D3',
    'Thistle1': '#FCDFFF',
    'Thistle2': '#E9CFEC',
    'Thistle3': '#C6AEC7',
    'Thistle4': '#806D7E',
    'Turquoise': '#43C6DB',
    'Turquoise1': '#52F3FF',
    'Turquoise2': '#4EE2EC',
    'Turquoise3': '#43BFC7',
    'Violet': '#8D38C9',
    'Violet Red': '#F6358A',
    'Violet Red1': '#F6358A',
    'Violet Red2': '#E4317F',
    'Violet Red3': '#C12869',
    'Violet Red4': '#7D0541',
    'Yellow': '#FFFF00',
    'Yellow Green': '#52D017',
    'Yellow1': '#FFFC17'
}
