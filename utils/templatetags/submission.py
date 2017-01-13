# coding=utf-8
import json
from django import template
from utils.signal2str import strsignal


def translate_result(value):
    results = {
        0: "Accepted",
        1: "Runtime Error",
        2: "Time Limit Exceeded",
        3: "Memory Limit Exceeded",
        4: "Compile Error",
        5: "Format Error",
        6: "Wrong Answer",
        7: "System Error",
        8: "Waiting"
    }
    return results[value]


def translate_signal(value):
    if not value:
        return ""
    else:
        return strsignal(value)

def get_memory(value):
    try:
        memory = json.loads(value)[0]['memory'] / 1024 / 1024
        return memory
    except:
        return '-'

def translate_language(value):
    return {1: "C", 2: "C++", 3: "Java"}[value]


def translate_result_class(value):
    if value == 0:
        return "success"
    elif value == 8:
        return "info"
    return "danger"


register = template.Library()
register.filter("translate_result", translate_result)
register.filter("translate_language", translate_language)
register.filter("translate_result_class", translate_result_class)
register.filter("translate_signal", translate_signal)
register.filter("get_memory", get_memory)
