from TeenHope import settings

def get_ck_list(session_str):
    if session_str:
        ck_list = session_str.split(",")
        ck_list = [int(x) for x in ck_list]
    else:
        ck_list = []
    return ck_list

def encode_ck_list(ck_list):
    return ",".join([str(x) for x in ck_list])
