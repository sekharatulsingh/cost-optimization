import datetime
import logging
import azure.functions as func
from . import cost, storage

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Billing started")

    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)
    old_records = cost.get_old_records(cutoff_date)

    for record in old_records:
        storage.save_to_blob(record)
        cost.delete_record(record['id'])

    logging.info(f"Archived {len(old_records)} records older than {cutoff_date}")
