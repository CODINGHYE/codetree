import sys
import copy
from collections import deque

sys.stdin = open('input.txt', 'r')
sys.stdout =open('output.txt', 'w')

def debug(grid):
    for row in grid:
        print(row)
    print("------------------------")

'''
병원을 선택
병원들 중 m개를 랜덤으로 고름
하지만 이미 있는 조합이라면 continue
없는 조합이라면 그 조합을 반환
'''
def select_hospital(hospitals, candis):
    selected = []
    def select(start):
        # m개의 병원을 선택했다면 하나의 조합 완성
        if len(selected) == m:
            candis.add(tuple(selected))
            return
        # 현재 선택한 병원보다 뒤에 있는 병원만 선택
        for i in range(start, len(hospitals)):
            selected.append(i)
            select(i + 1)
            selected.pop()
    select(0)
    return candis

'''
바이러스 제거
1. 선택한 m개의 각 병원에서 상하좌우 탐색하며 모든 거리를 구함
2. 한 지역에 대해 탐색한 거리가 이전 병원보다 작다면 대체 크다면 그래도 냅둠
3. bfs는 각 지역마다 도달하는데 걸리는 시간을 구하는 것
4. 만약 모든 바이러스를 없애지 못했다면 -1 출력
'''
def in_range(r,c):
    return 0<=r<n and 0<=c<n

# def remove_virus(hospitals, grid, candis,times):
#     dirs = [(-1,0),(1,0),(0,-1),(0,1)]
#     for candi in candis:
#         rm_virus_cnt = 0
#         dists = [[10000] * n for _ in range(n)] # m개의 병원이 구한 거리 저장, 이전 병원이 구한 거리보다 작다면 업데이트
#         for idx in candi:
#             cur_r, cur_c = hospitals[idx]
#             que = deque() # 탐색가능한 지역과 거리를 업데이트함
#             visited = [[None] * n for _ in range(n)] # 탐색할 지역의 거리를 저장함
#             que.append((0, cur_r,cur_c))
#             visited[cur_r][cur_c] = 0
#             while que: # 지금 bfs는 탐색과 거리계산을 동시에 하고 있음 vistied에 병원을 지나간 거리를
#                 d,r,c = que.popleft()
#                 for dr,dc in dirs:
#                     nr, nc = r+dr, c+dc
#                     # 병원을 지나가도됨
#                     if in_range(nr,nc) and grid[nr][nc] !=1 and visited[nr][nc]==None:
#                         nd = d+1
#                         que.append((nd,nr,nc))
#                         # print(que)
#                         visited[nr][nc] = nd
#                         if grid[nr][nc] == 0 and dists[nr][nc] > nd: #이전 병원이 구한 거리보다 작다면 교체
#                             dists[nr][nc] = nd
#                             debug(dists)
#         max_time = -1
#         for row in dists:
#             for col in row:
#                 if col == 10000: continue
#                 max_time= max(col, max_time)
#                 rm_virus_cnt +=1 # 현재 candi에서 없앤 virus 수
#         if rm_virus_cnt == virus_cnt:
#             times.append(max_time)

'''
다시점 bfs: 각 병원에서 시작한 bfs의 탐색과 이동 비용은 같음
=> 병원에서 지역까지의 거리는 비교할 필요 없음
'''
# 한 candi에 대한 이동 시간 계산
def remove_virus(hospitals,grid, candi,times,virus_cnt):
    rm_cnt = virus_cnt
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    max_time = -1
    que = deque()
    visited = [[False]*n for _ in range(n)]
    distance = [[100000]* n for _ in range(n)]
    for idx in candi:
        r,c = hospitals[idx]
        # 각 병원의 시작점을 que에 넣음
        que.append((0,r,c))
        visited[r][c] = True
        distance[r][c] = 0
    while que:
        cur_d, cur_r, cur_c = que.popleft()
        for dr, dc in dirs:
            nr, nc = cur_r+dr, cur_c+dc
            if in_range(nr, nc) and grid[nr][nc]!= 1 and not visited[nr][nc]: #범위체크 탐색하지 못하는 조건 기준으로
                nd = cur_d + 1
                que.append((nd,nr,nc))
                visited[nr][nc] = True
                if grid[nr][nc] == 0: # 바이러스가 있는 곳이면 거리 저장
                    distance[nr][nc] = nd
                    rm_cnt -= 1 # 바이러스를 실제 제거 할때만 업데이트
                    # debug(distance)
                    max_time = max(nd,max_time)
    if rm_cnt == 0:
        times.add(max_time)

#-------------------------------------------------------------입력
n,m = map(int, input().split())
grid = [list(map(int,input().split())) for _ in range(n)]
hospitals = [] #각 병원의 고정된 위치
virus_cnt = 0
for i in range(n):
    for j in range(n):
        if grid[i][j] == 2:
            hospitals.append((i,j))
        if grid[i][j] == 0:
            virus_cnt += 1
if virus_cnt == 0:
    print(0)
    sys.exit()
    
candis = set() # 모든 m개 병원 조합 저장
times = set() # 모든 조합에 대한 시간 저장
#--------------------------------------------------------------메인
'''
1. 병원을 선택, 더이상 조합할 병원이 없다면 종료
2. 선택한 병원에 대해 bfs 탐색하며 시간 구하기
3. 그 결과 저장하기
4. 저장한 모든 조합의 거리중 가장 최소를 구함
'''
select_hospital(hospitals, candis)
for candi in candis:
    if virus_cnt == 0:
        print(0)
        break
    # debug(grid)
    remove_virus(hospitals,grid,candi,times, virus_cnt)

if len(times) > 0:
    print(min(times))
else:
    print(-1)
