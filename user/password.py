import string
from random import choice
from pprint import pprint
import logging


def trois_element(element):
    if len(element) > 3:
        return element[:3]

    else:
        return element
if __name__=='__main__':
    element = trois_element('mamadou')
    print(element)