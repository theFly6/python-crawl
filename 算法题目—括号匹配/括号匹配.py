def check_parentheses(s):
    left = []  # 存储左括号的下标
    right = []  # 存储右括号的下标
    for i, char in enumerate(s):
        if char == "(":
            left.append(i)  # 若为左括号，将下标加入left列表
        elif char == ")":
            if left:
                left.pop()  # 若为右括号且匹配左括号，从left列表中弹出对应的左括号
            else:
                right.append(i)  # 若为右括号但没有匹配的左括号，将下标加入right列表
                
    res = [' ']*len(s)  # 初始化结果列表，初始值为' '，即空格
    for i in left:
        res[i] = 'x'  # 将未匹配的左括号位置标记为'x'
    for i in right:
        res[i] = '?'  # 将未匹配的右括号位置标记为'?'

    print(s)  # 打印原始字符串
    print(''.join(res))  # 打印标记结果字符串


if __name__ == "__main__":
    inputs = [
        "bge)))))))))",
        "((IIII))))))))",
        "()()()()(uuu",
        "))))UUUU((()"
    ]

    for s in inputs:
        check_parentheses(s)

    """ 时间、空间复杂度分析：
    对于上述代码的时间复杂度分析如下：
    1. 第一个循环遍历输入字符串 s，时间复杂度为 O(n)，其中 n 为字符串 s 的长度。
    2. 第二个循环遍历 left 和 right 列表，总共不超过 n 次，时间复杂度为 O(n)。
    3. 剩余操作的时间复杂度是 O(n)。
    因此，总体时间复杂度为 O(n)。

    对于空间复杂度分析：
    1. left 和 right 数组的长度不超过字符串 s 的长度 n，因此空间复杂度为 O(n)。
    2. 结果列表 res 的空间复杂度也为 O(n)。
    3. 其他变量的空间复杂度是常数级别，忽略不计。
    综上所述，总体空间复杂度为 O(n)。

    因此，该代码的时间复杂度为 O(n)，空间复杂度为 O(n)。
    """
