#coding=utf-8
_date_ = '2019/6/29 9:10'
import requests
import pandas as pd
class ZhiHu():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        }
        #json接口的url
        self.json_url = 'https://www.zhihu.com/api/v4/topics/19552832/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset=0'
        self.auther_url = 'https://www.zhihu.com/people/{}/activities'

        #条数控制器
        self.t = 0

        #创建标题
        title = {'title': ' 标题', 'answer': '回答', 'author_name': '用户名', 'authr_info': '简介', 'author_url': '用户主页',
             'comment_count': '评论数', 'voteup_count': '赞同数'}
        dataframe = pd.DataFrame(title, index=[0])
        dataframe.to_csv('知乎PythonTOP50.csv', index=False, header=False)

    def get_next_url(self,res_json):
        """
        翻页的url
        :param res_json: 获取的json数据
        :return: url
        """
        next_url = res_json['paging']['next']
        self.get_json(next_url)



    def get_json(self,url):
        """
        做递归 判断条件 当爬取数据大于50条的时候停止循环
        :param url:json_url
        :return:
        """
        if self.t>=50:
            return
        response_json = requests.get(url=url, headers=self.headers).json()
        self.get_item(response_json)
        self.get_next_url(response_json)


    def get_item(self,res_json):
        """
        对 json进行解析,并调用写入函数
        :param res_json: response
        :return:
        """
        for i in res_json['data']:
            item = dict()
            #文章题目
            try:
                item['title'] = i['target']['question']['title']
            except:
                item['title'] = i['target']['title']
            #回答答案
            answer = i['target']['excerpt']
            answer = answer.replace('\n','')
            answer = answer.replace('</b>', '')
            answer = answer.replace('<b>', '')
            item['answer'] = answer
            #回答者名字
            item['author_name'] = i['target']['author']['name']
            #回答者简介
            item['authr_info'] = i['target']['author']['headline']
            #作者url
            item['author_url'] = self.auther_url.format(i['target']['author']['url_token'])
            #评论数
            item['comment_count'] = i['target']['comment_count']
            #点赞数
            item['voteup_count'] = i['target']['voteup_count']
            #条件判断器
            self.t+=1
            #x写入表格中
            self.into_csv(item)
            print(item)

    def into_csv(self,items):
        dataframe = pd.DataFrame(items, index=[0])
        # #将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv("知乎PythonTOP50.csv", header=False, index=False, mode='a')

    def run(self):
        self.get_json(self.json_url)

if __name__ == '__main__':
    z = ZhiHu()
    z.run()