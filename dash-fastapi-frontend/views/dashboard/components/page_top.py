import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html
from config.env import ApiConfig
from utils.cache_util import CacheManager
from datetime import datetime
import random

current_hour = datetime.now().hour
greeting = "早安" if current_hour < 12 else "下午好" if current_hour < 18 else "晚上好"
random_sentences = [
    "逐梦星辰，无悔青春",
    "仰望星空，脚踏实地，心怀家国，矢志航天",
    "以航天精神为指引，在追梦路上不断前行，为科技强国之梦添砖加瓦",
    "航天梦，中国梦，追梦的脚步永不停歇，向着梦想不断远航",
    "矢志不渝，筑梦星辰大海",
    "星空浩瀚无比，探索永无止境",
    "怀揣不懈追求的航天梦，敢于战胜一切艰难险阻，勇于攀登航天科技高峰",
    "探索浩瀚宇宙，发展航天事业，建设航天强国，是我们不懈追求的航天梦",
    "你心中星河灿烂, 脚下征途漫漫",
    "追梦人的伟大之处在于，梦想就是他们奋斗的动力，梦想的味道就是奋斗的味道",
    "仰望星空，脚踏实地",
    "航天精神，勇于探索，敢为人先",
]


def render_page_top():
    return html.Div(
        [
            html.Div(
                fac.AntdAvatar(
                    id='dashboard-avatar-info',
                    mode='image',
                    src=f"{ApiConfig.BaseUrl}{CacheManager.get('user_info').get('avatar')}"
                    if CacheManager.get('user_info').get('avatar')
                    else '/assets/imgs/profile.jpg',
                    size='large',
                ),
                className='avatar',
            ),
            html.Div(
                [
                    html.Div(
                        fac.AntdText(
                            f"{greeting}，{CacheManager.get('user_info').get('nick_name')}，{random.choice(random_sentences)}！"
                        ),
                        className='content-title',
                    ),
                    html.Div(
                        f"{CacheManager.get('user_info').get('role')[0].get('role_name')}|"
                        f"{CacheManager.get('user_info').get('dept').get('dept_name')}-"
                        f"登录时间：{CacheManager.get('user_info').get('login_date')}",
                        style={
                            'color':'grey'
                        }
                    ),
                ],
                className='content',
            ),
            html.Div(
                [
                    # html.Div(
                    #     fac.AntdStatistic(title='项目数', value=56),
                    #     className='stat-item',
                    # ),
                    # html.Div(
                    #     fac.AntdStatistic(
                    #         title='团队内排名', value=8, suffix='/ 24'
                    #     ),
                    #     className='stat-item',
                    # ),
                    # html.Div(
                    #     fac.AntdStatistic(title='项目访问', value=2223),
                    #     className='stat-item',
                    # ),
                ],
                className='extra-content',
            ),
            fuc.FefferyStyle(
                rawStyle="""
                    .page-header-content {
                        display: flex;
                    }

                    .page-header-content .avatar {
                        flex: 0 1 72px;
                    }

                    .page-header-content .avatar > span {
                        display: block;
                        width: 72px;
                        height: 72px;
                        border-radius: 72px;
                    }

                    .page-header-content .content {
                        position: relative;
                        top: 4px;
                        margin-left: 24px;
                        line-height: 22px;
                        color: rgba(0,0,0,.45);
                        flex: 1 1 auto;
                    }

                    .page-header-content .content .content-title {
                        margin-bottom: 12px;
                        font-size: 20px;
                        font-weight: 500;
                        line-height: 28px;
                        color: rgba(0,0,0,.85);
                    }

                    .extra-content {
                        float: right;
                        white-space: nowrap;
                    }

                    .extra-content .stat-item {
                        position: relative;
                        display: inline-block;
                        padding: 0 32px;
                    }

                    .extra-content .stat-item > p:first-child {
                        margin-bottom: 4px;
                        font-size: 14px;
                        line-height: 22px;
                        color: rgba(0,0,0,.45);
                    }

                    .extra-content .stat-item > p {
                        margin: 0;
                        font-size: 30px;
                        line-height: 38px;
                        color: rgba(0,0,0,.85);
                    }

                    .extra-content .stat-item > p > span {
                        font-size: 20px;
                        color: rgba(0,0,0,.45);
                    }

                    .extra-content .stat-item::after {
                        position: absolute;
                        top: 8px;
                        right: 0;
                        width: 1px;
                        height: 40px;
                        background-color: #e8e8e8;
                        content: '';
                    }

                    .extra-content .stat-item:last-child {
                        padding-right: 0;
                    }

                    .extra-content .stat-item:last-child::after {
                        display: none;
                    }
                    """
            ),
        ],
        className='page-header-content',
        style={
            'padding': '12px',
            'marginBottom': '24px',
            # 'boxShadow': 'rgba(0, 0, 0, 0.1) 0px 4px 12px',
        },
    )
