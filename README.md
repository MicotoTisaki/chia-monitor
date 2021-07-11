# chia-monitor
chiaにおけるplotファイルのモニタリングをhpoolのGUI風で監視できるツールです。
plotディレクトリの追加・削除もこのツールから可能になっています。

This is a tool that can monitor chia plot files in the GUI style of hpool. It is also possible to add and remove plot directories from this tool.


# 表示情報について
## 上部ステータス欄
Capacity:登録ディレクトリ内のplotファイルの合計容量
Number:登録ディレクトリ内のplotファイルの合計数

Add dir:plotディレクトリの新規登録。chia plots add -d ""のコマンドが走ります
Delete dir:選択中のディレクトリが登録削除されます。cha plots remove -d ""のコマンドが走ります。
reload:画面内を更新します。これは起動後120secごとに自動で走っています。更新を急ぎたいときは押してください。


Capacity:Total capacity of plot files in the registered directory
Number: Total number of plot files in the registered directory

Add dir: New plots directory is registered, and the command chia plots add -d "" will be executed.
Delete dir: The selected directory will be registered and deleted, and the command cha plots remove -d "" will be executed.
reload: Refresh the screen. This runs automatically every 120 seconds after startup. Press this button if you want to hurry the refresh.



## 下部詳細欄
path:登録されているディレクトリ一覧です。chia plots showが走ってます。
capacity:そのドライブの合計容量が表示されます。
Idle capacity:空き容量が表示されます。
number:plotファイルの合計数が表示されます。これは拡張子.plotの個数で判定しています。
Idle number:現在の空き容量でいくつ追加出来るかを概算して表示しています。1plot101.5GiBでの計算です。


path: A list of registered directories, and the command chia plots show will be executed.
capacity: Shows the total capacity of the drive.
Idle capacity: Shows the free capacity of the drive.
number: Shows the total number of plot files. This is determined by the number of .plot extensions.
Idle number: Shows a rough estimate of how many plots can be added with the current free space, based on a calculation of 101.5 GiB per plot.



# 実行方法
このgithubにあるmain.exeをダウンロードし実行してください。ライブラリ等はコンパイル時に同胞しています。
また、一緒に上げているmain.pyはソースコードとなります。

Download and run the main.exe file on this github. The libraries are included at compile time.
Also, the main.py file is the source code.



これらの翻訳はDeepLにて行っています。
These are translated at DeepL.

## 投げ銭用アドレス
XCH:xch124zmvg9g59sauqhmvdryd58skhgsmrud5npn76xe3tgt6ujegdsspk9msh
