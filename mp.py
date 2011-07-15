# for another example of this (without the function wrapping), see 
# http://brianglass.wordpress.com/2009/11/29/asynchronous-shell-commands-with-tornado/

# todo, investigate multiprocessing. There's bound to be a better way.

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

    PERFORMANCE NOTE - do not declare your function in the same file as your
    tornado.web handlers. The new process will then need import tornado.web.

    PATH NOTE - I'm not passing shell around, so the path will be whatever
    the directory is in. If you want to pass your python path, do it
    by adding it is an argment to the function, then sys.path.append it.
    The performance impact will be negligable, compared to the massive costs of
    spinning up a whole new interpreter.

    TODO - consider "fork". Is it faster?

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

# Example usage:
import tornado.web, sys, run_func
class _TestHandlerold(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        callback = self.oncallback
        self.clean_up = run_process_async([sys.executable,__file__], callback)

    def oncallback(self, errcode, result):
        self.write(str(errcode)+result)
        self.finish()

    def on_connection_close(self):
        self.clean_up()


class TestHandler(tornado.web.RequestHandler):
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

