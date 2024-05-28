import random # 퀴즈에 사용할 난수 생성을 위한 모듈
import sys # 파이썬 시스템을 제어하는 모듈
import urllib.request # 파파고 API에 번역 요청및 결과 응답을 받기 위한 모듈
import copy # 퀴즈를 위한 리스트를 기존 리스트로부터 깊은복사(deep copy)하기 위한 모듈
import json # 파파고 번역 결과(json형식)을 해석하기 위한 모듈 
from pykakasi import kakasi # 한자를 가나로 변환하기 위한 모듈
import warnings # 경고메세지를 무시하기 위한 모듈


hiragana = ['あ', 'い', 'う', 'え', 'お', 'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご', 'さ', 'ざ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'た', 'だ', 'ち', 'ぢ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん', 'きゃ', 'きゅ', 'きょ', 'ぎゃ', 'ぎゅ', 'ぎょ', 'しゃ', 'しゅ', 'しょ', 'じゃ', 'じゅ', 'じょ', 'ちゃ', 'ちゅ', 'ちょ', 'にゃ', 'にゅ', 'にょ', 'ひゃ', 'ひゅ', 'ひょ', 'びゃ', 'びゅ', 'びょ', 'ぴゃ', 'ぴゅ', 'ぴょ', 'みゃ', 'みゅ', 'みょ', 'りゃ', 'りゅ', 'りょ'] # 히라가나(탁음, 반탁음, 요음 포함) 104자

katakana = ['ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ', 'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ', 'セ', 'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ヂ', 'ツ', 'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヲ', 'ン', 'キャ', 'キュ', 'キョ', 'ギャ', 'ギュ', 'ギョ', 'シャ', 'シュ', 'ショ', 'ジャ', 'ジュ', 'ジョ', 'チャ', 'チュ', 'チョ', 'ニャ', 'ニュ', 'ニョ', 'ヒャ', 'ヒュ', 'ヒョ', 'ビャ', 'ビュ', 'ビョ', 'ピャ', 'ピュ', 'ピョ', 'ミャ', 'ミュ', 'ミョ', 'リャ', 'リュ', 'リョ'] # 가타카나 104자

english = [['a'], ['i'], ['u'], ['e'], ['o'], ['ka'], ['ga'], ['ki'], ['gi'], ['ku'], ['gu'], ['ke'], ['ge'], ['ko'], ['go'], ['sa'], ['za'], ['shi','si','ci'], ['ji','zi'], ['su'], ['zu'], ['se'], ['ze'], ['so'], ['zo'], ['ta'], ['da'], ['chi'], ['ji','zi'], ['tsu','tu'], ['zu'], ['te'], ['de'], ['to'], ['do'], ['na'], ['ni'], ['nu'], ['ne'], ['no'], ['ha'], ['ba'], ['pa'], ['hi'], ['bi'], ['pi'], ['fu'], ['bu'], ['pu'], ['he'], ['be'], ['pe'], ['ho'], ['bo'], ['po'], ['ma'], ['mi'], ['mu'], ['me'], ['mo'], ['ya'], ['yu'], ['yo'], ['ra'], ['ri'], ['ru'], ['re'], ['ro'], ['wa'], ['wo'], ['n'], ['kya'], ['kyu'], ['kyo'], ['gya'], ['gyu'], ['gyo'], ['sha'], ['shu'], ['sho'], ['ja'], ['ju'], ['jo'], ['cha'], ['chu'], ['cho'], ['nya'], ['nyu'], ['nyo'], ['hya'], ['hyu'], ['h4yo'], ['bya'], ['byu'], ['byo'], ['pya'], ['pyu'], ['pyo'], ['mya'], ['myu'], ['myo'], ['rya'], ['ryu'], ['ryo']] # 가나에 대응되는 영어 104자

korean = [['아'], ['이'], ['우','으'], ['에'], ['오'], ['카','까'], ['가'], ['키','끼'], ['기'], ['쿠','꾸'], ['구'], ['케','께'], ['게'], ['코','꼬'], ['고'], ['사'], ['자'], ['시', '쉬'], ['지'], ['스'], ['즈'], ['세'], ['제'], ['소'], ['조'], ['타'], ['다'], ['치','찌'], ['###'], ['츠'], ['***'], ['테'], ['데'], ['토', '또'], ['도'], ['나'], ['니'], ['누'], ['네'], ['노'], ['하','와'], ['바'], ['파','빠'], ['히'], ['비'], ['피','삐'], ['후'], ['부'], ['푸','뿌'], ['헤'], ['베'], ['페','뻬'], ['호'], ['보'], ['포','뽀'], ['마'], ['미'], ['무'], ['메'], ['모'], ['야'], ['유'], ['요'], ['라','롸'], ['리','뤼'], ['루'], ['레','뤠'], ['로'], ['와'], ['ㅗ'], ['응','ㄴ','ㅁ','ㅇ'], ['캬','꺄'], ['큐','뀨'], ['쿄','꾜'], ['갸'], ['규'], ['겨'], ['샤','쌰'], ['슈','쓔'], ['쇼','쑈'], ['쟈'], ['쥬'], ['죠'], ['차','짜'], ['추','쭈'], ['초','쪼'], ['냐'], ['뉴'], ['뇨'], ['햐'], ['휴'], ['효'], ['뱌','뺘'], ['뷰'], ['뵤'], ['표','뾰'], ['퓨','쀼'], ['표','뾰'], ['먀'], ['뮤'], ['묘'], ['랴'], ['류'], ['료']] # 가나에 대응되는 한글 104자


def line(n): # 줄을 출력해주는 함수
    if n:
        print('\n----------------\n')
    else:
        print('----------------')


def gana_quiz(m): # 가나 퀴즈
    gana = copy.deepcopy(hiragana if m == 1 else katakana) # 퀴즈를 위한 가나 리스트 복제
    eng = copy.deepcopy(english)
    
    while(len(gana) > 0):
        line(0)
        i = random.randint(0, len(gana)-1) # 랜덤으로 가나 리스트에서 가나 하나 뽑기
        ans = str(input(gana[i]+' (남은 가나 수: '+str(len(gana))+')\n-> '))
        if ans in eng[i]: # 정답을 입력시 "정답!" 출력 후 가나 리스트에서 제거
            print("정답!")
            del gana[i]
            del eng[i]
        elif ans == '00':
            sys.exit()
        else:
            print("오답. 정답은 " + eng[i][0])
    print("퀴즈 완료") # 모든 가나를 맞출 시 퀴즈 종료


def add_word(txt): # 단어 암기장에 새로운 단어 추가
    with open(r'C:\Users\happy\Desktop\학교\고등학교\2학년\일본어 암기 프로그램\wordList.txt', 'r', encoding='utf-8') as file:
        word = file.read().strip().split('\n') # 단어 암기장을 읽어서 리스트로 변환
        if txt in word:
            print("이미 단어장에 포함된 단어")
        else:
            f.write(txt+'\n')


def word_quiz(): # 단어 암기장에 저장된 단어로 퀴즈
    with open(r'C:\Users\happy\Desktop\학교\고등학교\2학년\일본어 암기 프로그램\wordList.txt', 'r', encoding='utf-8') as file:
        word = file.read().strip().split('\n') # 단어 암기장을 읽어서 리스트로 변환
        
        while(len(word) > 0):
            line(0)
            i = random.randint(0, len(word)-1)
            ans = str(input(translate(word[i])+' (남은 단어 수: '+str(len(word))+')\n-> '))
            if ans == word[i]:
                print("정답!")
                del word[i]
            elif ans == '00':
                sys.exit()
            else:
                print("오답. 정답은 "+word[i])
    print("단어 퀴즈 완료")


def translate(txt): # 한-일 번역
    line(0)
    client_id = "obswukj60s"
    client_secret = "@API 사용을 위한 비밀 KEY가 들어갈 자리@" # 파파고 API를 사용하기 위한 ID와 PW
    encText = urllib.parse.quote(txt) # 번역 할 문장을 url 형식으로 인코딩
    data = "source=ko&target=ja&glossaryKey=d4073534-9c3f-491c-8395-7a4f9344a4a9&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation" #파파고 API로 문장 번역 요청
    request = urllib.request.Request(url) 
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return kanjitogana(json.loads(response_body.decode('utf-8'))["message"]["result"]["translatedText"]) # 응답받은 번역 결과를 반환(출력)
    else:
        print("Error Code:" + rescode) # 응답이 애러코드인 경우(오류가 발생한 경우) 애러코드 출력


def kortogana(txt,gm): # 한글을 가나로 변환
    txt = [c for c in txt] # 입력받은 한글을 리스트로 변환
    for i, t in enumerate(txt):
        if t in ['ㄱ','ㅅ','ㄷ','ㅌ','ㅍ','ㅈ']: # 촉음 입력
            if gm == 1:
                txt[i] = 'っ'
            elif gm == 2:
                txt[i] = 'ッ'
        elif t in ['ㅡ', '-','ー']: # 장음 변환
            if gm == 2:
                txt[i] = 'ー'
            elif txt[i-1] in ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ゃ", "ら", "わ", "が", "ざ", "だ", "ば", "ぱ"]:
                txt[i] = 'あ'
            elif txt[i-1] in ["い", "き", "し", "ち", "に", "ひ", "み", "り", "ぎ", "じ", "ぢ", "び", "ぴ"]:
                txt[i] = 'い'
            elif txt[i-1] in ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "ゅ", "る", "ぐ", "ず", "づ", "ぶ", "ぷ"]:
                txt[i] = 'う'
            elif txt[i-1] in ["え", "け", "せ", "て", "ね", "へ", "め", "れ", "げ", "ぜ", "で", "べ", "ぺ"]:
                txt[i] = 'え'
            elif txt[i-1] in ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "ょ", "ろ", "を", "ご", "ぞ", "ど", "ぼ", "ぽ"]:
                txt[i] = 'お'
        else:
            for j, c in  enumerate(korean): # 한글 발음에 맞는 가나를 찾아서 원하는 가나로 변환
                if t in c:
                    if gm == 1:
                        txt[i] = hiragana[j]
                        break
                    elif gm == 2:
                        txt[i] = katakana[j]
                        break
    return(''.join(txt)) # 변환된 문장을 반환


