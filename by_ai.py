import pygame
import random
import time

# Game environment constants
CELL_WIDTH = 10
CELL_HEIGHT = 10
CELL_AMOUNT_X = 100
CELL_AMOUNT_Y = 50
SCREEN_WIDTH = CELL_WIDTH * CELL_AMOUNT_X + (CELL_AMOUNT_X - 1)
SCREEN_HEIGHT = CELL_HEIGHT * CELL_AMOUNT_Y + (CELL_AMOUNT_Y - 1)

GRID_COLOR = "white"
CELL_COLOR = "black"
BG_COLOR = (201, 201, 201)

# 预计算网格线
V_GRID_LINES = tuple(
    (((CELL_WIDTH + 1) * i, 0), ((CELL_WIDTH + 1) * i, SCREEN_HEIGHT))
    for i in range(1, CELL_AMOUNT_X)
)

H_GRID_LINES = tuple(
    ((0, (CELL_HEIGHT + 1) * i), (SCREEN_WIDTH, (CELL_HEIGHT + 1) * i))
    for i in range(1, CELL_AMOUNT_Y)
)


class Cell:
    def __init__(self, index: int, alive: bool = False) -> None:
        self.index = index
        self.alive = alive
        self.line_num, self.x_pos = divmod(self.index, CELL_AMOUNT_X)
        self.neighbourhoods = self._calculate_neighbourhoods()

    def _calculate_neighbourhoods(self):
        """计算细胞的邻居索引，更简洁的方式"""
        neighbours = []
        
        # 计算可能的相对位置
        for dy in [-1, 0, 1]:
            new_y = self.line_num + dy
            if new_y < 0 or new_y >= CELL_AMOUNT_Y:
                continue
                
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:  # 跳过自身
                    continue
                    
                new_x = self.x_pos + dx
                if new_x < 0 or new_x >= CELL_AMOUNT_X:
                    continue
                    
                # 计算邻居索引
                neighbour_index = new_y * CELL_AMOUNT_X + new_x
                neighbours.append(neighbour_index)
                
        return tuple(neighbours)

    @property
    def rect_pos(self):
        left = self.x_pos * (CELL_WIDTH + 1) + 1
        top = self.line_num * (CELL_HEIGHT + 1) + 1
        width = CELL_WIDTH
        height = CELL_HEIGHT
        return (left, top, width, height)

    def fill(self, surface: pygame.Surface, color=CELL_COLOR):
        if self.alive:
            pygame.draw.rect(surface=surface, color=color, rect=self.rect_pos)
            
    def clone(self):
        """创建细胞的深拷贝"""
        return Cell(self.index, self.alive)


def create_cells(random_init=True):
    """创建所有细胞"""
    if random_init:
        return [Cell(i, bool(random.randint(0, 1))) for i in range(CELL_AMOUNT_X * CELL_AMOUNT_Y)]
    else:
        return [Cell(i, False) for i in range(CELL_AMOUNT_X * CELL_AMOUNT_Y)]


def update_cells(current_cells):
    """根据生命游戏规则更新细胞状态"""
    next_cells = [cell.clone() for cell in current_cells]
    
    for i, cell in enumerate(current_cells):
        alive_neighbours = sum(1 for n_idx in cell.neighbourhoods if current_cells[n_idx].alive)
        
        if cell.alive:
            # 规则1: 活细胞周围少于2个活细胞，死亡（孤独）
            # 规则2: 活细胞周围2-3个活细胞，存活
            # 规则3: 活细胞周围超过3个活细胞，死亡（过度拥挤）
            next_cells[i].alive = (alive_neighbours == 2 or alive_neighbours == 3)
        else:
            # 规则4: 死细胞周围正好有3个活细胞，复活（繁殖）
            next_cells[i].alive = (alive_neighbours == 3)
            
    return next_cells


def draw_grid(screen):
    """绘制网格线"""
    for h_line in H_GRID_LINES:
        pygame.draw.line(screen, GRID_COLOR, h_line[0], h_line[1])
    for v_line in V_GRID_LINES:
        pygame.draw.line(screen, GRID_COLOR, v_line[0], v_line[1])


def main():
    # pygame初始化
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    
    # 游戏状态
    running = True
    paused = False
    update_interval = 0.2  # 更新间隔（秒）
    last_update_time = time.time()
    
    # 初始化细胞
    current_cells = create_cells(random_init=True)
    
    # 主循环
    while running:
        current_time = time.time()
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # 重置游戏
                    current_cells = create_cells(random_init=True)
                elif event.key == pygame.K_c:
                    # 清空游戏
                    current_cells = create_cells(random_init=False)
                elif event.key == pygame.K_UP:
                    # 加快速度
                    update_interval = max(0.05, update_interval - 0.05)
                elif event.key == pygame.K_DOWN:
                    # 减慢速度
                    update_interval = min(1.0, update_interval + 0.05)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 点击切换细胞状态
                pos = pygame.mouse.get_pos()
                cell_x = pos[0] // (CELL_WIDTH + 1)
                cell_y = pos[1] // (CELL_HEIGHT + 1)
                if 0 <= cell_x < CELL_AMOUNT_X and 0 <= cell_y < CELL_AMOUNT_Y:
                    idx = cell_y * CELL_AMOUNT_X + cell_x
                    current_cells[idx].alive = not current_cells[idx].alive
        
        # 清屏
        screen.fill(BG_COLOR)
        
        # 绘制网格
        draw_grid(screen)
        
        # 绘制细胞
        for cell in current_cells:
            cell.fill(screen)
        
        # 更新游戏状态
        if not paused and (current_time - last_update_time) >= update_interval:
            current_cells = update_cells(current_cells)
            last_update_time = current_time
        
        # 显示状态信息
        status_text = f"{'暂停中' if paused else '运行中'} | 速度: {1/update_interval:.1f}帧/秒 | 空格:暂停/继续 | R:重置 | C:清空 | ↑↓:调整速度"
        status_surface = font.render(status_text, True, (0, 0, 0))
        screen.blit(status_surface, (10, 10))
        
        # 更新显示
        pygame.display.flip()
        clock.tick(60)  # 限制FPS为60
    
    pygame.quit()


if __name__ == "__main__":
    main()
