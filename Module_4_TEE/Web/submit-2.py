import time
import subprocess
from requests import post

# xor oldIv old message -> 2d62657063654e7c746262707674622f
    # https://gchq.github.io/CyberChef/#recipe=From_Hex('None')XOR(%7B'option':'Latin1','string':'%3Cstart_messages%3E'%7D,'Standard',false)To_Hex('None',0)&input=MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTE

    # message 2880ccda64f655478e053e178a2b4caf

    # https://gchq.github.io/CyberChef/#recipe=From_Hex('None')XOR(%7B'option':'Latin1','string':'%3Cstart_cmd%3E%3C!--%20'%7D,'Standard',false)To_Hex('None',0)&input=MmQ2MjY1NzA2MzY1NGU3Yzc0NjI2MjcwNzY3NDYyMmY
    # new iv 111111111111111f19065c4c57594f0f
    # iv2 004f5b4c0e003d5c0c5f40505654420f
    # iv3 0f4206145e472919000440501249400f
    # iv4 0d404a4e5f4a3d081510162f15190611

    # message 111111111111111f19065c4c57594f0f2880ccda64f655478e053e178a2b4caf004f5b4c0e003d5c0c5f40505654420f2880ccda64f655478e053e178a2b4caf0f4206145e472919000440501249400f2880ccda64f655478e053e178a2b4caf0d404a4e5f4a3d081510162f151906112880ccda64f655478e053e178a2b4caf

    # sha256 068eee42167b2ff8fa1bd0bac4f4941bbefe917390618b819b681ddb01d61711

    # mes 068eee42167b2ff8fa1bd0bac4f4941bbefe917390618b819b681ddb01d61711111111111111111f19065c4c57594f0f2880ccda64f655478e053e178a2b4caf004f5b4c0e003d5c0c5f40505654420f2880ccda64f655478e053e178a2b4caf0f4206145e472919000440501249400f2880ccda64f655478e053e178a2b4caf0d404a4e5f4a3d081510162f151906112880ccda64f655478e053e178a2b4caf

    # https://gchq.github.io/CyberChef/#recipe=From_Hex('None')SHA2('256',64,160)&input=MTExMTExMTExMTExMTExZjE5MDY1YzRjNTc1OTRmMGYyODgwY2NkYTY0ZjY1NTQ3OGUwNTNlMTc4YTJiNGNhZjAwNGY1YjRjMGUwMDNkNWMwYzVmNDA1MDU2NTQ0MjBmMjg4MGNjZGE2NGY2NTU0NzhlMDUzZTE3OGEyYjRjYWYwZjQyMDYxNDVlNDcyOTE5MDAwNDQwNTAxMjQ5NDAwZjI4ODBjY2RhNjRmNjU1NDc4ZTA1M2UxNzhhMmI0Y2FmMGQ0MDRhNGU1ZjRhM2QwODE1MTAxNjJmMTUxOTA2MTEyODgwY2NkYTY0ZjY1NTQ3OGUwNTNlMTc4YTJiNGNhZg



COMMAND_RUN = 'sh /home/isl/t2/run.sh'

headers = {'Content-Type':'application/xml'}

url_admin = 'http://127.0.0.1:37200/admin'
url_hello = 'http://127.0.0.1:37200/hello'
url_gets  = 'http://127.0.0.1:37200/gets'
url_store = 'http://127.0.0.1:37200/store'

