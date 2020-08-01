from math import sqrt

def M_distance(vector1,vector2):
    TSum = sum([(vector1[i] - vector2[i]) for i in range(len(vector1))])
    return TSum

def Euclidean_distance(vector1,vector2):
    TSum = sum([pow((vector1[i] - vector2[i]),2) for i in range(len(vector1))])
    SSum = sqrt(TSum)
    return SSum

def yezi(clust):
    if clust.left == None and clust.right == None :
        return [clust.id]
    return yezi(clust.left) + yezi(clust.right)


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right  # 每次聚类都是一对数据，left保存其中一个数据，right保存另一个
        self.vec = vec  # 保存两个数据聚类后形成新的中心
        self.id = id
        self.distance = distance


def hcluster(blogwords, n):
    biclusters = [bicluster(vec=blogwords[i], id=i) for i in range(len(blogwords))]
    distances = {}
    flag = None;
    currentclusted = -1
    while (len(biclusters) > n):  # 假设聚成n个类
        min_val = 999999999999;  # Python的无穷大应该是inf
        biclusters_len = len(biclusters)
        for i in range(biclusters_len - 1):
            for j in range(i + 1, biclusters_len):
                if distances.get((biclusters[i].id, biclusters[j].id)) == None:
                    distances[(biclusters[i].id, biclusters[j].id)] = Euclidean_distance(biclusters[i].vec, biclusters[j].vec)
                d = distances[(biclusters[i].id, biclusters[j].id)]
                if d < min_val:
                    min_val = d
                    flag = (i, j)
        bic1, bic2 = flag  # 解包bic1 = i , bic2 = j
        newvec = [(biclusters[bic1].vec[i] + biclusters[bic2].vec[i]) / 2 for i in
                  range(len(biclusters[bic1].vec))]  # 形成新的类中心，平均
        newbic = bicluster(newvec, left=biclusters[bic1], right=biclusters[bic2], distance=min_val,
                           id=currentclusted)  # 二合一
        currentclusted -= 1
        del biclusters[bic2]  # 删除聚成一起的两个数据，由于这两个数据要聚成一起
        del biclusters[bic1]
        biclusters.append(newbic)  # 补回新聚类中心
        clusters = [yezi(biclusters[i]) for i in range(len(biclusters))]  # 深度优先搜索叶子节点，用于输出显示
    return biclusters, clusters