# -*- coding: utf-8 -*-
import functools


# 不带参数的装饰器
def raptor_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
        # if not REPORT_STAT:
        #     return func(*args, **kwargs)

        # t = Cat.new_transaction(t_type, t_name)
        # try:
        #     return func(*args, **kwargs)
        # except CUSTOM_ERROR:  # 自定义异常不向cat上报
        #     # t.set_status_for_exception(e)
        #     raise
        # except Exception as e:  # 除自定义异常外的其他异常上报到cat
        #     t.set_status_for_exception(e)
        #     if report_args:  # 上报参数
        #         t.add_data("args: {0}, {1}".format(args, kwargs))
        #     raise
        # finally:
        #     t.complete()

    return wrapper


# 带参数的装饰器
def raptor_stat(t_type, t_name, report_args=True):
    """
    上报cat/raptor
    :param t_type: 类型
    :param t_name: 名称
    :param report_args: 是否上报接口/函数参数
    :return:
    """
    def raptor_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            # if not REPORT_STAT:
            #     return func(*args, **kwargs)

            # t = Cat.new_transaction(t_type, t_name)
            # try:
            #     return func(*args, **kwargs)
            # except CUSTOM_ERROR:  # 自定义异常不向cat上报
            #     # t.set_status_for_exception(e)
            #     raise
            # except Exception as e:  # 除自定义异常外的其他异常上报到cat
            #     t.set_status_for_exception(e)
            #     if report_args:  # 上报参数
            #         t.add_data("args: {0}, {1}".format(args, kwargs))
            #     raise
            # finally:
            #     t.complete()

        return wrapper

    return raptor_decorator
