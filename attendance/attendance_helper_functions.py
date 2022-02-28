import json
from platform import python_branch
from database import DB
from collections import defaultdict


# def populate_subjects(program: dict) -> dict:
#     """
#     Populates with subject
#     Args:
#         program (dict): A program 
#     Returns:
#         dict: program populated with dict
#     """

#     semesters = {}
#     for key, value in program['semesters'].items():
#         semesters[key] = {}
#         semesters[key]['subjects'] = list(filter(None, [DB.find_one(
#             Subject.collection, {'code': subject}) for subject in value['subjects']]))
#     program['semesters'] =semesters

#     return program





# def populate_programs(level: dict) -> dict:
#     """
#     Populates with subject
#     Args:
#         program (dict): A program 
#     Returns:
#         dict: program populated with dict
#     """

#     programs  = list(filter(None, [ DB.find_one(
#             Program.collection, {'code': program}) for program in  level['programs']]))


#     return {**level, 'programs':programs}

import traceback
from werkzeug.wsgi import ClosingIterator

class AfterResponse:
    def __init__(self, app=None):
        self.callbacks = []
        if app:
            self.init_app(app)

    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback

    def init_app(self, app):
        # install extension
        app.after_response = self

        # install middleware
        app.wsgi_app = AfterResponseMiddleware(app.wsgi_app, self)

    def flush(self):
        for fn in self.callbacks:
            try:
                fn()
            except Exception:
                traceback.print_exc()

class AfterResponseMiddleware:
    def __init__(self, application, after_response_ext):
        self.application = application
        self.after_response_ext = after_response_ext

    def __call__(self, environ, after_response):
        iterator = self.application(environ, after_response)
        try:
            return ClosingIterator(iterator, [self.after_response_ext.flush])
        except Exception:
            traceback.print_exc()
            return iterator


def countDays(attendance):
    all_attendees = list()
    for attendees_list in attendance.values():
        for attendee in attendees_list:
            all_attendees.append(attendee)
    all_attendees.sort()

    all_attendees.sort()
    working_days = defaultdict(int)
    for attendee in all_attendees:
        working_days[attendee] += 1
    return dict(working_days)






