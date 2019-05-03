#!/usr/bin/env python
#peer_helper.py
from image_helper import *
#these utilities were created by Donald Brant, ART350, spring 2019
#-------------------------------------------------------------------------------
def blue_channel(image):
    '''
    Args:
        image (numpy.ndarray): BGR image as an ndarray
    Returns:
        numpy.ndarray: the input BGR ndarray image with the green and red values zeroed out
    '''
    blue = image.copy()
    blue[:, :, 1] = 0
    blue[:, :, 2] = 0
    return blue
#-------------------------------------------------------------------------------
def green_channel(image):
    '''
    Args:
        image (numpy.ndarray): BGR image as an ndarray
    Returns:
        numpy.ndarray: the input BGR ndarray image with the blue and red values zeroed out
    '''
    green = image.copy()
    green[:, :, 0] = 0
    green[:, :, 2] = 0
    return green
#-------------------------------------------------------------------------------
def red_channel(image):
    '''
    Args:
        image (numpy.ndarray): BGR image as an ndarray
    Returns:
        numpy.ndarray: the input BGR ndarray image with the blue and green values zeroed out
    '''
    red = image.copy()
    red[:, :, 0] = 0
    red[:, :, 1] = 0
    return red
#-------------------------------------------------------------------------------
def rgb_offset(image,bluexshift,blueyshift,greenxshift,greenyshift,redxshift,redyshift):
    '''
    Args:
        image (numpy.ndarray): BGR image as an ndarray
        bluexshift (int): the blue channel x offset in pixels
        blueyshift (int):  the blue channel y offset in pixels
        greenxshift (int):  the green channel x offset in pixels
        greenyshift (int):  the green channel y offset in pixels
        redxshift (int):  the red channel x offset in pixels
        redyshift (int):  the red channel y offset in pixels
    Returns:
        numpy.ndarray: the input BGR ndarray image with the BGR color channels offset according to the input arguments
    '''
    blue = shift_image(blue_channel(image),bluexshift,blueyshift)
    green = shift_image(green_channel(image),greenxshift,greenyshift)
    red = shift_image(red_channel(image),redxshift,redyshift)
    out_img = image.copy()
    out_img[:, :, 0] = blue[:, :, 0]
    out_img[:, :, 1] = green[:, :, 1]
    out_img[:, :, 2] = red[:, :, 2]
    return out_img
#-------------------------------------------------------------------------------