d_admin_init = 'admin$00000000001636920594242$003575c066c711913e0b95b65aa1a9810c4726af722fc9a27974845a36ffb5aa4011111111111111111111111111111111af4a445d5bfee31c1fba656aefb089f112117264ee42ae55001f1d1a3bc561787439810809ab69fa140077db71232044813b626b53623b6d1a2fbc22f65f12eadfb7a4bc563719c11e063b744f5f91f9c412272ce5af58fbeace9d7862a3c1de8cbb695293a6fe76bf77e9493ad8eab1'
d_admin_stop = 'admin$00000000001636920605589$00023e67314ec1ac80c7df2ee1f2c5cecb019df64c3362d198236aa68d363a10c911111111111111111111111111111111af4a445d5bfee31c1fba656aefb089f1fcd61d26f3a5c0b85aa902e80032ad7e2e09ce67e206d707c137917710832db26a7fff8c6a7831bac40ed60042e138b8d32eff104960fa9af312358ecad3c257903337a3ba1940030464248eb9677bc7e2d594a5495199ca52923101fc8da202'
d_hello      = 'hello$00000000001636920512422$000389289a839f8104a19535a57c60be21c2da9312df51308e0cd363ba82885b51111111111111111111111111111111112880ccda64f655478e053e178a2b4caf3441570c37c51e5eddeb4fd3f5a15d94653de7101e9c59229b666124029fc7d2dbf080223cc1e27635e9ea1f374e44bf86208d23fe97661d97ed63d5b1585afed679e7d2855f55d403e71c50ebe0390207d926be16293d3d2aa55e6ea6d9f013'
d_gets       = 'gets$000000000001636920912942$0011434d9f6277a8dcf01ba29124a24c7fcad984da0feb3190ed8b19fced10385a111111111111111111111111111111112880ccda64f655478e053e178a2b4cafbb53d6f4e3d6208f387806d7fdd1b29d1ef0d44c78d3f67d087385cc23e857792c42ab947b9925bb962c44ce19571c245cedc1efaf00e4e745773ec52a8de4baaa3ea5f7b11113987c0c8283a400c30e9cc7e30a72efae130bb7369a9e391735'
d_store_1    = 'store$00000000001636920999182$0016fd8ebd2e696dc2323d83ce491aafa0d63f74a40ea31f924159d041837955a2111111111111111111111111111111112880ccda64f655478e053e178a2b4cafda230f5afde3a2b3e0b8b1fab8932fb5f92247f1a61e1ff48c154a7d889c8a90230a7c1edede1ef3db4d4614116d152ba252906ad668420f46e3321f294cc29272e39c5d99004d5cd4fd63b148c87970f5ae3ddce9d30afa66298b53b414b316'
d_store_2    = 'store$00000000001636920819299$002878b97f22115c59fbb3fb4b41564a6da24ecc24c48796195c1e42d5d0e5c7ae111111111111111111111111111111112880ccda64f655478e053e178a2b4cafda230f5afde3a2b3e0b8b1fab8932fb5a31a8733254af8eb083fd31fe7a10c364799ac5800ba50b75b32e01b2766953658320f6d1e4d99487824ae501104f85ce6a467afd899cdea1a7d091a1572e0d7f8e9c7906ba8fa066517fa3c167dce4f'
d_flag_4     = 'hello$00000000001636921242224$00068eee42167b2ff8fa1bd0bac4f4941bbefe917390618b819b681ddb01d61711111111111111111f19065c4c57594f0f2880ccda64f655478e053e178a2b4caf004f5b4c0e003d5c0c5f40505654420f2880ccda64f655478e053e178a2b4caf0f4206145e472919000440501249400f2880ccda64f655478e053e178a2b4caf0d404a4e5f4a3d081510162f151906112880ccda64f655478e053e178a2b4caf'



def flag_1():
    post(url_admin, data=d_admin_init, headers=headers)
    post(url_hello, data=d_hello, headers=headers)
    post(url_gets, data=d_gets, headers=headers)
    post(url_store, data=d_store_1, headers=headers)
    post(url_store, data=d_store_2, headers=headers)
    post(url_admin, data=d_admin_stop, headers=headers)
    post(url_admin, data=d_admin_init, headers=headers)
    post(url_hello, data=d_hello, headers=headers)
    post(url_gets, data=d_gets, headers=headers)
    post(url_store, data=d_store_1, headers=headers)
    post(url_store, data=d_store_2, headers=headers)
    post(url_admin, data=d_admin_stop, headers=headers)
    #admin
    #hello
    #gets
    #store

def flag_2():
    post(url_admin, data=d_admin_init, headers=headers)
    post(url_hello, data=d_hello, headers=headers)
    post(url_hello, data=d_hello, headers=headers)
    post(url_gets, data=d_gets, headers=headers)
    post(url_store, data=d_store_1, headers=headers)
    post(url_store, data=d_store_2, headers=headers)
    post(url_admin, data=d_admin_stop, headers=headers)
    #store1
    #store2
    #store1
    #store2
    #store1

def flag_3():
    # maybe change smth?
    post(url_admin, data=d_admin_init, headers=headers)
    post(url_store, data=d_store_2, headers=headers)
    post(url_store, data=d_store_1, headers=headers)
    post(url_admin, data=d_admin_stop, headers=headers)

def flag_4():
    post(url_admin, data=d_admin_init, headers=headers)
    post(url_admin, data=d_flag_4, headers=headers)
    post(url_admin, data=d_admin_stop, headers=headers)

if __name__ == '__main__':
    
    setup = subprocess.Popen(COMMAND_RUN, shell=True)
    setup.wait()

    flag_1()
    time.sleep(1)
    flag_2()
    time.sleep(1)
    flag_3()
    time.sleep(1)
    flag_4()
    time.sleep(1)


