from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError
import time
class Command(BaseCommand):

    def handle(self, *args , **options):
        
        self.stdout.write("Waiting for database ....")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
                self.stdout.write(self.style.SUCCESS("Connected to Database"))
            except Psycopg2OpError as e :
                self.stdout.write(f" {e} : Failed to connect : Retrying after 1 sec ...")
                self.stdout.write("Psycopg2 Error")
                time.sleep(1)
            except OperationalError as e :
                self.stdout.write(f" {e} : Failed to connect : Retrying after 1 sec ...")
                self.stdout.write("Operational Error")
                time.sleep(1)
           
                