# -*- coding: utf-8 -*-

from celery.schedules import crontab  
from celery.task import task, periodic_task  

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab  
#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))  
#def test():      
#    print "firing test task" 

@task
def test(id):
    print 'Finding day!'
    from models import Day, Entry
    d = Day.objects.get(id=int(id))
    return "Day " + str(d) + ' found!'
    return 'Thank you!'

@task
def parse_entries_task(id):
    from dar.models import Day, Entry
    d = Day.objects.get(id=int(id))
    print 'Beginning parsing of day ' + str(d)
    entries = Entry.objects.filter(day=d)
    for e in entries:
        e.parse_raw_text()
    for e in entries:
        e.calculate_neighbors()
    d.parsed = True
    d.save()
    #from django.core.mail import send_mail
    #send_mail('%s: Catalogação completa!' % str(d.date), 'A catalogação da sessão do dia %s está completa. Agora é só preciso rever e editar! <link>', 'from@example.com',
    #        ['to@example.com'], fail_silently=False)
    return "Day " + str(d) + ' parsed!'


