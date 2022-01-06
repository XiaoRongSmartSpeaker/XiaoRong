import logging
import sys
import requests
import schedule
import time
import threading
import logger.logger as logger

# set up logger
try:
    import logger
    logger = logger.get_logger(__name__)
except ModuleNotFoundError:
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

speaker_name = ''
server_url = ''

def clear_log():
    # send_log_to_server()
    open('log/smartspeaker.log', 'w').close()
    logger.debug("Log file cleared")

def send_log_to_server():
        payloads = {'speaker_name': speaker_name}
        try:
            response = requests.get(server_url, params=payloads, timeout=10)
            response.raise_for_status()
            logger.debug("Successfully sent log file to server")
        except requests.exceptions.HTTPError as errh:
            logger.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error(errc)
        except requests.exceptions.Timeout as errt:
            logger.error(errt)
        except requests.exceptions.RequestException as err:
            logger.error(err)

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# Stop the background thread
def stop_log_manager():
    stop_run_continuously.set()
    logger.debug("Log manager has been stopped")

# Start the background thread (upon importing this module)
stop_run_continuously = run_continuously()

# for production, uncomment this line
# schedule.every().hour.do(clear_log)

# for test only
if __name__ == '__main__':
    schedule.every(10).seconds.do(clear_log)
    for i in range(10):
        time.sleep(1)
        print("hello world!")
    stop_run_continuously.set()