#!/usr/bin/env python3
"""Regenerate the native SVG/PNG campaign kit on macOS; not a Hugo dependency.
Copy lives here; rendered SVG lettering is outlined and contains no external font link.
"""
import html
import json
from pathlib import Path
import subprocess
import shutil
import struct
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PAPER='#F3E7C8';WHITE='#FFF9E9';TEAL='#123C3D';INK='#292822';GOLD='#E8B844';ORANGE='#CF5935'
texts=[];assets=[];documents=[]

def text(value,x,y,size,color=TEAL,width=None,center=False,font='Futura-CondensedExtraBold'):
    i=len(texts)
    texts.append({'id':i,'text':value,'x':x,'y':y,'size':float(size),'font':font,'color':color,'maxWidth':width,'center':center})
    return f'@@TEXT{i}@@'

def body(value,x,y,size=32,color=TEAL,width=None,center=False):
    return text(value,x,y,size,color,width,center,'AvenirNext-DemiBold')

def rect(x,y,w,h,fill=TEAL,r=0,stroke=None,sw=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'

def circle(x,y,r,fill=GOLD,stroke=None,sw=3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'

def line(x1,y1,x2,y2,color=TEAL,sw=3):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}"/>'

def star(x,y,r,color=GOLD):
    return f'<path d="M{x} {y-r}L{x+r*.24} {y-r*.24}L{x+r} {y}L{x+r*.24} {y+r*.24}L{x} {y+r}L{x-r*.24} {y+r*.24}L{x-r} {y}L{x-r*.24} {y-r*.24}Z" fill="{color}"/>'

def art(name,x,y,w,h=None):
    source=ET.parse(ROOT/'static/brand/svg'/name).getroot()
    # Keep the canonical geometry untouched, use a nested viewport for positioning.
    prefix=f'a{len(texts)}-{len(documents)}-{str(x).replace("-","n")}-{str(y).replace("-","n")}-'
    for el in source.iter():
        if 'id' in el.attrib:el.set('id',prefix+el.get('id'))
    source.set('x',str(x));source.set('y',str(y));source.set('width',str(w));source.set('height',str(h or w))
    source.attrib.pop('aria-labelledby',None);source.attrib.pop('role',None)
    for el in list(source):
        if el.tag.rsplit('}',1)[-1] in ['title','desc']:source.remove(el)
    return ET.tostring(source,encoding='unicode').replace('ns0:','').replace(':ns0','')

def logo(x,y,w,color='ink'):
    return art(f'marks/wordmark-{color}.svg',x,y,w,w/5)

def label(value,x,y,w,size=27,fill=GOLD):
    return rect(x,y,w,size+30,fill,r=10)+body(value,x+18,y+14,size,TEAL,width=w-36)

def deco(w,h):
    return ''.join(star(x,y,r,c) for x,y,r,c in [(w*.08,h*.15,22,ORANGE),(w*.91,h*.16,28,GOLD),(w*.88,h*.86,18,ORANGE),(w*.11,h*.83,15,GOLD)])

def page(id,title,w,h,content,description,platforms,usage,alt=None,safe=None,kind='evergreen'):
    asset={'id':id,'title':title,'description':description,'width':w,'height':h,'svg':f'/marketing/svg/{id}.svg','png':f'/marketing/png/{id}.png','webp':f'/marketing/webp/{id}.webp','platforms':platforms,'alt':alt or description,'usage':usage,'kind':kind}
    if safe:asset['safeArea']=dict(zip(['x','y','width','height'],safe))
    assets.append(asset)
    documents.append((id,f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(asset["alt"])}</desc>{content}</svg>'))

def main():
    global texts, assets, documents
    texts, assets, documents = [], [], []
    # 1: An avatar keeps the original asymmetry and reads in circular crops.
    page('quiznauts-avatar','Mr. Big profile avatar',1024,1024,
        rect(0,0,1024,1024,TEAL)+circle(512,512,469,PAPER)+circle(512,512,447,TEAL)+art('mascot/mr-big-avatar.svg',34,-3,956),
        'A round, friendly Mr. Big astronaut helmet on a teal and cream profile medallion.',
        ['YouTube','Instagram','TikTok','Facebook','Bluesky','X','Pinterest'],
        'Shared 1024-square production master. Preview the actual circular profile crop before saving; no wordmark or small text.',safe=(64,64,896,896),kind='profile')

    # 2: Wide banner puts all meaning into the conservative proportional center crop.
    banner=(rect(0,0,2560,1440,PAPER)+deco(2560,1440)+circle(2300,280,160,GOLD)+circle(180,1150,220,ORANGE)
           +f'<path d="M0 1130Q1300 880 2560 1140V1440H0Z" fill="{TEAL}"/>'
           +logo(580,545,930)+body('Come for the cow. Leave knowing more.',600,780,44,width=1010)
           +body('Clever quizzes. Curious people.',600,852,30,width=950)
           +art('mascot/mr-big-welcome.svg',1570,470,490))
    page('quiznauts-youtube-banner','YouTube channel banner',2560,1440,banner,
         'Cream atomic-era banner with the Quiznauts wordmark, a welcoming toy cow astronaut, and the line “Come for the cow. Leave knowing more.”',
         ['YouTube'],'2560 × 1440 recommended canvas. Essentials use a centered 1540 × 420 design guide. Review actual phone, desktop and TV crops in Studio.',safe=(510,510,1540,420),kind='profile')

    # 3: Thumbnail is a factual evergreen invitation, not a pretend published video.
    thumb=(rect(0,0,1280,720,TEAL)+circle(1120,80,260,GOLD)+rect(42,40,1196,640,PAPER,r=24)
           +label('A LITTLE COW. A BIG QUESTION.',84,84,610,25)
           +text('HOW MUCH',80,190,106,width=680)+text('DO YOU KNOW?',80,300,106,width=670)
           +body('Pick A, B or C. Stay for the explanation.',85,487,29,width=680)
           +logo(84,588,500)+art('mascot/mr-big-avatar-thinking.svg',767,140,470)
           +star(1130,595,35,ORANGE))
    page('quiznauts-youtube-thumbnail','YouTube quiz invitation thumbnail',3840,2160,
         '<g transform="scale(3)">'+thumb+'</g>',
         'Retro invitation thumbnail: “How much do you know?” beside a thoughtful Mr. Big.',
         ['YouTube'],'3840 × 2160 follows current YouTube recommendation checked October 22, 2026. Adapt title to the actual video; do not imply this template is an uploaded episode.',safe=(126,120,3588,1920),kind='template')

    # 4: End card leaves a large clean panel for actual Studio end-screen elements.
    end=(rect(0,0,1920,1080,PAPER)+rect(0,0,750,1080,TEAL)+logo(70,75,590,'reversed')
         +art('mascot/mr-big-celebrating.svg',60,270,650)+text('ONE MORE',835,130,112,width=960)
         +text('SMALL DISCOVERY?',835,270,110,width=970)+body('Keep your curiosity in orbit.',845,445,43,width=910)
         +rect(835,575,960,360,WHITE,r=30,stroke=TEAL,sw=4)+star(1745,1010,25,ORANGE))
    page('quiznauts-youtube-end-card','YouTube end-card background',1920,1080,end,
         'Mr. Big cheers beside “One more small discovery?” and an open cream panel for end-screen elements.',
         ['YouTube'],'Design background only. Place real clickable end-screen elements in Studio; the empty panel is a suggested placement, not a guaranteed platform slot.',safe=(835,575,960,360),kind='template')

    # 5: Site metadata image.
    og=(rect(0,0,1200,630,PAPER)+rect(0,0,30,630,TEAL)+logo(65,68,670)
        +text('SMALL COW.',75,245,82,width=670)+text('BIG CURIOSITY.',75,345,82,width=670)
        +body('Play a quiz. Take a little knowledge home.',78,497,27,width=690)
        +circle(978,317,198,GOLD)+art('mascot/mr-big-welcome.svg',737,77,450)+star(1112,540,25,ORANGE))
    page('quiznauts-open-graph','Website and link preview',1200,630,og,
         'Quiznauts link card with a tiny cow astronaut: “Small cow. Big curiosity. Play a quiz. Take a little knowledge home.”',
         ['Website','Link previews'],'Default Open Graph image production choice. Preview actual link unfurls; crawlers and platforms control their own crop and caching.',safe=(55,55,1090,520))

    # 6: Brand square built as a poster, not a resized header.
    sq=(rect(0,0,1080,1080,TEAL)+rect(36,36,1008,1008,PAPER,r=24)+logo(120,90,840)
        +text('COME FOR',540,295,99,center=True,width=890)+text('THE COW.',540,410,99,center=True,width=890)
        +art('mascot/mr-big-welcome.svg',315,495,450)+star(160,685,52,ORANGE)+star(894,790,35,GOLD)
        +body('Leave knowing more.',540,966,37,center=True,width=900))
    page('quiznauts-brand-square','Square brand introduction',1080,1080,sq,
         'Atomic advertising poster: “Come for the cow. Leave knowing more.” with Mr. Big waving.',
         ['Instagram','Facebook','Community posts'],'Evergreen brand introduction; repeat the wording in the post caption and supply image description.',safe=(72,72,936,936))

    # 7: Portrait invitation, independently composed for feed.
    feed=(rect(0,0,1080,1350,PAPER)+rect(44,44,992,1262,WHITE,r=22,stroke=TEAL,sw=4)
          +logo(110,85,860)+label('CURIOSITY HAS A CREW',266,290,548,27)
          +text('YOU BELONG',540,410,116,center=True,width=910)+text('IN THIS ORBIT.',540,550,116,center=True,width=910)
          +art('mascot/mr-big-celebrating.svg',280,690,520)+star(170,860,38,ORANGE)+star(900,1020,42,GOLD)
          +body('Pick an answer. Meet a new idea.',540,1223,34,center=True,width=900))
    page('quiznauts-feed-portrait','Portrait feed invitation',1080,1350,feed,
         'Mr. Big cheers below “You belong in this orbit. Pick an answer. Meet a new idea.”',
         ['Instagram','Facebook'],'4:5 production export for feed posts. Recheck the current composer crop before publishing.',safe=(80,80,920,1190))

    # 8: Vertical layout keeps essentials away from typical edge controls.
    vertical=(rect(0,0,1080,1920,TEAL)+circle(930,180,230,GOLD)+circle(100,1750,270,ORANGE)
              +rect(75,240,850,1330,PAPER,r=48)+logo(145,320,680)
              +text('ONE QUESTION.',500,535,103,center=True,width=735)+text('A NEW IDEA.',500,665,103,center=True,width=735)
              +art('mascot/mr-big-pointing.svg',180,820,650)
              +body('Pick A, B or C.',500,1450,46,center=True,width=720)
              +body('Stay for the explanation.',500,1523,35,center=True,width=720))
    page('quiznauts-vertical-invitation','Vertical quiz invitation',1080,1920,vertical,
         'Vertical teal poster with Mr. Big and the words “One question. A new idea. Pick A, B or C. Stay for the explanation.”',
         ['YouTube Shorts','Instagram Reels','TikTok','Stories'],
         '9:16 still artwork, not a video or a platform-certified overlay map. Essential content uses x120–900 and y280–1580. Check each app’s live UI and captions.',safe=(120,280,780,1300))

    # 9–10: A sourced two-card post tied to the playable first-contact mission.
    mission=json.loads((ROOT/'data/quick_mission.json').read_text())
    question_data=next(q for q in mission['questions'] if q['id']=='fc-ocean-pacific')
    assert question_data['answer']=='B'
    assert question_data['prompt']=="Which is Earth's largest ocean basin?"
    assert question_data['explanation']=="The Pacific is Earth's largest ocean basin. It is also the deepest; the Atlantic is the second largest."
    question=(rect(0,0,1080,1080,PAPER)+logo(80,60,610)+label('FIRST CONTACT · QUESTION 01',80,240,760,26)
              +text("EARTH'S LARGEST",80,370,111,width=920)+text('OCEAN BASIN?',80,510,111,width=900)
              +body('Which would you choose?',84,673,33,width=890))
    for i,choice in enumerate(question_data['choices']):
        x=80+i*314
        question+=rect(x,770,290,150,TEAL,r=22)+text(choice['id'],x+145,792,61,PAPER,center=True)
        question+=body(choice['text'],x+145,873,29,PAPER,width=245,center=True)
    question+=body('Source: NOAA · Answer on the next card',80,975,27,width=920)
    page('quiznauts-question-card','First Contact question card',1080,1080,question,
         "Quiznauts asks: Which is Earth's largest ocean basin? A Atlantic, B Pacific, or C Indian. Answer on the next card. Source: NOAA.",
         ['Instagram','Facebook','Community posts'],'Pair with the explanation card. Based on First Contact question fc-ocean-pacific; include the complete source link and both cards in the post.',safe=(80,60,920,970),kind='question')
    assets[-1]['source']=question_data['source'];assets[-1]['questionId']=question_data['id']
    answer=(rect(0,0,1080,1080,TEAL)+logo(80,65,640,'reversed')+rect(65,245,950,640,PAPER,r=28)
            +label('FIRST CONTACT · EXPLANATION',105,280,860,24)
            +text('B · PACIFIC',110,405,115,width=840)
            +body('The Pacific is Earth’s largest',110,580,36,width=840)
            +body('ocean basin. It is also the deepest.',110,643,36,width=840)
            +body('The Atlantic is the second largest.',110,723,33,width=840)
            +body('Source: NOAA Ocean Service',110,807,28,width=840)
            +body('The explanation is part of the fun.',540,947,36,PAPER,center=True,width=920))
    page('quiznauts-explanation-card','First Contact explanation card',1080,1080,answer,
         'Answer B: Pacific. The Pacific is Earth’s largest ocean basin and the deepest. The Atlantic is second largest. Source: NOAA Ocean Service.',
         ['Instagram','Facebook','Community posts'],'Pair with the question card. Include source https://oceanservice.noaa.gov/facts/biggestocean.html in the caption; wording is synchronized to the First Contact mission.',safe=(80,65,920,950),kind='explanation')
    assets[-1]['source']=question_data['source'];assets[-1]['questionId']=question_data['id']

    # 11: Keep meaning centrally placed; platform overlap still needs composer checks.
    wide=(rect(0,0,1500,500,PAPER)+rect(0,445,1500,55,TEAL)+logo(260,75,790)
          +body('Small cow. Big curiosity.',275,292,44,width=820)+art('mascot/mr-big-avatar.svg',1070,-15,475)
          +star(100,150,52,ORANGE)+star(150,350,26,GOLD))
    page('quiznauts-wide-profile-header','Wide profile header',1500,500,wide,
         'A cream wide header with the Quiznauts wordmark, “Small cow. Big curiosity.” and Mr. Big’s helmet.',
         ['Bluesky','X'],'3:1 reusable production master. Profile-photo overlap and responsive cropping differ by service; check the composer before saving.',safe=(250,60,1050,345),kind='profile')

    # 12: Cover uses a different central arrangement from the 3:1 header.
    cover=(rect(0,0,1640,624,TEAL)+circle(1450,155,125,GOLD)+logo(305,90,1000,'reversed')
           +text('A LITTLE COW. A BIG QUESTION.',820,335,66,PAPER,center=True,width=1190)
           +body('Clever quizzes for curious people.',820,444,41,PAPER,center=True,width=1150)
           +star(130,145,54,ORANGE)+star(1500,530,35,ORANGE))
    page('quiznauts-facebook-cover','Community cover artwork',1640,624,cover,
         'Teal community cover: “A little cow. A big question. Clever quizzes for curious people.”',
         ['Facebook'],'1640 × 624 production master, not a verified current platform minimum. Check desktop/mobile crop and profile overlap in the composer.',safe=(260,85,1120,430),kind='profile')

    # 13: Pinterest-style vertical poster follows an editorial path, not a clipped feed card.
    pin=(rect(0,0,1000,1500,PAPER)+rect(40,40,920,1420,WHITE,r=28,stroke=TEAL,sw=4)
         +logo(110,90,780)+label('A SMALL DISCOVERY AWAITS',160,300,680,27)
         +text('TAKE YOUR',500,435,113,center=True,width=850)+text('CURIOSITY',500,570,113,center=True,width=850)
         +text('FOR A SPIN.',500,705,113,center=True,width=850)
         +art('mascot/mr-big-welcome.svg',240,850,520)+star(125,1030,40,ORANGE)+star(870,1150,31,GOLD)
         +body('Quizzes worth wondering about.',500,1386,31,center=True,width=850))
    page('quiznauts-pinterest-poster','Curiosity poster',1000,1500,pin,
         'A tall atomic-era poster featuring Mr. Big: “Take your curiosity for a spin. Quizzes worth wondering about.”',
         ['Pinterest'],'2:3 production export. Link only to a published matching destination; add the readable copy and image description in the composer.',safe=(80,80,840,1340))

    # 14: Small corner mark useful for video, not another avatar.
    page('quiznauts-video-watermark','Video corner watermark',300,300,
         art('marks/q-orbit.svg',10,10,280),
         'Transparent Quiznauts Q-orbit corner mark.',
         ['YouTube','Video'],'300-square production choice. YouTube requires at least150 ×150 and under1MB; availability depends on video audience designation. Check legibility over footage.',safe=(10,10,280,280),kind='video')

    with tempfile.TemporaryDirectory(prefix='quiznauts-art-') as td:
        td=Path(td); request=td/'text-input.json';response=td/'text-output.json'
        request.write_text(json.dumps(texts))
        subprocess.run(['swift','-module-cache-path','/private/tmp/quiznauts-swift-cache',str(ROOT/'scripts/generate-art-outlines.swift'),str(request),str(response)],check=True)
        outlines={a['id']:a for a in json.loads(response.read_text())}
        replacements={}
        for a in texts:
            o=outlines[a['id']];scale=min(1,(a['maxWidth']/o['width'])) if a['maxWidth'] else 1
            x=a['x']-(o['width']*scale/2 if a['center'] else 0)
            replacements[f'@@TEXT{a["id"]}@@']=f'<g aria-label="{html.escape(a["text"])}" fill="{a["color"]}" transform="translate({x:.3f} {a["y"]}) scale({scale:.5f})"><path d="{o["d"]}"/></g>'
        render=[]
        for (id,svg),asset in zip(documents,assets):
            for token,shape in replacements.items():svg=svg.replace(token,shape)
            out=td/'svg'/f'{id}.svg';out.parent.mkdir(exist_ok=True);out.write_text(svg+'\n')
            render.append({'input':str(out),'output':str(td/'png'/f'{id}.png'),'width':asset['width'],'height':asset['height']})
        (td/'png').mkdir(exist_ok=True)
        jobs=td/'render.json';jobs.write_text(json.dumps(render))
        subprocess.run(['swift','-module-cache-path','/private/tmp/quiznauts-swift-cache',str(ROOT/'scripts/generate-art-render.swift'),str(jobs)],check=True)
        # Validate the complete batch before replacing any saved master/export.
        for asset in assets:
            ET.parse(td/'svg'/f"{asset['id']}.svg")
            raw=(td/'png'/f"{asset['id']}.png").read_bytes()
            if raw[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',raw[16:24]) != (asset['width'],asset['height']):
                raise ValueError('Incomplete native render: '+asset['id'])
        for asset in assets:
            for kind in ('svg','png'):
                source=td/kind/f"{asset['id']}.{kind}"
                destination=ROOT/'static/marketing'/kind/source.name
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source,destination)
    (ROOT/'data/marketing.json').write_text(json.dumps({'edition':'1.0','reviewed':'2026-10-22','direction':'Atomic Advertising; Mr. Big v1.4','assets':assets},indent=2,ensure_ascii=False)+'\n')
    print(f'Wrote {len(assets)} self-contained SVG masters, native-size PNGs, and marketing metadata. Run ./qn images to refresh WebP copies and download kits.')


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit("Artwork generation stopped; saved outputs were retained until the full render succeeded: " + str(error))
