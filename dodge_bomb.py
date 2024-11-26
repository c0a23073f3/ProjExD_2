import os
import sys
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect)->tuple[bool,bool]:
    """
    引数で与えられたRectが画面の中か外か判定する。
    引数:こうかとんRectか爆弾Rect
    戻り値:こうかとんRect　OR　爆弾Rect
    """
    yoko, = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の設定
    bb_img = pg.Surface((20, 20), pg.SRCALPHA)  # 爆弾Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明化
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        # キャラクターの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        # 爆弾の移動
        bb_rct.move_ip(vx, vy)
        if bb_rct.left < 0 or bb_rct.right > WIDTH:
            vx *= -1  # 横方向の反転
        if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
            vy *= -1  # 縦方向の反転

        # 描画
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(500)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
