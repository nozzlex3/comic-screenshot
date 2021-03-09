# coding:utf-8
import pyautogui
import time
import os
# import shutil
from pathlib import Path
# import img2pdf
# from PIL import Image


SPAN = 0.1
WAIT_TIME = 5

# 背景色
# honto
# BACKGROUND_RGB = (50, 50, 60)     # Windows
# BACKGROUND_RGB = (50, 50, 59)     # Mac


BACKGROUND_RGB = (51, 51, 51)         # 少年ジャンプ+
TRANSPARENT_THRESHOLD = 10

# フォルダ名
PNG_FOLDER = "png"
PDF_FOLDER = "pdf"
ZIP_FOLDER = "zip"


def isBackgroundPixel(pixel_rgb):
    diff_rgb = [abs(pixel_rgb[i]-BACKGROUND_RGB[i]) for i in range(0, 3)]
    return (diff_rgb[0] < TRANSPARENT_THRESHOLD) & (diff_rgb[1] < TRANSPARENT_THRESHOLD) & (diff_rgb[2] < TRANSPARENT_THRESHOLD)


def boolInteractiveInput():
    input_value = input().lower()
    if input_value in ("y", "yes", "1", "true", "t"):
        return True
    elif input_value in ("n", "no", "0", "false", "f"):
        return False
    else raise ValueError


# 対話型 環境定義
print("### 電子書籍をpngにして保存します ###")
print("### タイトルとページ番号を入力した後、電子書籍を全画面表示にして下さい ###")
print("### ページごとの表示になっているか確認（見開きNG） ###")

print("保存するフォルダ名を入力してください\n> ", end='')
folder_name = input()
if (os.path.isdir(PNG_FOLDER+'/'+folder_name)):
    print(folder_name, "は既に存在しています\n")
    while True:
        try:
            print("上書きしますか？[y/n]\n> ", end='')
            overwrite_flag = boolInteractiveInput()
            if overwrite_flag:
                break
            else:
                print("中止しました")
                exit(1)
        except ValueError:
            print("'y'か'n'を入力してください\n")

while True:
    try:
        print("ページ数を入力してください\n> ", end='')
        page = int(input())
        break
    except ValueError:
        print("ページ数は半角数字である必要があります\n")
while True:
    try:
        print("見開きページですか？[y/n]\n> ", end='')
        spread_flag = boolInteractiveInput()
        break
    except ValueError:
        print("'y'か'n'を入力してください\n")
if spread_flag:
    while True:
        try:
            print("表紙は見開きですか？[y/n]\n> ", end='')
            spread_cover_flag = boolInteractiveInput()
            break
        except ValueError:
            print("'y'か'n'を入力してください\n")
else:
    spread_cover_flag = False
while True:
    try:
        print(WAIT_TIME, "秒以内に電子書籍のソフトかブラウザをフルスクリーンでアクティブな状態にして下さい")
        print("ENTER キーを押すとカウントダウンが始まります\n> ", end='')
        execution_bool = input()
        if execution_bool == '':
            break
        else:
            print("中止するには Ctrl + C を押して下さい\n")
    except KeyboardInterrupt:
        print("中止しました")
        exit(1)


os.makedirs(PNG_FOLDER + '/' + folder_name, exist_ok=True)

# カウントダウン
for second in range(WAIT_TIME+1):
    print("\r{:02} [s]".format(WAIT_TIME-second), end='')
    time.sleep(1)

# ディスプレイサイズ取得
img = pyautogui.screenshot()
display_width = img.size[0]
display_height = img.size[1]


# 背景の色ではない2つの角のx座標を取得
# (x1,y1)=左上 (x2,y2)=右下
for xi in range(0, display_width):
    if isBackgroundPixel(img.getpixel((xi, 0))):
        pass
    else:
        x1 = xi
        break
for xi in range(0, display_width):
    if isBackgroundPixel(img.getpixel(((display_width-1)-xi, (display_height-1)-1))):
        pass
    else:
        x2 = (display_width-1)-xi
        break

y1, y2 = 0, display_height-1

# パディング(必要なら)
x1 += 1
y2 -= 1

# ページサイズの定義
# 表紙が見開き
if spread_cover_flag:
    # ページサイズは半分
    page_width = (x2-x1+1)//2
    page_height = y2-y1+1
    top_page = 0
# 表紙が単一ページ
else:
    page_width = x2-x1+1
    page_height = y2-y1+1
    top_page = 1


# 表紙が単一ページの場合の表紙のスクリーンショット
if not spread_cover_flag:
    out_filename = str(1).zfill(4) + '.png'
    s = pyautogui.screenshot(region=(x1, y1, page_width, page_height))
    s.save(PNG_FOLDER+'/'+folder_name + '/' + out_filename)
    pyautogui.keyDown('left')
    time.sleep(SPAN)


# ページ数分スクリーンショットをとる
# 見開きの場合
if spread_flag:
    for p in range(top_page, page, 2):
        # 奇数ページ
        out_filename = str(p+1).zfill(4) + '.png'
        s = pyautogui.screenshot(region=(display_width//2, 0, page_width, page_height))
        s.save(PNG_FOLDER+'/'+folder_name + '/' + out_filename)

        # 偶数ページ
        out_filename = str(p+2).zfill(4) + '.png'
        s = pyautogui.screenshot(region=(display_width//2-page_width, 0, page_width, page_height))
        s.save(PNG_FOLDER+'/'+folder_name + '/' + out_filename)
        pyautogui.keyDown('left')
        time.sleep(SPAN)

# 単一ページの場合
else:
    for p in range(top_page, page):
        out_filename = str(p+1).zfill(4) + '.png'
        s = pyautogui.screenshot(region=(x1, y1, page_width, page_height))
        s.save(PNG_FOLDER+'/'+folder_name + '/' + out_filename)
        pyautogui.keyDown('left')
        time.sleep(SPAN)


# shutil.make_archive(ZIP_FOLDER+'/'+folder_name, 'zip', root_dir=PNG_FOLDER+'/'+folder_name)
# img_path_list = [str(img_path) for img_path in Path(
#     "./"+PNG_FOLDER+'/'+folder_name).rglob('*.png')]
# with open(PDF_FOLDER+'/'+folder_name+".pdf",'wb') as f:
#     # for img_path in img_path_list:
#     f.write(img2pdf.convert(img_path_list))
print("finished")
