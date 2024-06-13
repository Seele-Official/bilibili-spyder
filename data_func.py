import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体 (SimHei) 来支持中文
plt.rcParams['axes.unicode_minus'] = False
def create_Dressphoto(pendants, top):
    count_series = pd.Series(pendants).value_counts().head(top)
    tick_label = ["NO Dress" if i=='' else i for i in count_series.index]
    values = count_series.values
    plt.figure(figsize=(12, 6))
    plt.bar(tick_label, values, tick_label=tick_label)


    plt.title(f'Top {top} Most Frequent Dress Name')
    plt.xlabel('Dress')
    plt.ylabel('Frequency')


    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')



    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.savefig('Dress.png', bbox_inches='tight')
    plt.show()
def create_uidphoto(uids, top:int):

    count_series = pd.Series(uids).value_counts().head(top)


    def mask_number(number):
        return 'UID:' + number[:2] + '****' + number[-2:]


    masked_labels = [mask_number(num) for num in count_series.index]
    values = count_series.values


    plt.figure(figsize=(12, 6))
    plt.bar(masked_labels, values, tick_label=masked_labels)


    plt.title(f'Top {top} Most Frequent UID (Masked)')
    plt.xlabel('UID')
    plt.ylabel('Frequency')


    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')



    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.savefig('UID.png', bbox_inches='tight')
    plt.show()
def create_timephoto(timestamps, start_date, end_date, unit):
    # unit：'2H'（每2小时）'D'（每日）或 'M'（每月）
    # start_date = '2024-05-27'
    # end_date = '2024-05-29'

    dates = [datetime.fromtimestamp(int(ts)) for ts in timestamps]
    df = pd.DataFrame({'date': dates})



    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')


    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask].copy()


    filtered_df['count'] = 1
    filtered_df.set_index('date', inplace=True)
    count_series = filtered_df['count'].resample('H').sum().fillna(0)  # 以小时为单位的统计

    
    user_choice = unit  


    resampled_data = count_series.resample(user_choice).sum()


    plt.figure(figsize=(12, 6))
    plt.plot(resampled_data.index, resampled_data.values, marker='o', linestyle='-')


    for x, y in zip(resampled_data.index, resampled_data.values):
        plt.text(x, y, str(y), fontsize=12, ha='right', va='bottom')


    if user_choice[1] == 'H':
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.HourLocator(interval=int(user_choice[0])))
    elif user_choice[1] == 'D':
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=int(user_choice[0])))
    elif user_choice[1] == 'M':
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=int(user_choice[0])))

    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Timestamp Counts from {} to {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.savefig('Time.png', bbox_inches='tight')
    plt.tight_layout()

    # 显示图形
    plt.show()

def create_levelphoto(data:eval):
    labels = list(data.keys())
    values = list(data.values())


    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, tick_label=labels)


    plt.title('Bilibili Level Counts')
    plt.xlabel('Level')
    plt.ylabel('Count')


    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')


    plt.tight_layout() 
    plt.savefig('Level.png', bbox_inches='tight')
    plt.show()