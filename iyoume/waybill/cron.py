# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="rasmadeus@gmail.com"
__date__ ="$Jul 16, 2014 11:02:53 PM$"

from django_cron import CronJobBase, Schedule
class OldWaybillsKiller(CronJobBase):

    
    schedule = Schedule(run_every_mins=1440)
    code = 'iyoume.waybill.cron.OldWaybillsKiller'    # a unique code


    def do(self):
        from iyoume.waybill.models import Waybill
        Waybill.remove_old_waybills()