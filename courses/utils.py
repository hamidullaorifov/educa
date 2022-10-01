


def duration_formatting(duration):
        hour = int(duration/3600)
        minutes = int(duration)%3600//60
        seconds = int(duration)%60
        f=''
        if hour:
            f+=f'{hour} h '
        if minutes:
            f+=f'{minutes} m '
        if seconds:
            f+=f'{seconds} s'

        return f


# def incr_course_orders(pk):
#     order = Course._modules_latest_orders.get(str(pk),0)
#     order+=1
#     Course._modules_latest_orders[str(pk)]=order
# def decr_course_orders(pk):
#     order = Course._modules_latest_orders.get(str(pk))
#     order-=1
#     Course._modules_latest_orders[str(pk)]=order
# def incr_module_orders(pk):
#     order = Module._contents_latest_orders.get(str(pk),0)
#     order+=1
#     Module._contents_latest_orders[str(pk)]=order
# def incr_module_orders(pk):
#     order = Module._contents_latest_orders.get(str(pk),0)
#     order+=1
#     Module._contents_latest_orders[str(pk)]=order
