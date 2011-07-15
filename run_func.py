def test_func():
    import resource
    import time
    import bcrypt
    time.sleep(1)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return ('this func cost about '+str(int(usage[0]*1000))+'ms user time, '+
            str(int(usage[1]*1000))+'ms system, totalling '+
            str(int((usage[0]+usage[1])*1000))+'ms.')

if __name__ in '__main__' :
    import sys
    max_CPU_time = int(sys.argv[-1])
    nice = int(sys.argv[-2])

    if max_CPU_time > 0:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (max_CPU_time,max_CPU_time))
    if nice > 0:
        import os
        os.nice(nice)

    # note, this *won't* be the case when you unpickle
    # the test function above - creating a weird bug.

    import cPickle
    stdout = sys.stdout
    sys.stdout = sys.stderr # don't let chatty programs mess up my pickles!
    input_str = sys.stdin.read()

    try:
        func, args, kwargs = cPickle.loads(input_str)
        result = func(*args, **kwargs)
        result_s = cPickle.dumps(result)
    except Exception, E:
        try:
            result_s = cPickle.dumps(E)
        except PicklingError, PE:
            result_s = cPickle.dumps(str(E)+'and unable to pickle exception '+str(PE))
        raise E
    finally:
        stdout.write(result_s)

