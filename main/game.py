import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("똥피하기 (SUBERUNKER Style)")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (224, 224, 224) # #e0e0e0
BROWN = (139, 69, 19) # #8B4513
RED = (255, 68, 68)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
YELLOW = (255, 235, 59)
ORANGE = (255, 152, 0)
DARK_GRAY = (50, 50, 50)

# 폰트 설정 (한글 깨짐 방지 위해 기본 시스템 폰트 사용 시도)
try:
    font_large = pygame.font.SysFont("malgungothic", 60, True)
    font_medium = pygame.font.SysFont("malgungothic", 40, True)
    font_small = pygame.font.SysFont("malgungothic", 24, True)
except:
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 24)

# 난이도 데이터
DIFFICULTY_SETTINGS = {
    'Easy': {'base_speed': 3, 'interval': 30, 'speed_mult': 0.5, 'color': BLUE},
    'Normal': {'base_speed': 5, 'interval': 20, 'speed_mult': 1.0, 'color': GREEN},
    'Hard': {'base_speed': 7, 'interval': 15, 'speed_mult': 1.5, 'color': ORANGE},
    'Hell': {'base_speed': 10, 'interval': 5, 'speed_mult': 2.0, 'color': RED},
}

class Player:
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.vx = 0
        self.speed = 0.5
        self.friction = 0.85
        self.max_speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.vx -= self.speed
        if keys[pygame.K_RIGHT]:
            self.vx += self.speed

        # 최대 속도 제한
        if self.vx > self.max_speed: self.vx = self.max_speed
        if self.vx < -self.max_speed: self.vx = -self.max_speed

        # 마찰
        self.vx *= self.friction
        
        # 이동 반영
        self.x += self.vx
        
        # 벽 충돌
        if self.x < 0:
            self.x = 0
            self.vx = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.vx = 0
            
        self.rect.x = int(self.x)

    def draw(self):
        # 졸라맨 그리기
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)
        
        # 머리
        pygame.draw.circle(screen, BLACK, (cx, int(self.y + 8)), 8, 2)
        
        # 몸통
        pygame.draw.line(screen, BLACK, (cx, int(self.y + 16)), (cx, int(self.y + 35)), 2)
        
        # 팔 (흔들림 효과)
        arm_offset = int(self.vx * 1.5)
        pygame.draw.line(screen, BLACK, (cx, int(self.y + 20)), (cx - 10 - arm_offset, int(self.y + 30)), 2)
        pygame.draw.line(screen, BLACK, (cx, int(self.y + 20)), (cx + 10 - arm_offset, int(self.y + 30)), 2)
        
        # 다리 (움직임 효과)
        leg_offset = int(self.vx * 1.5)
        if abs(self.vx) < 0.1: leg_offset = 0 # 정지 시 차렷
        pygame.draw.line(screen, BLACK, (cx, int(self.y + 35)), (cx - 8 + leg_offset, int(self.y + 50)), 2)
        pygame.draw.line(screen, BLACK, (cx, int(self.y + 35)), (cx + 8 - leg_offset, int(self.y + 50)), 2)

class Poop:
    def __init__(self, settings, current_diff_level):
        r = random.random()
        if r < 0.1: self.size = 30
        elif r < 0.3: self.size = 24
        else: self.size = 15
        
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = -self.size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        base_speed = settings['base_speed']
        
        # 속도 계산 Logic (Web 버전과 동일하게)
        rand_speed = random.uniform(base_speed/2, base_speed)
        size_factor = 30 / self.size
        diff_factor = (current_diff_level * settings['speed_mult'])
        
        self.speed = (rand_speed * size_factor * 0.6) + diff_factor
        
    def update(self):
        self.y += self.speed
        self.rect.y = int(self.y)

    def draw(self):
        # 똥 그리기 (3단 + 꼬리 - 비율 수정: 납작하게)
        radius = self.size / 2
        cx, cy = self.rect.centerx, self.rect.centery
        
        # 1단 (맨 아래 - 더 넓고 납작하게)
        # width: radius * 2, height: radius * 0.8 (기존 1.2에서 축소)
        pygame.draw.ellipse(screen, BROWN, (cx - radius, cy, radius * 2, radius * 0.8))
        
        # 2단 (중간)
        # width: radius * 1.6, height: radius * 0.7 (기존 1.0에서 축소)
        pygame.draw.ellipse(screen, BROWN, (cx - radius * 0.8, cy - radius * 0.5, radius * 1.6, radius * 0.7))
        
        # 3단 (위)
        # width: radius, height: radius * 0.6 (기존 0.8에서 축소)
        pygame.draw.ellipse(screen, BROWN, (cx - radius * 0.5, cy - radius * 0.9, radius, radius * 0.6))
        
        # 꼬리 (삼각형 높이 축소)
        points = [
            (cx - radius * 0.2, cy - radius * 0.8),
            (cx + radius * 0.2, cy - radius * 0.8),
            (cx, cy - radius * 1.4) # 기존 1.5에서 살짝 낮춤
        ]
        pygame.draw.polygon(screen, BROWN, points)
        
        # 하이라이트
        highlight_rect = (cx - radius * 0.3, cy, radius * 0.4, radius * 0.2)
        pygame.draw.ellipse(screen, (255, 255, 255, 80), highlight_rect) # Alpha 적용 안됨 (Surface 필요), 그냥 밝은색 그리기
        
        # Pygame 기본 draw는 alpha 지원이 안되므로 간단히 흰색 점 찍기
        pygame.draw.circle(screen, (255, 230, 230), (int(cx - radius * 0.3), int(cy)), 2)


