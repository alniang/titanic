import time 
from prefect import task, flow
from prefect.logging import get_run_logger
from datetime import timedelta


@task
def wake_up():
    logger = get_run_logger()
    logger.info("Waking up...")
    time.sleep(3)
    logger.info("🔥 Awake now!")
    
@task
def coffee():
    logger = get_run_logger()
    logger.info("Making coffee...")
    time.sleep(2)
    logger.info("☕️ Coffee is ready!")
    
@task
def drink_coffee(log_print=True):
    logger = get_run_logger()
    time.sleep(1)
    logger.info("☕️ Coffee drunk!")
    
    
@flow
def morning_routine():
    logger = get_run_logger()
    logger.info("Drinking coffee...")
    wake_up()
    coffee()
    drink_coffee()

if __name__ == "__main__":
    morning_routine.serve(
        name="🔥 Morning Routine 🔥", 
        )
