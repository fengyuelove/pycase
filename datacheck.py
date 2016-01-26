#!/usr/lib/env python2.7
# -*- coding:utf-8 -*-
import mysql.connector
from email.header import Header
from email.mime.text import MIMEText
import smtplib
from datetime import datetime

# 邮件配置
from_addr = 'noreply@lianjia.com'
password = "***"
to_addr = ('fengyue@lianjia.com', 'wangxiaofei@lianjia.com', 'zhubaiyang@lianjia.com', 'jinsanpu@lianjia.com',
           'dongjinyong@lianjia.com', 'wanghaoyu@lianjia.com', 'xsy@lianjia.com', 'helichun@lianjia.com')
# to_addr = ('fengyue@lianjia.com')
smtp_server = 'smtp.exmail.qq.com'

ucConfigs = {
    'host': '***',
    'port': '***',
    'user': "***",
    'password': '***',
    'database': '***'
}

# 数据校验sql
# 校验同店组多名商圈经理
store_manager_check = ('SELECT user_code, user_name, org_code, org_name, position_code, name '
                       'FROM user_org_position '
                       'LEFT JOIN uc_city ON user_org_position.office_address = uc_city.city_code '
                       'WHERE org_code IN '
                       '(SELECT org_code FROM user_org_position '
                       'WHERE position_code = 765 AND user_record = 0 AND position_status = 1 '
                       'GROUP BY org_code HAVING  count(*) > 1) '
                       'AND  user_org_position.position_status = 1 '
                       'AND user_org_position.user_record = 0 '
                       'AND user_org_position.position_code = 765 '
                       'ORDER BY office_address, org_code;')
# 只有兼岗没有主岗
position_check = ('SELECT user_code, user_name, org_code, org_name, position_code, name '
                  'FROM user_org_position LEFT JOIN uc_city ON user_org_position.office_address = uc_city.city_code '
                  'WHERE user_record != 0 AND user_code NOT IN '
                  '(SELECT user_code FROM user_org_position WHERE user_record = 0 AND position_status = 1) '
                  'AND user_org_position.position_status = 1 GROUP BY user_code ORDER BY office_address, org_code;')

conn = mysql.connector.connect(**ucConfigs)
cursor = conn.cursor()
content = u'<html><body><font style="color: red">数据正确性关乎UC服务质量和技术口碑,望大家认真对待!</font>'


def _create_table_html(sql, title):
    cursor.execute(sql)
    results = cursor.fetchall()
    html = u'<div><h3 style="color: red">' \
           + title.decode('utf-8') + u'</h3>' \
                                     u'<table><tr><th>工号</th><th>姓名</th><th>组织编号</th><th>组织名称</th><th>职位编码</th><th>城市</th></tr>'
    for row in results:
        html += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % row
    html += "</table></div>"
    return html


content += _create_table_html(store_manager_check, '同店组存在多名有效商圈经理')
content += _create_table_html(position_check, '主岗位缺失的在职员工')
content += "</body></html>"

# 邮件发送部分
# def _format_addr(s):
#     name, addr = parseaddr(s)
#     return formataddr(( \
#         Header(name, 'utf-8').encode(), \
#         addr.encode('utf-8') if isinstance(addr, unicode) else addr))

msg = MIMEText(content, 'html', 'utf-8')
msg['From'] = from_addr
msg['To'] = ','.join(to_addr)
msg['Subject'] = Header(u'用户中心数据质量日报', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
# server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
print '%s数据日报邮件发送成功' % datetime.now().strftime("%y-%m-%d %H:%m")
