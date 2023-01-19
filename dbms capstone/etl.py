import logging as log
import numpy as np
import pandas as pd
import sys
import os
import mysql.connector
import random, string

def read_excel(excel_path:str):
   
   try:
    excel = pd.ExcelFile(excel_path)
   except Exception as e:
    log.error('Please Enter a valid File Path.')
    log.error(e)
    sys.exit('\n Please Enter a valid File Path.')
   
   log.info('>>>Extracting data from file <<<<')

   order_df = pd.read_excel(excel,'Orders')
   people_df = pd.read_excel(excel,'People')
   returns_df = pd.read_excel(excel,'Returns')

   #check colums if possible

   #processing extracted data

   returns_df = returns_df.where(returns_df['Returned'] == 'Yes').reset_index(drop=True)

   log.info('>>> Extraction completed <<<<')
   
   return order_df, people_df, returns_df

def get_country_details(df):
   return pd.DataFrame({
      'country_name': df['Country/Region'].unique() 
      })

def get_customer_segment_details(df):
   return pd.DataFrame({
      'segment_name': df['Segment'].unique() 
      })

def get_shipping_mode_details(df):
   return pd.DataFrame({
      'shipping_mode_name': df['Ship Mode'].unique() 
      })

def get_category_details(df):
   return pd.DataFrame({
      'category_name': df['Category'].unique() 
      })

