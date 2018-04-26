# -*- coding: utf-8 -*-
import os
import sys
import curses
import traceback
import logging
import logging.handlers
from flask import request
from flask import current_app as app


def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


class LogFormatter(logging.Formatter):
    MOBI_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(mobi_module)s:%(mobi_lineno)d]%(end_color)s %(message)s'
    DEFAULT_FORMAT = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%y%m%d %H:%M:%S'
    DEFAULT_COLORS = {
        logging.DEBUG: 4,  # Blue
        logging.INFO: 2,  # Green
        logging.WARNING: 3,  # Yellow
        logging.ERROR: 1,  # Red
    }

    def __init__(self, color=True, fmt=DEFAULT_FORMAT,
                 datefmt=DEFAULT_DATE_FORMAT, colors=DEFAULT_COLORS):
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt

        self._colors = {}
        if color and _stderr_supports_color():
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = str(fg_color, "ascii")

            for levelno, code in colors.items():
                self._colors[levelno] = str(curses.tparm(fg_color, code), "ascii")
            self._normal = str(curses.tigetstr("sgr0"), "ascii")
        else:
            self._normal = ''

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''

        if record.__dict__.get('mobi_module'):
            formatted = self.MOBI_FORMAT % record.__dict__
        else:
            formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(ln for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


def get_extra():
    f = sys._getframe(3)
    if f is not None:
        f = f.f_back
    rv = "(unknown file)", 0, "(unknown function)", None
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == __file__:
            f = f.f_back
            continue
        rv = (co.co_filename, f.f_lineno, co.co_name)
        break
    module = os.path.splitext(rv[0].split('/src/')[1])[0]

    return dict(mobi_module=module, mobi_lineno=rv[1])


def access(data, flag, show_detail):
    try:
        if 'ticker' in request.url:
            pass
        else:
            req_args = dict(request.args or request.form)
            detailed_args = req_args if show_detail else req_args.keys()
            info('{} {} {} token: {}'.format(
                request.method.upper(), request.path, detailed_args,
                request.headers.get('token', '0' * 10)[-10:])
            )
            info('{} {}'.format(flag, data if show_detail else ''))
    except Exception as detail:
        app.logger.error(detail)
        app.logger.error(traceback.format_exc())


def info(msg):
    app.logger.info('{} {}'.format(get_prefix(), str(msg)[:2000], extra=get_extra()))


def error(msg):
    app.logger.error('{} {}'.format(get_prefix(), str(msg)[:2000], extra=get_extra()))


def debug(msg):
    app.logger.debug('{} {}'.format(get_prefix(), str(msg)[:2000], extra=get_extra()))


def warning(msg):
    app.logger.warning('{} {}'.format(get_prefix(), str(msg)[:2000], extra=get_extra()))


def get_prefix():
    """

    :return:
    """
    # from src.app.handler import get_session
    # session = get_session()
    # cid = request.headers.get("cid", 'empty')
    # ver = request.headers.get('App-Version', 'empty')
    # prefix = get_uid_prefix()
    # mobile = ''
    # if session:
    #     auth = session.get_auth()
    #     mobile = auth.get('mobile')
    # return 'ver[{}] cid:{} mobile:{} {}'.format(ver, cid, mobile, prefix)


def get_uid_prefix():
    """

    :return:
    """
    # from src.app.handler import get_current_user
    # uid = None
    # current_user = get_current_user()
    # if current_user:
    #     uid = current_user.get('user_id', '')
    # return 'uid:None' if not uid else 'uid:{}'.format(uid)
