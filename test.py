import time
search_result = {}
search_slot = {'terminate': False, 'progress': ["a", "b", "c"], 'num': 0}
search_result['id1'] = {"key": "abc",
                        "slot": search_slot,
                        "status": False,
                        "starting_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                        "mode": '1'}
progress = search_result['id1']["slot"]["progress"]
search_result.pop("id1")
print(progress)
