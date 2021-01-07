#!/usr/bin/env python
# coding: utf-8

# In[1]:


def generate_days_fn(init_date, final_date):
    
    delta = final_date - init_date       # as timedelta

    target_days = []
    for i in range(delta.days + 1):
        day = init_date + timedelta(days=i)
        target_days.append(day)
    
    return target_days


# In[2]:


def read_INE_trips_date_fn(date_, trips_type='all', flow_type= 'all'):
    date_str= date_.strftime('%Y%m%d')
    df_date= pd.read_csv(os.path.join(data_path, f'{date_str}_maestra_1_mitma_distrito.txt'), 
                             sep='|',dtype={'origen':str, 'destino':str,'fecha':str, 'periodo':str})
    
    if flow_type== 'incoming':
        df_date = df_date[df_date['destino'].isin(target_regions_ids)]
    elif flow_type == 'outgoing':
        df_date = df_date[df_date['origen'].isin(target_regions_ids)]
    elif flow_type== 'all':
        df_date = df_date[(df_date['destino'].isin(target_regions_ids)) |
                          (df_date['origen'].isin(target_regions_ids))]
    
    if trips_type=='inter':
        df_date= df_date[df_date['origen']!=df_date['destino']] #only keep trips between areas
    elif trips_type=='intra':
        df_date= df_date[df_date['origen']==df_date['destino']] #only keep trips within the areas
    
    
    
    #convert period column to a two-digit string
    df_date['periodo'] = df_date['periodo'].apply(lambda x: x.zfill(2))
    df_date= df_date.fillna(0) # set nan as 0
    return df_date