def ganatokor(txt): # 가나를 한글로 변환
    txt = [c for c in txt]
    for i, t in enumerate(txt):
        for j, c in  enumerate(hiragana):
            if t in c or t in katakana[j]:
                txt[i] = korean[j][0]
                break
    return(''.join(txt))


def kanjitogana(txt): # 한자를 히라가나로 변환
    line(0)
    k = kakasi()
    k.setMode('J', 'H')  # 한자-히라가나 변환
    k.setMode('H', 'H')  # 히라가나-히라가나로 유지
    k.setMode('K', 'K')  # 카타카나 유지
    k.setMode('s', True)  # 공백 유지
    conv = k.getConverter()
    return conv.do(txt)



def main(): # 메인 함수
    mode = 1
    while mode != 0:
        line(1)
        mode = int(input( "히라가나: 1\n가타카나: 2\n단어: 3\n한-일 번역기: 4\n한글-가나 입력기: 5\n가나-한글 입력기: 6\n한자-가나 변환기: 7\n-> ")) # 유저가 사용할 기능 선택 후 기능 실행
        if mode == 1: # 히라가나 퀴즈
            line(1)
            gana_quiz(1)
        elif mode == 2: # 가타카나 퀴즈
            line(1)
            gana_quiz(2)
        elif mode == 3: # 단어
            line(1)
            ans = int(input("단어 추가: 1\n단어 퀴즈: 2\n-> "))
            if ans == 1: # 단어 추가
                while 1:
                    line(0)
                    txt = str(input("추가 할 단어 입력(종료는 00 입력): "))
                    if txt == '00':
                        sys.exit()
                    else:
                        add_word(txt)
            elif ans == 2: # 단어 퀴즈
                line(1)
                word_quiz()
            else:
                sys.exit()
        elif mode == 4: # 한-일 번역
            while 1:
                line(1)
                txt = input('번역할 문장 입력(종료는 00 입력): ')
                if txt == '00':
                    sys.exit()
                tr = translate(txt)
                print(tr)
                line(0)
                print(ganatokor(tr))
        elif mode == 5: # 한글-가나 입력기
            line(1)
            gm = int(input("출력 할 가나 선택\n히라가나: 1\n가타카나: 2\n-> ")) # 변환 할 가나 선택
            while 1:
                line(0)
                txt = str(input("한글 입력(종료는 00 입력) -> "))
                if txt == '00':
                    sys.exit()
                print(kortogana(txt,gm))
        elif mode == 6: # 가나-한글 입력기
            while 1:
                line(0)
                txt = str(input("가나 입력(종료는 00 입력) -> "))
                if txt == '00':
                    sys.exit()
                print(ganatokor(txt))
        elif mode == 7: # 한자-가나 변환기
            while 1:
                line(0)
                txt = str(input("문장 입력(종료는 00 입력) -> "))
                if txt == '00':
                    sys.exit()
                print(kanjitogana(txt))



if __name__== "__main__": # 프로그램 시작시
    f = open(r'C:\Users\happy\Desktop\학교\고등학교\2학년\일본어 암기 프로그램\wordList.txt', 'a', encoding='utf-8') #  단어장을 "추가"모드로 열고,
    warnings.filterwarnings("ignore") # 경고메세지를 무시하도록 설정하고,
    main() # '메인 함수' 실행