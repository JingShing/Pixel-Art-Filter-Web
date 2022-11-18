# bind listen port and ip
bind = '0.0.0.0:5000' 
# Multiprocessing, recommend max cpu core*2+1
workers = 4
# wait for client need to service. Maxinum is 2048, which is maxinum connection num.
backlog = 2048
# sync, gevent,meinheld  
# working mode, default is sync, this set as gevent
worker_class = "gevent"  
# maxinum client number
max_requests = 2000
# working in background.
daemon = True
# When code edit restart workers.
reload = True
# keep-alive wait second default is 2 secs. Usually set on 1-5 secs.           
# It is how long we need to listen and break connection. Unit is second.
keepalive = 5
# set pid file name
pidfile = './gunicore.pid'
# debug error warning error critical
loglevel = 'info' 
# Accessing log path and name
accesslog = str('gunicorn_acess.log')
errorlog  = str('gunicorn_error.log')
# log format
access_log_format = '%({X-Real-IP}i)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'