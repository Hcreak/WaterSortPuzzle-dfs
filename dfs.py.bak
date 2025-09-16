# coding=utf-8

# import cv2
from PIL import Image  # 改为PIL 代替openCV

SIZE = 4
vm = [ [] for i in range(14) ] # 14个试管
visit = [] # 放置出现过的vm状态 改进：存储vm的哈希值
DEEP_MAX = 50 # 递归深度阈值
deep_list = [] # 以正向存储正解

x = [ 92+i*94 for i in range(7) ]
y1 = [ 444+i*64 for i in range(SIZE) ]
y2 = [ 863+i*64 for i in range(SIZE) ]
y = y1+y2
# 深蓝 紫 深绿 棕 红 灰 浅绿 粉红 浅蓝 橙 翠绿 黄
color = [65, 74, 78, 83, 92, 100, 130, 140, 151, 159, 178, 211]
color_RGB = [(56, 46, 187, 255), (105, 47, 142, 255), (46, 99, 56, 255), (119, 76, 26, 255), (181, 57, 45, 255), (99, 100, 101, 255), (126, 149, 47, 255), (217, 103, 124, 255), (104, 161, 223, 255), (219, 144, 81, 255), (129, 211, 133, 255), (237, 219, 109, 255)]

def Init(path="",image=""):
    # image = cv2.imread (path,0)
    if path:
        image = Image.open(path).convert('L')
    for i in range(8):
        for j in range(7):
            vmi = j+(i>=4)*7
            # c = image[x[i],y[j]]
            c = image.getpixel((x[j],y[i]))

            # 颜色模糊
            for n in range(c-1,c+2):
                if n in color:
                    vm[vmi].insert(0, n)
                    break

def oneCol(vi):   # 判断单个试管中颜色是否一致
    for i in range(len(vi)):
        if vi[i] != vi[i-1]:
            return False
    return True

def end():   # 遍历每个试管 判断颜色是否一致
    for vi in vm:
        if not oneCol(vi):
            return False

    # 改进：加上判断是否有同一纯颜色的两个试管
    vi_end_list = []
    for vi in vm:
        if len(vi) != 0:
            if vi[0] in vi_end_list:
                return False
            else:
                vi_end_list.append(vi[0])
    return True

def canPour(i,j):
    if i == j:    # 同一试管防呆
        return False

    si = len(vm[i])
    sj = len(vm[j])
    if si == 0 or sj == SIZE:   # 源试管为空或目标试管满
        return False
    if sj == 0:                   # 若目标试管为空：
        return not oneCol(vm[i])  # 源试管若已完成则没必要倒了 反之则可以用空试管倒腾 

    ci = vm[i][si-1]
    cj = vm[j][sj-1]
    if ci != cj:   # 主要逻辑 源试管与目标试管栈尾颜色判断
        return False

    # 同一颜色色块是一起倒的 检出要倒的色块数量
    num = 0
    # for like C language style, range NB 666! 
    for k in range(si-1, 0, -1):
        if vm[i][k] == ci:
            num += 1
    return sj + num <= SIZE   # 检查目标试管剩余能否放下要倒的色块数

def pour(i,j):   # 返回倒的块数(同颜色倒多块)
    x = 0
    while canPour(i,j):
        it = vm[i].pop()
        vm[j].append(it)
        x += 1
    return x

def pour_f(i,j,num):   # 按照倒的块数回滚状态
    while num:
        it = vm[j].pop()
        vm[i].append(it)
        num -= 1

def dfs(deep):
    # 将vm状态化为哈希值 判断是否存在过此状态 若存在直接抛出
    vm_hash = hash(str(vm))
    if vm_hash in visit:
        return False
    visit.append(vm_hash)

    # 若每个试管颜色均一致 或达到阈值深度 即视作成功
    if end() or deep > DEEP_MAX:
        return True

    # i为倒出的试管 j为被倒入的试管
    for i in range(len(vm)):
        for j in range(len(vm)):
            if not canPour(i,j):
                continue

            x = pour(i,j)
            if dfs(deep+1):
                # print "deep = " + str(deep) + " from " + str(i) + " to " + str(j)
                action = (i,j)
                deep_list.insert(0,action)
                return True
            pour_f(i,j,x)
    return False

if __name__ == '__main__':
    # Init(path = "example/IMG_5162.PNG")
    # print "Start: " + str(vm)

    # dfs(0)
    # for deep in range(len(deep_list)):
    #     i = deep_list[deep][0]
    #     j = deep_list[deep][1]
    #     print "deep = " + str(deep) + " from " + str(i) + " to " + str(j)

    # print "End: " + str(vm)

    path = "1337.jpg"
    image = Image.open(path).convert('L')
    # image = Image.open(path)

    m = {}
    for i in x:
        for j in y:
            c = image.getpixel((i,j))

            # 颜色模糊
            for n in range(c-1,c+2):
                if m.has_key(n):
                    m[n] += 1
                    break
            else:
                m[c] = 1

    for k,v in m.items():
        print str(k) + '\t' + str(v)

    for k,v in m.items():
        if v != 4:
            del m[k]
    print len(m)

    # # cl = m.keys()
    # # cl.sort()
    # # print cl
    
    # rgb_gray_map = {}
    # for k in m.keys():
    #     gray = int(k[0]*0.299 + k[1]*0.587 + k[2]*0.114)
    #     rgb_gray_map[gray] = k
    
    # image = Image.new('RGB', (60*len(rgb_gray_map), 60), (255, 255, 255))
    # from PIL import ImageDraw
    # draw = ImageDraw.Draw(image)

    # cl = []
    # for i in sorted(rgb_gray_map):
    #     cl.append(rgb_gray_map[i])

    # print cl
    # for i in range(len(cl)):
    #     x0 = 60 * i
    #     x1 = x0 + 60
    #     draw.rectangle([(x0, 0), (x1, 60)], fill=cl[i])
    
    # image.show()
    # image.save('code.jpg', 'jpeg')
