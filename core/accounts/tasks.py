from celery import shared_task
import time

@shared_task
def sendEmail():
    time.sleep(3)
    print("send email is done")
    