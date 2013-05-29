Pyora
=====

Python script to monitor oracle

Requirements
=====
cx-Oracle==5.1.2

Tested with python 2.6 and 2.7

Usage
=====
First setup the access to a Oracle database on pyora.py

<pre><code>
username = 'pyora'
password = 'pyora'
address  = '127.0.0.1'
database = 'master'
</pre></code>

<pre><code>
0: python pyora.py 
usage: pyora.py [-h]
                
                 {dbseqread,version,lastapplarclog,tblscans,indexffs,bufbusywaits,logswcompletion,netresv,redowrites,logonscurrent,netroundtrips,directread,directwrite,rollbacks,logfilesync,lastarclog,dbfilesize,dbsnglwrite,dsksortratio,netsent,commits,uptime,enqueue,hparsratio,tablespace,check_active,rcachehit,activeusercount,logprllwrite,dbscattread,deadlocks,tblrowsscans,latchfree,dbprllwrite,show_tablespaces,dbsize,freebufwaits}
                      ...
                pyora.py: error: too few arguments

# Check Oracle version
0: python pyora.py version
Oracle Database 10g Enterprise Edition Release 10.2.0.4.0 - 64bi

# Check Oracle active user count
0: python pyora.py activeusercount
68

# Show the tablespaces usage in MB
0: python pyora.py show_tablespaces
('ORASDPM', 307)
('MDS', 102)
('ORABAM', 205)
('SOAINFRA', 7168)
('DATA', 9216)
('MGMT_AD4J_TS', 205)
('MGMT_EDEPOT_TS', 41)
('MGMT_TSPACE', 1382)
('RECOVER', 205)
('RMAN_CAT', 102)
('SYSAUX', 717)
('SYSTEM', 1024)
('UNDOTBS', 614)

# Show a particular tablespace usage in %
0: python pyora.py tablespace SYSTEM
92.45

</code></pre>