SET CHARSET UTF8MB4;
CREATE TABLE album.post( 
    post_ULID CHAR(26),
    posted_by INT UNSIGNED NOT NULL,
    posted_at DATETIME  DEFAULT CURRENT_TIMESTAMP,
    taken_at DATETIME  DEFAULT CURRENT_TIMESTAMP,

    file_name varchar(255) NOT NULL,
    content_type varchar(512) NOT NULL,

    file_path varchar(255) UNIQUE,

    PRIMARY KEY(post_ULID)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE album.tag (
  tag_ID INT NOT NULL AUTO_INCREMENT,
  type varchar(25) NOT NULL,
  name varchar(100) NOT NULL,
  PRIMARY KEY(tag_ID)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE album.tag_post_relation (
  post_ULID CHAR(26),
  tag_ID INT,
  PRIMARY KEY(post_ULID,tag_ID)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO album.tag (tag_ID,type,name) values (1, 'yolo','人');
INSERT INTO album.tag (tag_ID,type,name) values (2, 'yolo','自転車');
INSERT INTO album.tag (tag_ID,type,name) values (3, 'yolo','車');
INSERT INTO album.tag (tag_ID,type,name) values (4, 'yolo','オートバイ');
INSERT INTO album.tag (tag_ID,type,name) values (5, 'yolo','飛行機');
INSERT INTO album.tag (tag_ID,type,name) values (6, 'yolo','バス');
INSERT INTO album.tag (tag_ID,type,name) values (7, 'yolo','電車');
INSERT INTO album.tag (tag_ID,type,name) values (8, 'yolo','トラック');
INSERT INTO album.tag (tag_ID,type,name) values (9, 'yolo','ボート');
INSERT INTO album.tag (tag_ID,type,name) values (10, 'yolo','信号機');
INSERT INTO album.tag (tag_ID,type,name) values (11, 'yolo','消火栓');
INSERT INTO album.tag (tag_ID,type,name) values (12, 'yolo','一時停止の標識');
INSERT INTO album.tag (tag_ID,type,name) values (13, 'yolo','パーキングメーター');
INSERT INTO album.tag (tag_ID,type,name) values (14, 'yolo','ベンチ');
INSERT INTO album.tag (tag_ID,type,name) values (15, 'yolo','鳥');
INSERT INTO album.tag (tag_ID,type,name) values (16, 'yolo','猫');
INSERT INTO album.tag (tag_ID,type,name) values (17, 'yolo','犬');
INSERT INTO album.tag (tag_ID,type,name) values (18, 'yolo','馬');
INSERT INTO album.tag (tag_ID,type,name) values (19, 'yolo','羊');
INSERT INTO album.tag (tag_ID,type,name) values (20, 'yolo','牛');
INSERT INTO album.tag (tag_ID,type,name) values (21, 'yolo','象');
INSERT INTO album.tag (tag_ID,type,name) values (22, 'yolo','クマ');
INSERT INTO album.tag (tag_ID,type,name) values (23, 'yolo','ゼブラ');
INSERT INTO album.tag (tag_ID,type,name) values (24, 'yolo','キリン');
INSERT INTO album.tag (tag_ID,type,name) values (25, 'yolo','バックパック');
INSERT INTO album.tag (tag_ID,type,name) values (26, 'yolo','傘');
INSERT INTO album.tag (tag_ID,type,name) values (27, 'yolo','ハンドバッグ');
INSERT INTO album.tag (tag_ID,type,name) values (28, 'yolo','ネクタイ');
INSERT INTO album.tag (tag_ID,type,name) values (29, 'yolo','スーツケース');
INSERT INTO album.tag (tag_ID,type,name) values (30, 'yolo','フリスビー');
INSERT INTO album.tag (tag_ID,type,name) values (31, 'yolo','スキー');
INSERT INTO album.tag (tag_ID,type,name) values (32, 'yolo','スノーボード');
INSERT INTO album.tag (tag_ID,type,name) values (33, 'yolo','スポーツボール');
INSERT INTO album.tag (tag_ID,type,name) values (34, 'yolo','凧');
INSERT INTO album.tag (tag_ID,type,name) values (35, 'yolo','野球のバット');
INSERT INTO album.tag (tag_ID,type,name) values (36, 'yolo','野球のグローブ');
INSERT INTO album.tag (tag_ID,type,name) values (37, 'yolo','スケートボード');
INSERT INTO album.tag (tag_ID,type,name) values (38, 'yolo','サーフボード');
INSERT INTO album.tag (tag_ID,type,name) values (39, 'yolo','テニスラケット');
INSERT INTO album.tag (tag_ID,type,name) values (40, 'yolo','ボトル');
INSERT INTO album.tag (tag_ID,type,name) values (41, 'yolo','ワイングラス');
INSERT INTO album.tag (tag_ID,type,name) values (42, 'yolo','カップ');
INSERT INTO album.tag (tag_ID,type,name) values (43, 'yolo','フォーク');
INSERT INTO album.tag (tag_ID,type,name) values (44, 'yolo','ナイフ');
INSERT INTO album.tag (tag_ID,type,name) values (45, 'yolo','スプーン');
INSERT INTO album.tag (tag_ID,type,name) values (46, 'yolo','ボウル');
INSERT INTO album.tag (tag_ID,type,name) values (47, 'yolo','バナナ');
INSERT INTO album.tag (tag_ID,type,name) values (48, 'yolo','りんご');
INSERT INTO album.tag (tag_ID,type,name) values (49, 'yolo','サンドイッチ');
INSERT INTO album.tag (tag_ID,type,name) values (50, 'yolo','オレンジ');
INSERT INTO album.tag (tag_ID,type,name) values (51, 'yolo','ブロッコリー');
INSERT INTO album.tag (tag_ID,type,name) values (52, 'yolo','ニンジン');
INSERT INTO album.tag (tag_ID,type,name) values (53, 'yolo','ホットドッグ');
INSERT INTO album.tag (tag_ID,type,name) values (54, 'yolo','ピザ');
INSERT INTO album.tag (tag_ID,type,name) values (55, 'yolo','ドーナツ');
INSERT INTO album.tag (tag_ID,type,name) values (56, 'yolo','ケーキ');
INSERT INTO album.tag (tag_ID,type,name) values (57, 'yolo','椅子');
INSERT INTO album.tag (tag_ID,type,name) values (58, 'yolo','ソファー');
INSERT INTO album.tag (tag_ID,type,name) values (59, 'yolo','鉢植え');
INSERT INTO album.tag (tag_ID,type,name) values (60, 'yolo','ベッド');
INSERT INTO album.tag (tag_ID,type,name) values (61, 'yolo','ダイニングテーブル');
INSERT INTO album.tag (tag_ID,type,name) values (62, 'yolo','トイレ');
INSERT INTO album.tag (tag_ID,type,name) values (63, 'yolo','テレビ');
INSERT INTO album.tag (tag_ID,type,name) values (64, 'yolo','ラップトップ');
INSERT INTO album.tag (tag_ID,type,name) values (65, 'yolo','ねずみ');
INSERT INTO album.tag (tag_ID,type,name) values (66, 'yolo','リモート');
INSERT INTO album.tag (tag_ID,type,name) values (67, 'yolo','キーボード');
INSERT INTO album.tag (tag_ID,type,name) values (68, 'yolo','携帯電話');
INSERT INTO album.tag (tag_ID,type,name) values (69, 'yolo','電子レンジ');
INSERT INTO album.tag (tag_ID,type,name) values (70, 'yolo','オーブン');
INSERT INTO album.tag (tag_ID,type,name) values (71, 'yolo','トースター');
INSERT INTO album.tag (tag_ID,type,name) values (72, 'yolo','シンク');
INSERT INTO album.tag (tag_ID,type,name) values (73, 'yolo','冷蔵庫');
INSERT INTO album.tag (tag_ID,type,name) values (74, 'yolo','本');
INSERT INTO album.tag (tag_ID,type,name) values (75, 'yolo','クロック');
INSERT INTO album.tag (tag_ID,type,name) values (76, 'yolo','花瓶');
INSERT INTO album.tag (tag_ID,type,name) values (77, 'yolo','はさみ');
INSERT INTO album.tag (tag_ID,type,name) values (78, 'yolo','テディベア');
INSERT INTO album.tag (tag_ID,type,name) values (79, 'yolo','ヘアドライヤー');
INSERT INTO album.tag (tag_ID,type,name) values (80, 'yolo','歯ブラシ');
