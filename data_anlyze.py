import json

import data_func

# 等级 粉丝牌子 时间趋势 总人数 评论次数

if __name__ == '__main__':
    timestamps = []
    member = []
    pendants = []
    UID_Eval = {}
    level = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    }


    filename ='comment'
    with open(f'./store/{filename}.json','r') as f:
        data = json.loads(f.read())['data']
    
    for reply in data:
        
        for reply_rpeply in reply['replies']:
            timestamps.append(reply_rpeply['ctime'])
            member.append(reply_rpeply['member']['mid'])
            UID_Eval[reply_rpeply['member']['mid']] = {
                'pendant' :reply_rpeply['member']['pendant']['name'],
                'level' :reply_rpeply['member']['level_info']['current_level']
            }

        member.append(reply['member']['mid'])
        timestamps.append(reply['ctime'])
        UID_Eval[reply['member']['mid']] = {
                'pendant' :reply['member']['pendant']['name'],
                'level' :reply['member']['level_info']['current_level']
            }
    for i in UID_Eval:
        pendants.append(UID_Eval[i]['pendant'])
        level[UID_Eval[i]['level']] +=1
    
    start_date = '2024-04-27'
    end_date = '2024-05-01'
    unit = '3H'

    data_func.create_timephoto(timestamps=timestamps, start_date=start_date, end_date=end_date, unit=unit)
    data_func.create_uidphoto(member, 20)
    data_func.create_Dressphoto(pendants, 20)
    total = 0
    L = {}

    for i in level:
        L[str(i)] = level[i]
        total += level[i]
    L['Total'] = total
    level = L
    data_func.create_levelphoto(level)
            
            