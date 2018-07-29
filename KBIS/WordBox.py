# encoding: utf-8
import  random
class WordBox(object):
    def __init__(self):
        pass
    def GetString(self,name: str,money: int,calluser=False,command=None):
        random_value=random.randint(0,2)
        box=[]
        if(money>0):
           box.append(f'{name} さんは現在 {money}円 滞納しています。\r\nご相談等は会計担当まで。')
           box.append(f'現在、{name} さんの滞納額は {money}円 となっています。\r\nお早めのお支払をお願いします')
           box.append(f'現在、 {name} さんは {money}円 が滞納となっています')
        elif(money==0):
            box.append(f'現在、{name} さんの滞納額は 0円 となっています。\r\nご協力ありがとうございます')
            box.append(f'{name} さんには現在、滞納・返金等はございません。日頃よりご協力いただきありがとうございます')
            box.append(f'現在、 {name} さんは滞納、返金ともに無しとなっています')
        elif(money<0):
            box.append(f'{name} さんは現在 {money}円 払いすぎの状態となっています。\r\n後日返金させて頂きます。ご相談等は会計担当まで。')
            box.append(f'現在、{name} さんには {money}円 の返金が生じています。\r\n次回定例会などで会計担当よりお受け取りください。')
            box.append(f'現在、 {name} さんには {money}円 をご返金する予定です。')
        else:
            raise ValueError(f'GetStringでmoneyの値が不正 :money= {money}')
        returnStr=box[random_value]+'\r\n\r\n心当たりない場合、データが最新ではない可能性があります。次回更新時刻のあとにもう一度お試しください。'
        if(calluser and (command==None)):
            raise ValueError('calluserがTrueなのにcommandがnullのままになっています')
        if(calluser):
            calluser_random_value=random.randint(0,2)
            cubox=[]
            cubox.append(f'KBISより通知です。通知条件「{command}」に合致したためお知らせします。\r\n')
            cubox.append((f'KBISからのお知らせです。{name} さんは告知の基準「{command}」に該当しています。\r\n'))
            cubox.append(f'KBISより、条件:{command}を満たす方へ通知です。\r\n')
            returnStr= cubox[calluser_random_value] +returnStr
        return  returnStr