def draw_text_centered(text, font, color, center_y):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, center_y))
    screen.blit(text_surface, rect)
    return rect

def start_screen():
    while True:
        screen.fill(BLACK)
        draw_text_centered("똥피하기", font_large, YELLOW, 250)
        draw_text_centered("SUBERUNKER Style", font_small, GRAY, 310)
        
        btn_rect = pygame.Rect(0, 0, 200, 60)
        btn_rect.center = (SCREEN_WIDTH // 2, 500)
        pygame.draw.rect(screen, GREEN, btn_rect, border_radius=10)
        draw_text_centered("게임 시작", font_medium, WHITE, 500)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return 'difficulty'
        
        pygame.display.flip()
        clock.tick(60)

def difficulty_screen():
    btn_rects = {}
    y_pos = 300
    
    while True:
        screen.fill(BLACK)
        draw_text_centered("난이도 선택", font_large, WHITE, 150)
        
        mouse_pos = pygame.mouse.get_pos()
        
        items = list(DIFFICULTY_SETTINGS.items())
        
        for i, (name, settings) in enumerate(items):
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (SCREEN_WIDTH // 2, 300 + i * 80)
            btn_rects[name] = rect
            
            color = settings['color']
            # Hover 효과
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, color, rect, border_radius=10)
                pygame.draw.rect(screen, WHITE, rect, 3, border_radius=10)
            else:
                pygame.draw.rect(screen, color, rect, border_radius=10)
                
            draw_text_centered(name, font_medium, BLACK if name != 'Hell' else WHITE, 300 + i * 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in btn_rects.items():
                    if rect.collidepoint(event.pos):
                        return name
        
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(score):
    while True:
        # 반투명 배경 효과 (직전 화면 위에 그리기 위해 loop 밖에서 스크린샷 찍는게 좋지만, 간단히 구현)
        # 여기서는 그냥 검은 배경
        screen.fill(BLACK)
        
        draw_text_centered("YOU DIED", font_large, RED, 250)
        draw_text_centered(f"버틴 시간: {score:.2f}초", font_medium, WHITE, 350)
        
        btn_rect = pygame.Rect(0, 0, 200, 60)
        btn_rect.center = (SCREEN_WIDTH // 2, 550)
        pygame.draw.rect(screen, GREEN, btn_rect, border_radius=10)
        draw_text_centered("처음으로", font_medium, WHITE, 550)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return 'menu'
        
        pygame.display.flip()
        clock.tick(60)

def play_game(difficulty_name):
    settings = DIFFICULTY_SETTINGS[difficulty_name]
    player = Player()
    poops = []
    
    start_ticks = pygame.time.get_ticks()
    poop_timer = 0
    difficulty_level = 1
    
    # 설정값 로드
    poop_interval = settings['interval']
    
    running = True
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

        # 상태 업데이트
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # 시간 계산
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        
        # 난이도 자동 증가 (5초마다)
        difficulty_level = 1 + int(elapsed_seconds / 5)
        
        # 생성 간격 계산
        current_interval = settings['interval'] - (difficulty_level * (1 if difficulty_name == 'Hell' else 2))
        if current_interval < 3: current_interval = 3
        
        # 똥 생성
        poop_timer += 1
        if poop_timer > current_interval:
            poops.append(Poop(settings, difficulty_level))
            poop_timer = 0
            
        # 똥 업데이트 및 충돌 검사
        player_hitbox = player.rect.inflate(-10, -5) # 히트박스 조금 작게
        
        for poop in poops[:]:
            poop.update()
            if poop.y > SCREEN_HEIGHT + 50:
                poops.remove(poop)
                continue
            
            # 충돌 로직
            # 원형 충돌 판정을 위해 거리 계산 사용
            p_center = player_hitbox.center
            poop_center = poop.rect.center
            dist_sq = (p_center[0] - poop_center[0])**2 + (p_center[1] - poop_center[1])**2
            radius_sum = (player.width/2) + (poop.size/2 * 0.8) # 판정 조금 후하게
            
            if dist_sq < radius_sum**2:
                return elapsed_seconds # 죽음, 점수 반환

        # 그리기
        screen.fill(GRAY)
        player.draw()
        for poop in poops:
            poop.draw()
            
        # UI (점수판)
        score_text = font_medium.render(f"{elapsed_seconds:.2f}초", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 40))
        # 점수판 배경
        bg_rect = score_rect.inflate(40, 20)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=15)
        screen.blit(score_text, score_rect)
        
        pygame.display.flip()
        clock.tick(60)

# 메인 루프
def main():
    state = 'menu'
    while True:
        if state == 'menu':
            res = start_screen()
            if res == 'quit': break
            elif res == 'difficulty': state = 'difficulty'
            
        elif state == 'difficulty':
            diff = difficulty_screen()
            score = play_game(diff)
            if score == 'quit': break
            else:
                state = 'gameover'
                final_score = score
                
        elif state == 'gameover':
            res = game_over_screen(final_score)
            if res == 'quit': break
            elif res == 'menu': state = 'menu'

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
