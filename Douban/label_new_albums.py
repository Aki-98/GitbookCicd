from const_albums import *
from const_common import *
from douban import URL_SEARCH_ALBUM

import re
from playwright.sync_api import sync_playwright


# def search_and_restore_csc_open_tapd_jira():
#     results_tapd = search_csc_jira(filter=FILTER.BUGS_TAPD_OPEN)
#     total = get_total(results_tapd)
#     if 0 == total:
#         logger.warning(
#             "%s: %s",
#             TAG.SEARCH_AND_RESTORE_CSC_OPEN_TAPD_JIRA,
#             "no csc open tapd jira found, skipping..",
#         )
#         return None
#     else:
#         logger.info(
#             "%s: %s", TAG.SEARCH_AND_RESTORE_CSC_OPEN_TAPD_JIRA, f"found {total} jira"
#         )

#     json_csc = {}
#     json_csc[CSC.OPEN_TAPDS] = []
#     issues_tapd = get_issues(results_tapd)
#     for issue_tapd in issues_tapd:
#         jira_id = get_key(issue_tapd)
#         logging.info(
#             "%s: %s", TAG.SEARCH_AND_RESTORE_CSC_OPEN_TAPD_JIRA, "jira_id: " + jira_id
#         )
#         field_trd_party_link = get_trd_party(issue_tapd)
#         logging.info(
#             "%s: %s",
#             TAG.SEARCH_AND_RESTORE_CSC_OPEN_TAPD_JIRA,
#             "field_trd_party_link: " + field_trd_party_link,
#         )
#         tapd_link = format_tapd_bug(extract_tapd_id(field_trd_party_link))
#         jira_data = {}
#         jira_data[CSC.JIRA_ID] = jira_id
#         jira_data[CSC.TAPD_LINK] = tapd_link
#         json_csc[CSC.OPEN_TAPDS].append(jira_data)
#     write_json_to_file(
#         file_all_path=FILE_DATA_CSC.format(time=current_file_time),
#         json_data=json_csc,
#     )
#     return json_csc


# def run_playwright(page, url):
#     try:
#         # url = jira_data[CSC.TAPD_LINK]
#         # logger.info("%s: %s", TAG.RUN_PLAYWRIGHT, "url: " + url)
#         page.goto(url)
#         comment_wrap = page.wait_for_selector(
#             r'//div[@id="comments_status_wrap"]', timeout=60000
#         )
#         comment_area = comment_wrap.query_selector(r'//div[@id="comment_area"]')
#         comments_elements = comment_area.query_selector_all("> div")
#         comments_value = {}
#         csc_id = jira_data[CSC.JIRA_ID]
#         logger.info(
#             "%s: %s",
#             TAG.RUN_PLAYWRIGHT,
#             f"csc_id: {csc_id}",
#         )
#         comments_value[csc_id] = []
#         for index, child_element in enumerate(comments_elements):
#             element_field_time = child_element.query_selector(".field-time")
#             time = element_field_time.text_content()
#             timestamp = convert_to_timestamp(
#                 time, tz=TIME_ZONE_SHANGHAI, format=FORMAT_JIRA_TAPD_TIME
#             )
#             logger.info(
#                 "%s: %s",
#                 TAG.RUN_PLAYWRIGHT,
#                 f"tapd_timestamp: {timestamp} last_udpate_timestamp: {last_update_timestamp}",
#             )
#             if timestamp < last_update_timestamp:
#                 logger.warning(
#                     "%s: %s",
#                     TAG.RUN_PLAYWRIGHT,
#                     "tapd_timestamp is early then last_update_timestamp, skipping",
#                 )
#                 continue
#             element_field_author = child_element.query_selector(".field-author")
#             author = element_field_author.text_content()
#             if USER_CNUX == author:
#                 logger.warning(
#                     "%s: %s",
#                     TAG.RUN_PLAYWRIGHT,
#                     "comment reporter is cnux, skipping",
#                 )
#                 continue
#             element_comment_text = child_element.query_selector(".comment_type_text")
#             comment = element_comment_text.text_content().lstrip().rstrip()
#             value_dict = {}
#             value_dict[TAPD.AUTHOR] = author
#             value_dict[TAPD.TIME] = time
#             value_dict[TAPD.COMMENT] = comment
#             comments_value[jira_data[CSC.JIRA_ID]].append(value_dict)
#         return comments_value
#     except Exception as e:
#         logger.info("%s: %s", TAG.EXCEPTION, e)




def search_albums(context,album_name):
    search_page = context.pages[0]
    search_page.goto(URL_SEARCH_ALBUM % album_name)
    search_result = search_page.wait_for_selector(r'//*[@id="content"]/div/div[1]/div[3]/div', timeout=60000) 
    result_list = search_result.query_selector_all(".result")
    target = 1
    for result_item in result_list:
        result_subject_list = result_item.query_selector_all(".subject-cast")
        print(f"{target}.{result_subject_list[0].text_content()}")
        target += 1
    target = (int)(input("Please input the sequence of target album:"))
    target_result_item = result_list[target-1]
    target_album_a_list = target_result_item.query_selector_all("a")
    target_album_a_list[0].click()
    album_page = context.pages[1]
    info = album_page.wait_for_selector(r'#info', timeout=60000)
    print(album_page)
    info_text = info.text_content()
    # Get Time
    published_year = re.match(TIME, info_text)
    print(published_year)
    # Get Area
    
def select_label_type():
    return
    
#         comments_value = {}

if __name__ == "__main__":
    # 输入序号选择本批Album的Genre，或输入英文找寻匹配的Genre，或程序自动匹配Genre
    select_label_type()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(
            "ws://localhost:7666/devtools/browser/0887c8cd-be5d-4b40-bdd2-e26d1a0811f1"
        )
        context = browser.contexts[0]
        while True:
            album_name = input("Please input album name:")
            album_name = "pygmallon"
            search_albums(context,album_name)
        browser.close()
    # return
    # 1.选择Album页
    # search_albums()
    # 3.展示result_list
    # 4.选择result_list
    # 5.label album 时代自动化 genre按照一开始定义的 国家 按artiest介绍
    # # 2.查询CSC系统中目前还OPEN的tapd相关的BUG
    # json_csc = search_and_restore_csc_open_tapd_jira()
    # # 3.爬取相应的Comment
    # json_tapd = search_and_restore_tapd_comments(json_csc)
    # # 4.在CSC Jira Center更新Comment
    # comment_on_csc(json_tapd)
    # # 5.更新时间戳
    # update_timestamp()
