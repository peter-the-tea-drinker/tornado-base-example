# for another example of this (without the function wrapping), see 
# http://brianglass.wordpress.com/2009/11/29/asynchronous-shell-commands-with-tornado/

def run_process_async(executable_args, callback, input_str=None, path=None):
    """I wonder what happens if you call this with itself as an argument?
    """
    from subprocess import Popen, PIPE
    from tornado.ioloop import IOLoop
    import sys
    ioloop = IOLoop.instance()
    #p = subprocess.Popen([sys.executable,__file__,'!!!!!!!!!!!'],
    #                          stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if path is not None:
        env={"PATH": "/usr/bin"}
    else:
        env = {}
    p = Popen(executable_args, stdin=PIPE, stderr=PIPE, stdout=PIPE, env=env)
    if input_str:
        p.stdin.write(input_str)
    p.stdin.close()

    def on_read(fd, events):
        err_code = p.poll()
        if err_code is not None:
            ioloop.remove_handler(p.stdout.fileno())
            # send error messages from the child's errr pipe to sys.stderr
            traceback = p.stderr.read()
            p.stderr.close()
            sys.stderr.write(traceback)
            # get the result
            result_str = p.stdout.read()
            p.stdout.close()
            # run the callback
            callback(err_code, result_str)
    
    ioloop.add_handler(p.stdout.fileno(), on_read, IOLoop.READ)

    def clean_up():
        ioloop.remove_handler(p.stdout.fileno())
        if p.poll() is None:
            p.kill()
    return clean_up

def run_async_func(func, callback, on_error, nice=0, max_CPU_time=-1,
                   *args, **kwargs):
    '''Magic fairy dust, which you can sprinkle over fairly arbitrary (i.e.
    pickleable) functions to make them run in a separate process, then asyncronously 
    get the result (which is automatically unpickled).

    The cost is, that the function runs in a new process. On a 2GHz C2Duo with
    SSD HDD, this may cost ~40ms, plus the cost of reimporting libraries (smtplib 
    takes ~20ms, a big library can take a lot longer).

    If you want to write your own functions to use here, make sure they can be
    called fast. For example, don't make sure *they* can be imported without 
    importing too many unneeded things.

    Given how slow this is (What, no free lunch?), why would you use it?
    If the function you are calling is blocking, but you don't have an
    asyncronous version (as would be the case for a lengthy db query, or 
    sending email), then this saves you re-writing the function.
    Even if the function is not blocking, it will mean Tornado doesn't block
    on *other* users, who might also be waiting.

    However, keep in mind, it's not ideal, due to the overhead of creating a
    whole new process, and importing the libraries again.
    '''
    import cPickle, inspect, os, sys
    path = os.path.dirname(inspect.getfile(func))
    input_str = cPickle.dumps((func, args, kwargs), cPickle.HIGHEST_PROTOCOL)

    def unpickle_callback(errcode, result_str):
        try:
            result = cPickle.loads(result_str)
        except:
            sys.stderr.write( 'Error uncpickling '+result_str+' errcode = '+str(errcode) )
            raise
        if errcode:
            on_error(result)
        else:
            callback(result)

    clean_up = run_process_async([sys.executable,'run_func.py',
        str(int(nice)),str(int(max_CPU_time))], 
        unpickle_callback, input_str = input_str, path = path)
    return clean_up

# TODO - for the subprocess, should we limit CPU use via:
# os.nice(10)
# resource.setrlimit(resource.RLIMIT_CPU, (60,60))

import sys
if __name__ in '__main__' :

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
    '''
    import sys

    
    print 'waiting'
    import time
    import pickle
    p = pickle.dumps(pickle.dumps)
    t=time.time()
    import sys
    import cPickle
    import smtplib
    sys.stderr.write('Chatchatcah\n')
    import time
    #print (time.time()-t)*1000
    #time.sleep(3)
    #print 'result!'
    '''

else:
 if not len(sys.argv) == 4:
    import tornado.web, sys, run_func
    class TestHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
            callback = self.oncallback
            self.clean_up = run_process_async([sys.executable,__file__], callback)

        def oncallback(self, errcode, result):
            self.write(str(errcode)+result)
            self.finish()

        def on_connection_close(self):
            self.clean_up()


    class TestHandler2(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
            import time
            callback = self.oncallback
            onerror = self.onerror
            #self.write('<div>please wait <p>'+time.ctime()+'</div>')
            #self.flush()
            self.t0=time.time()
            self.clean_up = run_async_func(run_func.test_func, callback, onerror)

        def oncallback(self, result):
            import time
            self.write(str(result))
            self.write('<p>That took '+str((time.time()-self.t0)*1000)+'ms')
            self.finish()

        def onerror(self, result):
            self.write('Error!\n')

            self.write(str(type(result))+'\n')
            self.write(str(result)+'\n')
            self.finish()

        def on_connection_close(self):
            self.clean_up()


'''import tornado.web
import tornado.ioloop

class SubprocessHandler(tornado.web.RequestHandler):
    def start_subprocess(self, executable_args, callback):
        from subprocess import Popen, PIPE
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.subprocess = Popen(executable_args, stdout=PIPE)
        self.ioloop.add_handler(self.subprocess.stdout.fileno(), self.on_read,
                tornado.ioloop.IOLoop.READ)
        self.outputs = []
        self.callback = callback

    def on_read(self, fd, events):
        self.outputs.append(self.subprocess.stdout.read())
        print self.outputs[-1]
        errcode = self.subprocess.poll()
        if errcode is not None:
            self.ioloop.remove_handler(self.subprocess.stdout.fileno())
            self.callback(errcode, self.outputs)


class TestHandler(SubprocessHandler):
    @tornado.web.asynchronous
    def get(self):
        import sys
        self.start_subprocess((sys.executable,__file__),self.my_callback)

    def my_callback(self, errcode, outputs):
        self.write(str(errcode))
        for line in outputs:
            self.write(line)
        self.finish()

def make_(function, ):
'''



'''
if __name__ == '__main__':

    import sys
    #len(sys.argv)
    #import inspect
    #this_file = inspect.currentframe().f_code.co_filename
    if len(sys.argv) == 1:
        import subprocess
        import os.path
        import tornado
        import time
        import sys
        n=time.time()
        #ioloop = tornado.ioloop.IOLoop.instance()
        #print __file__
        p = subprocess.Popen([sys.executable,__file__,'!!!!!!!!!!!'],
                              stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        print (time.time()-n)*1000,'ms'
        stdout = p.stdout
        stdin = p.stdin
        stdin.write('hihihi\n')
        stdin.close()
        print (time.time()-n)*1000,'ms'
        #stdin.flush()
        #time.sleep(1)
        print stdout.read(),
        stdout.close()
        print (time.time()-n)*1000,'ms'
        #stdin.flush()
        #stdout.flush()
        #print 'called!',stdout.fileno()
        #print stdout.readline()
        #stdin.write('hi')
        
        #for l in p.stdout:
        #    print `l`
        #time.sleep(3)
        #stdin.close()
        #p.wait()
        #stdin.write('hihi')
        #print `p.stdout.read()`
    else:
        import time
        import sys
        import smtplib
        s = sys.stdin.read()
        print s+'done'
        sys.stdout.flush()'''
