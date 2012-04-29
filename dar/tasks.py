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
    print 'Starting task'
    from dar.models import Day, Entry
    d = Day.objects.get(id=int(id))
    print 'Getting entries from ' + str(d)
    entries = Entry.objects.filter(day=d)
    print 'Beginning parsing'
    for e in entries:
        e.parse_raw_text()
    print 'Calculating neighbors'
    for e in entries:
        e.calculate_neighbors()
    print 'Setting parse state'
    d.parsed = True
    print 'Saving'
    d.save()
    print 'Done!'
    return "Day " + str(d) + ' parsed!'


