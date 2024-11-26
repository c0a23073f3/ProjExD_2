import os
import random
import sys
import time  # timeモジュールをインポート
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

"""
引数で与えられたRectが画面内に収まっているかどうかを判定する関数
引数:こうかとんRect or 爆弾Rect
戻り値：横方向と縦方向の判定結果タプル（画面内: True, 画面外: False）
"""

def check_bound(rct):
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen, kk_img):
    """
    ゲームオーバー時の画面表示
    引数: pg.Surfaceと、kk_img（こうかとん）
    戻り値: None
    """
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # 黒い半透明の背景
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # 泣いているこうかとん1
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    screen.blit(kk_img, kk_rct)

    # 泣いているこうかとん2
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    screen.blit(kk_img, kk_rct)

    screen.blit(text, text_rect)
    pg.display.update()

    # 5秒間停止させる☆
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の設定
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):  # 爆弾のサイズと加速度を段階的に増加
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
        bb_accs.append(r)
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        if kk_rct.colliderect(bb_rct):
            game_over(screen, kk_img)
            return

        screen.blit(bg_img, [0, 0])

        # キャラクター移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        # 画面外判定
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾の移動
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        # 時間経過で爆弾の拡大と加速を促します
        bb_img = bb_imgs[min(tmr // 500, 9)]
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]

        bb_rct.move_ip(avx, avy)

        # 描画
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
