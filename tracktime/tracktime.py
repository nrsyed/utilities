import argparse
import datetime
import os
import pickle
from queue import Queue
import threading
import time

# Python utility to track the amount of time you've spent working on something.
# Run script when you start, press Enter in terminal window when you're done.
# Each session (start to end) is stored in a Python pickle file in the form of
# a list of dicts, with each dict corresponding to a session.

# NOTE: Currently supports only Python 3.
# TODO: Documentation and additional functionality.

class Session(threading.Thread):
    """Periodically write log, updated with the current session, to file."""

    def __init__(self, sessions, log_filepath, autosave_timeout, log_lock):
        self.sessions = sessions
        self.log_filepath = log_filepath
        self.autosave_timeout = autosave_timeout
        self.log_lock = log_lock
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            time.sleep(self.autosave_timeout)
            self.save()

    def save(self):
        with self.log_lock:
            self.sessions[-1]["end_time"] = datetime.datetime.now()
            pickle.dump(self.sessions, open(self.log_filepath, "wb"))

def subdivide_sessions_by_date(sessions):
    """
    Check list of sessions for sessions spanning multiple days. Subdivide
    these sessions into several multiple sessions (one per day). Return
    new list.
    """
    updated_sessions = []
    q = Queue()
    for i, session in enumerate(sessions):
        q.put(session)
        while not q.empty():
            sess = q.get()
            if sess["start_time"].day != sess["end_time"].day:
                # Get a datetime object corresponding to the beginning of the
                # day after the session start time by adding a day and setting
                # hour, min, sec, and usec to zero (ie, midnight).
                next_day = ((sess["start_time"] + datetime.timedelta(days=1)
                    ).replace(hour=0, minute=0, second=0, microsecond=0))

                # Make two copies of the current session. sess_first is the
                # part from the start time to the end of the day. sess_next
                # is the part from the beginning of the next day to the end_time.
                sess_first = dict(sess)
                sess_next = dict(sess)

                # Set the end time of sess_first equal to beginning of next day
                # minus one microsecond. Append to new list of sessions.
                sess_first["end_time"] = (next_day - datetime.timedelta(microseconds=1))
                updated_sessions.append(sess_first)

                # Set start time of sess_next equal to beginning of next day.
                # Add to queue.
                sess_next["start_time"] = next_day
                q.put(sess_next)
            else:
                updated_sessions.append(sess)

    return updated_sessions
            
def list_sessions(sessions):
    """Print the list of sessions, each separated by a newline, to terminal."""

    for i, session in enumerate(sessions):
        start_str = "Start: " + session["start_time"].strftime("%x, %X")
        end_str = "End: " + session["end_time"].strftime("%x, %X")
        print("Session {:d}: ".format(i+1) + start_str + " | " + end_str)

def new_session(sessions, log_filepath, autosave_timeout):
    """Begin a new session and add it to the list."""

    # Initialize current session dict start_time and end_time to current time. 
    current_time = datetime.datetime.now()
    current_session = {"start_time": current_time, "end_time": current_time}

    # Append current session to list of sessions.
    sessions.append(current_session)

    log_lock = threading.Lock()

    # If autosave_timeout is 0, no need to start a new thread.
    if autosave_timeout > 0:
        s = Session(sessions, log_filepath, autosave_timeout, log_lock)
        s.start()

    input("[INFO] Session timer started. Press Enter to stop.\n")

    with log_lock:
        sessions[-1]["end_time"] = datetime.datetime.now()
        pickle.dump(sessions, open(log_filepath, "wb"))
    print("[INFO] Session appended to log and written to file.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    default_log_file = "log.pkl"
    ap.add_argument("-f", "--log-filepath", type=str, default=default_log_file,
        help="Path to pickled log file. File will be created if it does not "
            + "exist. Default \"{}\".".format(default_log_file))
    ap.add_argument("-a", "--autosave", type=int, default=1,
        help="How frequently the log file will be autosaved (in minutes) "
            + "while script is running. Default 1; set to 0 for no autosave.")
    ap.add_argument("-l", "--list-sessions", action="store_true",
        help="If this flag is set, the given log file's contents are printed "
            + "to the terminal.")

    args = vars(ap.parse_args())

    # Load or create log pickle file.
    log_filepath = os.path.abspath(args["log_filepath"])
    if not os.path.isfile(log_filepath):
        sessions = []
        pickle.dump(sessions, open(log_filepath, "wb"))
        print("[INFO] Log file {} created.".format(log_filepath))
    else:
        sessions = pickle.load(open(log_filepath, "rb"))
        print("[INFO] Log file {} loaded.".format(log_filepath))

        # Check that list "sessions" was correctly loaded from pickle file.
        if sessions is None or type(sessions) is not type(list()):
            raise RuntimeError("Invalid log file.")

    if args["list_sessions"]:
        list_sessions(sessions)
    else:
        autosave_timeout = 60 * args["autosave"]
        new_session(sessions, log_filepath, autosave_timeout)
