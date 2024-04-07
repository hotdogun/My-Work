import requests
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm
import os

def extract_media(url,Group,id):
    video_links = []
    flag=0
    try:
        #print(url)
        response = requests.get(url)
        url=url[:url.find('/',url.find('/',url.find('/')+1)+1)] #도메인 이후 절사
        soup = BeautifulSoup(response.content, 'html.parser')
        name_tags = soup.find_all('h2',class_="subject") #이름 찾기
        for ntag in name_tags:
            name = ntag.text
            name=remove_html_tags(name)
        print(name)
        video_tags = soup.find_all('video')#비디오 파일을 포함하는 태그를 찾기
        #print(video_tags)
        for tag in video_tags:
            #print(tag['src'])
            Target=url+str(tag['src'])#비디오 소스 url
            video_links.append(Target)
        if not name:
            print("@ 재접근")
            flag=1
        else:
            for link in video_links:
                valid_filename = ''.join(c if c.isalnum() or c in ['.', ' '] else '_' for c in name) #파일명 불가 특수문자 제거
                webget(link,str(id)+'-'+valid_filename+".mp3",Group)
    except Exception as e:
        print("Error:", e)
    return flag

def webget(url,name,subDirectory):
    response = requests.get(url)
    directory = os.path.join(os.getcwd(), subDirectory)  # 현재 작업 디렉토리와 하위 디렉토리를 조합하여 경로 생성
    os.makedirs(directory, exist_ok=True)  # 하위 디렉토리 생성 (이미 존재하면 무시)
    filepath = os.path.join(directory, name)  # 파일 경로 생성
    with open(filepath, 'wb') as f:
        f.write(response.content)

def remove_html_tags(text):
    # 정규 표현식을 사용하여 HTML 태그를 제거
    cleaned_text = re.sub(r'<[^>]+>', '', text)
    return cleaned_text

# 게시물 번호 범위
start_id = 36334
end_id = 36745


# 각 게시물에서 비디오 추출 및 다운로드
print("##금융감독원 보이스피싱 음원 그놈목소리 추출##")
for post_id in tqdm(range(start_id, end_id + 1)):
    url1 = f"https://fss.or.kr/fss/bbs/B0000206/view.do?nttId={post_id}&menuNo=200690"
    url2 = f"https://fss.or.kr/fss/bbs/B0000207/view.do?nttId={post_id}&menuNo=200691"
    print("\n"+str(post_id))
    if(extract_media(url1,"대출사기형",post_id)):
        extract_media(url2,"수사기관 사칭형(검찰, 경찰 등)",post_id)
    time.sleep(0.3)
    
