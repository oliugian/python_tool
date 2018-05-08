# -*- coding: utf-8 -*-
import string
import random


def generate_sign_up_user(user_name, random_password=False):
    """ramdomly generate a user to sign up

    Args:
        random_password (bool, optional): use uniform password or specific password
    """
    # user name

    # mail box
    prefix = string.digits + string.lowercase
    postfix = ['@outlook.com', '@gmail.com', '@hotmail.com', '@foxmail.com']
    prefix_len = random.randint(5, 12)
    mail = ''
    for i in xrange(prefix_len):
        mail += random.choice(prefix)
    mail_box = mail + random.choice(postfix)

    # password
    if random_password:
        candidates = string.digits + string.letters + '_@'
        passwd = ''
        for i in xrange(random.randint(7, 17)):
            passwd += random.choice(candidates)
    else:
        passwd = 'ScutAmazon1234$'
    sign_up_form = {'customerName': user_name, 'email': mail_box, 'password': passwd, 'passwordCheck': passwd}
    return sign_up_form



