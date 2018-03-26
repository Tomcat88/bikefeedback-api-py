
def periodic(scheduler, delay, action, actionargs=()):
    scheduler.enter(delay, 1, periodic, (scheduler, delay, action, actionargs))
    action(*actionargs)
