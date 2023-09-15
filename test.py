# import re
# a = "https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000340.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D906/E6/F186/809f30db-7079-421f-a625-7baa8ec21874.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000341.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D878/E420/F173/04765739-d40f-4d13-b271-8d5f9e5f44bd.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11000342.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D20/E983/F199/866b5059-8fd7-4719-964c-51d2f78675d5.jpghttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D546/E538/F353/ed2464d1-bc28-4790-96cd-5216db2c14f5.JPGhttps://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D814/E111/F733/aed9d34d-890c-49fd-83ca-f76f38e4b94b.jpghttps://www.travel.taipei/streams/sceneadmin/video/100C1.mp3"
# pattern = r"[jJ][pP][gG]*"
# # regex = re.compile(pattern)
# # arr = re.search(pattern, a).groups()
# # arr = re.search(pattern, a)

# # print(arr)

# # arr = re.split(pattern, a)
# # arr = [pattern + url for url in arr]
# # pattern = r"[[jJ][pP][gG]][[pP][nN][gG]]"
# # for url in arr:
# #     url = re.search(pattern, url)
# #     if url
# # print(arr)


# def cut_file_str(id:int, attraction_id:int, urls:str) -> list:
#     pattern = r"https:"
#     arr = re.split(pattern, urls)

#     pattern = r"[jJ][pP][gG]"
#     res = []
#     for url in arr:
#         if len(url) < 3:
#             continue
#         if not re.search(pattern, url[-3:]):
#             continue
#         id += 1
#         res.append((str(id), str(attraction_id), "https:" + url))

#     return id, res


# # cut_file_str(a)

# num, data = cut_file_str(0, 1, a)
# print( num, data )
# # for da in data:
# #     print(da)
# #     da = ", ".join(da)
# #     print(da)

import random
# print(random.randint(1000000000, 9999999999))
for j in range(10):
    ran_set = set()
    repeat = 0
    for i in range(10000000):
        new_int = random.randint(1000000000, 9999999999)
        if new_int in ran_set:
            # print("重複: ", i, "  數值: ", new_int)
            repeat += 1
        ran_set.add(new_int)
    print("重複: ", j, "  次數: ", repeat)
    