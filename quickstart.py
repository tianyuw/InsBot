import os, sys
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

FOLLOW_AMOUNT = 5



if __name__=='__main__':
    args = sys.argv
    insta_username = args[1]
    insta_password = args[2]
    tag_str = args[3]
    follow = args[4]

    tag_list = tag_str.split('_')
    if follow == 'True':
        unfollow_amount = len(tag_list) * FOLLOW_AMOUNT

    session = InstaPy(username=insta_username,
                    password=insta_password,
                    headless_browser=True,
                    nogui=True,
                    multi_logs=True)

    try:
        session.login()

        # settings
        session.set_upper_follower_count(limit=2500)
        session.set_do_comment(True, percentage=30)
        session.set_comments(['aMEIzing!', 'So beautiful!', 'Nicey!'])
        session.set_dont_include(['akaxuan_'])
        session.set_dont_like(['pizza', 'girl'])

        #if follow == 'True':
            # following
            #session.set_do_follow(enabled=True, percentage=20, times=1)
            #session.follow_by_tags(tag_list, amount=FOLLOW_AMOUNT)
            #session.unfollow_users(amount=unfollow_amount, onlyNotFollowMe=True, sleep_delay=60)

        # actions
        #session.set_smart_hashtags(['portrait', 'holiday', 'photography'], limit=1, sort='top', log_tags=True)
        session.like_by_tags(tag_list, amount=30)


    except Exception as exc:
        # if changes to IG layout, upload the file to help us locate the change
        if isinstance(exc, NoSuchElementException):
            file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
            with open(file_path, 'wb') as fp:
                fp.write(session.browser.page_source.encode('utf8'))
            print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
                '*' * 70, file_path))
        # full stacktrace when raising Github issue
        raise

    finally:
        # end the bot session
        session.end()
