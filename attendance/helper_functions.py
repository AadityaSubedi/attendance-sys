
from database import DB
from .models import Subject, Program


def populate_subjects(program: dict) -> dict:
    """
    Populates with subject
    Args:
        program (dict): A program 
    Returns:
        dict: program populated with dict
    """

    semesters = {}
    for key, value in program['semesters'].items():
        semesters[key] = {}
        semesters[key]['subjects'] = list(filter(None, [DB.find_one(
            Subject.collection, {'code': subject}) for subject in value['subjects']]))
    program['semesters'] =semesters

    return program





def populate_programs(level: dict) -> dict:
    """
    Populates with subject
    Args:
        program (dict): A program 
    Returns:
        dict: program populated with dict
    """

    programs  = list(filter(None, [ DB.find_one(
            Program.collection, {'code': program}) for program in  level['programs']]))


    return {**level, 'programs':programs}


