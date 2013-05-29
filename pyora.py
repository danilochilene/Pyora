#!/usr/bin/env python
# coding: utf-8

import argparse,cx_Oracle
import inspect

username = 'pyora'
password = 'pyora'
address  = '127.0.0.1'
database = 'master'

con = cx_Oracle.connect('''{0}/{1}@{2}/{3}'''.format(username,password,address,database))
cur = con.cursor()

def bytes2human(n):
  '''
  http://code.activestate.com/recipes/578019
  >>> bytes2human(10000)
  '9.8K'
  >>> bytes2human(100001221)
  '95.4M'
  '''
  symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
  prefix = {}
  for i, s in enumerate(symbols):
    prefix[s] = 1 << (i+1)*10
  for s in reversed(symbols):
    if n >= prefix[s]:
      value = float(n) / prefix[s]
      return '%.1f%s' % (value, s)
  return '%sB' % n

class Checks(object):

	def check_active(self):
	  sql = "select to_char(case when inst_cnt > 0 then 1 else 0 end,'FM99999999999999990') retvalue from (select count(*) inst_cnt from v$instance where status = 'OPEN' and logins = 'ALLOWED' and database_status = 'ACTIVE')"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)

	  for i in res:
	      print i[0]

	def rcachehit(self):
	  sql = "SELECT to_char((1 - (phy.value - lob.value - dir.value) / ses.value) * 100, 'FM99999990.9999') retvalue \
	            FROM   v$sysstat ses, v$sysstat lob, \
	                   v$sysstat dir, v$sysstat phy \
	            WHERE  ses.name = 'session logical reads' \
	            AND    dir.name = 'physical reads direct' \
	            AND    lob.name = 'physical reads direct (lob)' \
	            AND    phy.name = 'physical reads'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)

	  for i in res:
	      print i[0]

	def dsksortratio(self):
	  sql = "SELECT to_char(d.value/(d.value + m.value)*100, 'FM99999990.9999') retvalue \
	             FROM  v$sysstat m, v$sysstat d \
	             WHERE m.name = 'sorts (memory)' \
	             AND d.name = 'sorts (disk)'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)

	  for i in res:
	      print i[0]

	def activeusercount(self):
	  sql = "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null \
	             and status='ACTIVE'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)

	  for i in res:
	      print i[0]

	def activeusercount(self):
	  sql = "select to_char(count(*)-1, 'FM99999999999999990') retvalue from v$session where username is not null"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)

	  for i in res:
	      print i[0]

	def dbsize(self):
	  sql = "SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), 'FM99999999999999990') retvalue \
	             FROM sys.dba_tablespaces d, \
	             (select tablespace_name, sum(bytes) bytes from dba_data_files group by tablespace_name) a, \
	             (select tablespace_name, sum(bytes) bytes from dba_free_space group by tablespace_name) f \
	             WHERE d.tablespace_name = a.tablespace_name(+) AND d.tablespace_name = f.tablespace_name(+) \
	             AND NOT (d.extent_management like 'LOCAL' AND d.contents like 'TEMPORARY')"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print bytes2human(int(i[0]))

	def dbfilesize(self):
	  sql = "select to_char(sum(bytes), 'FM99999999999999990') retvalue from dba_data_files"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print bytes2human(int(i[0]))

	def version(self):
	  sql = "select banner from v$version where rownum=1"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def uptime(self):
	  sql = "select to_char((sysdate-startup_time)*86400, 'FM99999999999999990') retvalue from v$instance"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def commits(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user commits'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def rollbacks(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'user rollbacks'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def deadlocks(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'enqueue deadlocks'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def redowrites(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'redo writes'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def tblscans(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scans (long tables)'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def tblrowsscans(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'table scan rows gotten'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def indexffs(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'index fast full scans (full)'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def hparsratio(self):
	  sql = "SELECT to_char(h.value/t.value*100,'FM99999990.9999') retvalue \
	             FROM  v$sysstat h, v$sysstat t \
	             WHERE h.name = 'parse count (hard)' \
	             AND t.name = 'parse count (total)'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def netsent(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes sent via SQL*Net to client'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def netresv(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'bytes received via SQL*Net from client'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def netroundtrips(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'SQL*Net roundtrips to/from client'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def logonscurrent(self):
	  sql = "select to_char(value, 'FM99999999999999990') retvalue from v$sysstat where name = 'logons current'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]
	  
	def lastarclog(self):
	  sql = "select to_char(max(SEQUENCE#), 'FM99999999999999990') retvalue from v$log where archived = 'YES'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def lastapplarclog(self):
	  sql = "select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') retvalue \
	             from v$loghist lh, v$archived_log al \
	             where lh.SEQUENCE# = al.SEQUENCE# and applied='YES'"

	def freebufwaits(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'free buffer waits'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def bufbusywaits(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'buffer busy waits'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def logswcompletion(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file switch completion'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def logfilesync(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file sync'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def logprllwrite(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'log file parallel write'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def enqueue(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'enqueue'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def dbseqread(self):
	  sql = "select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file sequential read'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def dbscattread(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file scattered read'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def dbsnglwrite(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file single write'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def dbprllwrite(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'db file parallel write'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def directread(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'direct path read'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def directwrite(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'direct path write'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]

	def latchfree(self):
	  sql="select to_char(time_waited, 'FM99999999999999990') retvalue \
	             from v$system_event se, v$event_name en \
	             where se.event(+) = en.name and en.name = 'latch free'"
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[0]
	
	def tablespace(self, name):
	  sql = '''SELECT df.tablespace_name "TABLESPACE", ROUND ( (df.bytes - SUM (fs.bytes)) * 100 / df.bytes, 2) "USADO" FROM sys.sm$ts_free fs, (  SELECT tablespace_name, SUM (bytes) bytes FROM sys.sm$ts_avail GROUP BY tablespace_name) df WHERE fs.tablespace_name(+) = df.tablespace_name and df.tablespace_name = '{0}' GROUP BY df.tablespace_name, df.bytes ORDER BY 1'''.format(name)
	  cur.execute(sql)
	  res = cur.fetchmany(numRows=3)
	  for i in res:
	    print i[1]

	def show_tablespaces(self):
		'''List tablespace names, and size in MB'''
		sql = "SELECT tablespace_name, ROUND(bytes/1024000) MB FROM dba_data_files ORDER by 1";
		cur.execute(sql)
		res = cur.fetchmany(numRows=15)
		for i in res:
			print i

class Main(Checks):
    def __init__(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        for name in dir(self):
            if not name.startswith("_"):
                p = subparsers.add_parser(name)
                method = getattr(self, name)
                argnames = inspect.getargspec(method).args[1:]
                for argname in argnames:
                    p.add_argument(argname)
                p.set_defaults(func=method, argnames=argnames)
        self.args = parser.parse_args()

    def __call__(self):
        a = self.args
        callargs = [getattr(a, name) for name in a.argnames]
        return self.args.func(*callargs)

if __name__ == "__main__":
    main = Main()
    main()
    con.close()