def get_region_details(df):
   temp = pd.DataFrame({
      'region_name': df['Region'],
      'country_name': df['Country/Region']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_sub_category_details(df):
   temp = pd.DataFrame({
      'sub_category_name': df['Sub-Category'],
      'category_name': df['Category']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_state_details(df):
   temp = pd.DataFrame({
      'state_name': df['State'],
      'region_name': df['Region']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_regional_manager_details(df):
   temp = pd.DataFrame({
      'manager_name': df['Regional Manager'],
      'region_name': df['Region']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_product_details(df):
   temp = pd.DataFrame({
      'product_id': df['Product ID'],
      'product_name': df['Product Name'],
      'sub_category_name': df['Sub-Category']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_city_details(df):
   temp = pd.DataFrame({
      'postal_code': df['Postal Code'],
      'city_name': df['City'],
      'state_name': df['State']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_customer_details(df):
   temp = pd.DataFrame({
      'customer_id': df['Customer ID'],
      'customer_name': df['Customer Name'],
      'customer_segment_name': df['Segment']
   }) 
   return temp.drop_duplicates().reset_index(drop=True)

def get_order_details(df,return_df):
   temp = pd.DataFrame({
      'order_id': df['Order ID'],
      'order_date': df['Order Date'],
      'shipping_date': df['Ship Date'],
      'shipping_mode_name': df['Ship Mode'],
      'customer_id': df['Customer ID'],
      'postal_code': df['Postal Code'],
      'returned': None,
   }) 

   temp['returned'] = temp['order_id'].isin(returns_df['Order ID']).astype(int)

   return temp.drop_duplicates().reset_index(drop=True)

def get_sales_details(df):
   temp = pd.DataFrame({
      'total_sale': df['Sales'],
      'order_id': df['Order ID'],
      'product_id': df['Product ID'],
      'quantity': df['Quantity'],
      'discount': df['Discount'],
      'profit': df['Profit'],
   })
   return temp.drop_duplicates().reset_index(drop=True)

class Data:
   def __init__(self, order_df, people_df, returns_df):

     self.country_details = get_country_details(order_df)
     self.customer_segment_details = get_customer_segment_details(order_df)
     self.shipping_mode_details = get_shipping_mode_details(order_df)
     self.category_details = get_category_details(order_df)

     self.region_details = get_region_details(order_df)
     self.sub_category_details = get_sub_category_details(order_df)

     self.state_details = get_state_details(order_df)
     self.regional_manager_details = get_regional_manager_details(people_df)
     self.product_details = get_product_details(order_df)

     self.city_details = get_city_details(order_df)

     self.customer_details = get_customer_details(order_df)

     self.order_details = get_order_details(order_df,returns_df)
     
     self.sales_details = get_sales_details(order_df)

def insert_country_details(db:mysql.connector.MySQLConnection, country_details:pd.DataFrame):

   query = '''INSERT INTO `country_details`
               (`country_name`)
               VALUES
               (%s);'''
   
   cursor = db.cursor()

   params = [(country_details['country_name'][i],) for i in country_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `country_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `country_details` table.')
      log.error(e)

def insert_customer_segment_details(db:mysql.connector.MySQLConnection, segment_details:pd.DataFrame):

   query = '''INSERT INTO `customer_segment_details`
               (`segment_name`)
               VALUES
               (%s);'''
   
   cursor = db.cursor()

   params = [(segment_details['segment_name'][i],) for i in segment_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `customer_segment_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `customer_segment_details` table.')
      log.error(e)

def insert_shipping_mode_details(db:mysql.connector.MySQLConnection, shipping_mode_details:pd.DataFrame):

   query = '''INSERT INTO `shiping_mode_details`
               (`shipping_mode_name`)
               VALUES
               (%s);'''
   
   cursor = db.cursor()

   params = [(shipping_mode_details['shipping_mode_name'][i],) for i in shipping_mode_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `shiping_mode_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `shiping_mode_details` table.')
      log.error(e)

def insert_category_details(db:mysql.connector.MySQLConnection, category_details:pd.DataFrame):

   query = '''INSERT INTO `category_details`
               (`category_name`)
               VALUES
               (%s);'''
   
   cursor = db.cursor()

   params = [(category_details['category_name'][i],) for i in category_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `category_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `category_details` table.')
      log.error(e)

def insert_region_details(db:mysql.connector.MySQLConnection, region_details:pd.DataFrame):

   query = '''INSERT INTO `region_details`
               (`region_name`,
               `country_id`)
               VALUES
               (%s,
               (SELECT `country_id` from `country_details` where `country_name` = %s));
               '''
   
   cursor = db.cursor()

   params = [(region_details['region_name'][i],region_details['country_name'][i]) for i in region_details.index]
   
   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `region_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `region_details` table.')
      log.error(e)

def insert_sub_category_details(db:mysql.connector.MySQLConnection, sub_category_details:pd.DataFrame):

   query = '''INSERT INTO `sub_category_details`
               (`sub_category_name`,
               `category_id`)
               VALUES
               ( %s,
               (SELECT `category_id` FROM `category_details` where `category_name` = %s ));
               '''
   
   cursor = db.cursor()

   params = [(sub_category_details['sub_category_name'][i], sub_category_details['category_name'][i]) for i in sub_category_details.index]
   
   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `sub_category_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `sub_category_details` table.')
      log.error(e)

def insert_state_details(db:mysql.connector.MySQLConnection, state_details:pd.DataFrame):

   query = '''INSERT INTO `state_details`
               (`state_name`,
               `region_id`)
               VALUES
               ( %s,
               (SELECT `region_id` from `region_details` where `region_name` = %s));
               '''
   
   cursor = db.cursor()

   params = [(state_details['state_name'][i], state_details['region_name'][i]) for i in state_details.index]
   
   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `state_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `state_details` table.')
      log.error(e)

def insert_regional_manager_details(db:mysql.connector.MySQLConnection, regional_manager_details:pd.DataFrame):

   query = '''INSERT INTO `regional_manager_details`
               (`manager_name`,
               `region_id`)
               VALUES
               ( %s,
               (SELECT `region_id` FROM `region_details` where `region_name` = %s));
               '''
   
   cursor = db.cursor()

   params = [(regional_manager_details['manager_name'][i], regional_manager_details['region_name'][i]) for i in regional_manager_details.index]
   
   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `regional_manager_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `regional_manager_details` table.')
      log.error(e)

def insert_product_details(db:mysql.connector.MySQLConnection, product_details:pd.DataFrame):

   query = '''INSERT INTO `product_details`
               (`product_id`,
               `product_name`,
               `sub_category_id`)
               VALUES
               ( %s,
               %s,
               (SELECT `sub_category_id` FROM `sub_category_details` WHERE `sub_category_name` = %s));
               '''
   
   cursor = db.cursor()

   #print('+++++ See this ++++ ',sum(k>1 for k in product_details['product_id'].value_counts().to_list()))

   params = [(product_details['product_id'][i], product_details['product_name'][i],product_details['sub_category_name'][i]) for i in product_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `product_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `product_details` table.')
      log.error(e)

def insert_city_details(db:mysql.connector.MySQLConnection, city_details:pd.DataFrame):

   query = '''INSERT INTO `city_details`
               (`postal_code`,
               `city_name`,
               `state_id`)
               VALUES
               ( %s,
               %s,
               (SELECT `state_id` FROM `state_details` WHERE `state_name` = %s ));
               '''

   cursor = db.cursor()

   params = [(int(city_details['postal_code'][i]), city_details['city_name'][i], city_details['state_name'][i]) for i in city_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `city_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `city_details` table.')
      log.error(e)

def insert_customer_details(db:mysql.connector.MySQLConnection, customer_details:pd.DataFrame):

   query = '''INSERT INTO `customer_details`
               (`customer_id`,
               `customer_name`,
               `segment_id`)
               VALUES
               ( %s,
               %s,
               (SELECT `segment_id` FROM `customer_segment_details` WHERE `segment_name` = %s));'''

   cursor = db.cursor()

   params = [(customer_details['customer_id'][i], customer_details['customer_name'][i], customer_details['customer_segment_name'][i])
    for i in customer_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `customer_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `customer_details` table.')
      log.error(e)

def insert_order_details(db:mysql.connector.MySQLConnection, order_details:pd.DataFrame):

   query = '''INSERT INTO `order_details`
               (`order_id`,
               `order_date`,
               `shipping_date`,
               `shipping_mode_id`,
               `customer_id`,
               `postal_code`,
               `returned`)
               VALUES
               (%s,
               %s,
               %s,
               (SELECT `shipping_mode_id` FROM `shiping_mode_details` WHERE `shipping_mode_name` = %s),
               %s,
               %s,
               %s);
               '''

   cursor = db.cursor()

   # print('+++++ See this ++++ ',sum(k>1 for k in order_details['order_id'].value_counts().to_list()))

   order_details['order_date'] = order_details['order_date'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
   order_details['shipping_date'] = order_details['shipping_date'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

   params = [(order_details['order_id'][i], order_details['order_date'][i], order_details['shipping_date'][i],
               order_details['shipping_mode_name'][i], order_details['customer_id'][i], int(order_details['postal_code'][i]), 
               int(order_details['returned'][i])) 
               for i in order_details.index]

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `order_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `order_details` table.')
      log.error(e)

def insert_sales_details(db:mysql.connector.MySQLConnection, sales_details:pd.DataFrame):

   query = '''INSERT INTO `sales_details`
               (
               `total_sale`,
               `order_id`,
               `product_id`,
               `quantity`,
               `discount`,
               `profit`)
               VALUES
               (
               %s,
               %s,
               %s,
               %s,
               %s,
               %s);
               '''

   cursor = db.cursor()

   params = [(float(sales_details['total_sale'][i]), sales_details['order_id'][i], sales_details['product_id'][i],
               int(sales_details['quantity'][i]), float(sales_details['discount'][i]),float(sales_details['profit'][i])) 
               for i in sales_details.index]
   

   try:
      cursor.executemany(query,params)
      db.commit()
      log.info(f'===> %s rows inserted into `sales_details` table.',cursor.rowcount)
   except Exception as e:
      log.error('Error inserting data into `sales_details` table.')
      log.error(e)


def load_data_to_tables(db:mysql.connector.MySQLConnection, data:Data):

   insert_country_details(db, data.country_details)
   insert_customer_segment_details(db, data.customer_segment_details)
   insert_shipping_mode_details(db, data.shipping_mode_details)
   insert_category_details(db, data.category_details)

   insert_region_details(db, data.region_details)
   insert_sub_category_details(db, data.sub_category_details)

   insert_state_details(db, data.state_details)
   insert_regional_manager_details(db, data.regional_manager_details)
   insert_product_details(db, data.product_details)

   insert_city_details(db, data.city_details)

   insert_customer_details(db, data.customer_details)

   insert_order_details(db, data.order_details)
     
   insert_sales_details(db, data.sales_details)


if __name__ == '__main__':
    
    path = os.path.dirname(__file__)
    log.basicConfig(filename=path+'\etl.log', level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    log.info('==== ETL Pipeline Starts ====')
   
    order_df, people_df, returns_df = read_excel('C:\\Users\\harpr\\Documents\\Data\\George Brown College\\GBC_Level1\\4002_Foundations of Data Management\\Lab Exercises\\Lab Exercise_2\\Draft_3\\Sample - Superstore.xls')
   #  order_df, people_df, returns_df = read_excel(input('Path to the data : \n\t'))
   
    log.info('>>>>>Transforming data to required formats<<<<<')
    data = Data(order_df, people_df, returns_df)
    log.info('>>>>>Transformation Completed<<<<<')

    log.info('Connecting to DB')

    db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='gbc_superstore'
            )

    if db != None:
      log.info('>>>>>> DB Connection Successful <<<<<<<<<<<')
      log.info('>>>>>>>>>>>>Loading Data into tables<<<<<<<<<<<<<')
      load_data_to_tables(db,data)
      log.info('>>>>>>>>>>>>>>Loading COMPLETED<<<<<<<<<<<<<<<<')
    else:
      log.error('DB connection Failed. Exiting.')

    log.info('XXXXXXXXXXXXXXXXXX === PIPELINE ENDS === XXXXXXXXXXXX')

    