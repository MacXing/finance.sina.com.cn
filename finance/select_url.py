import pymysql

def serch_url():
    conn = pymysql.connect(host="192.168.160.36", user="root",
                           password="gzxiaoi", db="crawler", charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT url FROM finance WHERE url is not NULL"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # for result in results:
        #     print(result[0])
        urls=[result[0] for result in results]
        for url in urls:
            if 'finance.sina.com' not in url:
                print(url)
        # print(urls)
    except:
        print('no url')
    cursor.close()
    conn.close()
    return urls

if __name__ == '__main__':
    serch_url()