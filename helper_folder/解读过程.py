import openai

from helper_folder.数据库表格 import NewsData, TestOnly

key3 = "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"
openai.api_key = key3

def test_thread(num,db):
    model = "gpt-3.5-turbo"
    message = [{"role": "user", "content": f"帮我算个数{num}*2+1"}]
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0.5,
        messages=message,
    )
    ai_answer = response['choices'][0]['message']['content']

    to_add = TestOnly(
        id = num,
        test_result = num*2+1,
        ai_response = ai_answer
    )
    db.session.add(to_add)

    db.session.commit()


def total_process(complete, test_version,db):
    ##################################################参数设定
    ##测试范围确定
    if complete == "1":
        test_news = NewsData.query.all()
    else:
        test_news = NewsData.query.filter(NewsData.test_version > test_version).all()

    ###开始解读每一条新闻
    ###多进程环节
    for test_new in test_news:
        test_thread(test_new.id,db)

    return 0
