Pyora
=====

Python script to monitor oracle

**Python 2 branch**

Requirements
=====
cx-Oracle==5.1.2

python-argparse

Note:Try installing python-argparse: `easy_install argparse`  or  `yum install python-argarse` on RHEL/Centos.

Tested with python 2.6 and 2.7

Create Oracle user for Pyora usage
=====
<pre><code>
CREATE USER ZABBIX IDENTIFIED BY <REPLACE WITH PASSWORD> DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE TEMP PROFILE DEFAULT ACCOUNT UNLOCK;
GRANT CONNECT TO ZABBIX;
GRANT RESOURCE TO ZABBIX;
ALTER USER ZABBIX DEFAULT ROLE ALL;
GRANT SELECT ANY TABLE TO ZABBIX;
GRANT CREATE SESSION TO ZABBIX;
GRANT SELECT ANY DICTIONARY TO ZABBIX;
GRANT UNLIMITED TABLESPACE TO ZABBIX;
GRANT SELECT ANY DICTIONARY TO ZABBIX;
GRANT SELECT ON V_$SESSION TO ZABBIX;
GRANT SELECT ON V_$SYSTEM_EVENT TO ZABBIX;
GRANT SELECT ON V_$EVENT_NAME TO ZABBIX;
GRANT SELECT ON V_$RECOVERY_FILE_DEST TO ZABBIX;
</code></pre>

Usage
=====
<pre><code>
» python pyora.py                                                                                                    
usage: pyora.py [-h] [--username USERNAME] [--password PASSWORD]
                [--address ADDRESS] [--database DATABASE]
                
                {activeusercount,bufbusywaits,check_active,check_archive,commits,db_close,db_connect,dbfilesize,dbprllwrite,dbscattread,dbseqread,dbsize,dbsnglwrite,deadlocks,directread,directwrite,dsksortratio,enqueue,freebufwaits,hparsratio,indexffs,lastapplarclog,lastarclog,latchfree,logfilesync,logonscurrent,logprllwrite,logswcompletion,netresv,netroundtrips,netsent,query_lock,query_redologs,query_rollbacks,query_sessions,query_temp,rcachehit,redowrites,rollbacks,show_tablespaces,tablespace,tblrowsscans,tblscans,uptime,version}
                ...
pyora.py: error: too few arguments


# Check Oracle version
0: python pyora.py --username pyora --password secret --address 127.0.0.1 --database DATABASE version
Oracle Database 10g Enterprise Edition Release 10.2.0.4.0 - 64bi

# Check Oracle active user count
0: python pyora.py --username pyora --password secret --address 127.0.0.1 --database DATABASE activeusercount
68

# Show the tablespaces names in a JSON format
0: python pyora.py show_tablespaces
{
	"data":[
	{ "{#TABLESPACE}":"ORASDPM"},
	{ "{#TABLESPACE}":"MDS"},
	{ "{#TABLESPACE}":"SOADEV_MDS"},
	{ "{#TABLESPACE}":"ORABAM"},
	{ "{#TABLESPACE}":"SOAINF"},
	{ "{#TABLESPACE}":"DATA"},
	{ "{#TABLESPACE}":"MGMT_AD4J_TS"},
	{ "{#TABLESPACE}":"MGMT_ECM_DEPOT_TS"},
	{ "{#TABLESPACE}":"MGMT_TABLESPACE"},
	{ "{#TABLESPACE}":"RECOVER"},
	{ "{#TABLESPACE}":"RMAN_CAT"},
	{ "{#TABLESPACE}":"SYSAUX"},
	{ "{#TABLESPACE}":"SYSTEM"},
	{ "{#TABLESPACE}":"TEMP"},
	{ "{#TABLESPACE}":"UNDOTBS"},
	{ "{#TABLESPACE}":"VIRTUALCENTER"},
	]
}

# Show a particular tablespace usage in %
0: python pyora.py --username pyora --password secret --address 127.0.0.1 --database DATABASE tablespace SYSTEM
92.45

</code></pre>
