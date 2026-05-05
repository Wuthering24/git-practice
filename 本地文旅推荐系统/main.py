import json
import requests
import time
import matplotlib.pyplot as plt

# 设置文件路径
TOURISM_DATA_PATH = r"C:\Users\16338\OneDrive\Desktop\本地文旅推荐系统\tourism_data.json"
CONFIG_PATH = r"C:\Users\16338\OneDrive\Desktop\本地文旅推荐系统\config.json"

# 设置中文显示
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def load_tourism_data(file_path=TOURISM_DATA_PATH):  
    """
    加载本地文旅数据集
    :param file_path: 数据集文件路径
    :return: 解析后的字典数据，失败则返回空字典
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"成功加载数据集，包含景点{len(data.get('scenic_spots', []))}条、"
              f"美食{len(data.get('food', []))}条、民宿{len(data.get('homestay', []))}条")
        return data
    except FileNotFoundError:
        print(f"错误: 未找到数据集文件 {file_path}")
        return {}
    except json.JSONDecodeError:
        print("错误: JSON文件格式错误，请检查")
        return {}

def load_api_config(file_path=CONFIG_PATH):  # 修改这里
    """加载API密钥配置"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载配置失败: {e}")
        return {}

def ai_intent_analysis(user_input, model="ERNIE-Speed-8K", max_retry=3):
    """
    调用百度文心一言API解析用户意图
    :param user_input: 用户输入的需求文本
    :param model: 使用的模型
    :param max_retry: 最大重试次数
    :return: 解析后的关键词字典，失败则返回None
    """
    config = load_api_config()
    api_key = config.get("baidu_api", {}).get("api_key")
    
    if not api_key:
        print("错误: 未配置百度API密钥")
        return None
    
    # 使用新的API调用方式（直接使用API Key）
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = (
        "请解析以下用户需求，提取核心关键词，按JSON格式返回，仅返回JSON，不要其他内容:\n"
        f"用户需求: {user_input}\n"
        '返回格式: {"region": "地域", "type": "scenic_spots/food/homestay", "price": "价格特征", "tags": ["特色1", "特色2"]}，'
        "其中type标签仅在scenic_spots/food/homestay三者中选一个,不要携带任何多余的解释说明"
    )
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # 降低随机性，确保输出稳定
    }
    
    for retry in range(max_retry):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # 检查API返回错误
            if "error_code" in data:
                print(f"API返回错误: {data['error_msg']}")
                return None
                
            content = data["result"]
            
            # 清理返回内容，提取JSON部分
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            intent_dict = json.loads(content)
            return intent_dict
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败，重试 {retry + 1}/{max_retry}: {e}")
            if retry == max_retry - 1:
                return None
            time.sleep(2)
        except Exception as e:
            print(f"API调用失败，重试 {retry + 1}/{max_retry}: {e}")
            if retry == max_retry - 1:
                return None
            time.sleep(2)
    
    return None

# ==================== 降级方案模块 ====================
def manual_intent_analysis(user_input):
    """
    手动关键词匹配(AI接口降级方案)
    :param user_input: 用户输入的需求文本
    :return: 解析后的关键词字典
    """
    # 预定义关键词字典(针对成都地区)
    region_dict = {
        "成都": ["成都", "蓉", "锦城", "天府"],
        "成华区": ["成华", "熊猫基地"],
        "青羊区": ["青羊", "宽窄巷子", "锦里", "文殊院"],
        "锦江区": ["锦江", "春熙路", "太古里"],
        "武侯区": ["武侯", "武侯祠"],
        "都江堰市": ["都江堰", "青城山"]
    }
    
    type_dict = {
        "scenic_spots": ["景点", "景区", "公园", "打卡", "拍照", "游玩", "观光", "旅游"],
        "food": ["美食", "吃", "餐厅", "小吃", "川菜", "火锅", "美食", "餐馆", "饭店"],
        "homestay": ["民宿", "住宿", "酒店", "住", "客栈", "宾馆", "旅店"]
    }
    
    price_dict = {
        "性价比高": ["性价比", "便宜", "实惠", "划算", "经济"],
        "免费": ["免费", "不花钱", "0元"],
        "高价": ["贵", "高端", "轻奢", "豪华", "高级"]
    }
    
    # 通用特色标签
    tags_list = ["历史", "拍照", "亲子", "本地特色", "夜游", "自然", "文化", "休闲", "购物", "美食", "网红", "老字号"]
    
    # 初始化解析结果
    intent_dict = {
        "region": "",
        "type": "",
        "price": "",
        "tags": []
    }
    
    # 1.匹配地域
    for region, keywords in region_dict.items():
        if any(key in user_input for key in keywords):
            intent_dict["region"] = region
            break
    
    # 2.匹配类型
    for type_name, keywords in type_dict.items():
        if any(key in user_input for key in keywords):
            intent_dict["type"] = type_name
            break
    
    # 3.匹配价格特征
    for price, keywords in price_dict.items():
        if any(key in user_input for key in keywords):
            intent_dict["price"] = price
            break
    
    # 4.匹配特色标签
    for tag in tags_list:
        if tag in user_input:
            intent_dict["tags"].append(tag)
    
    return intent_dict

def calculate_match_score(item, intent_dict):
    """
    计算单条数据的匹配度
    :param item: 单条文旅数据(字典)
    :param intent_dict: 解析后的意图字典
    :return: 匹配度分数(0-10分)
    """
    score = 0
    
    # 1.地域匹配(3分)
    if intent_dict["region"] and item["region"] == intent_dict["region"]:
        score += 3
    elif intent_dict["region"] and intent_dict["region"] in ["成都", "蓉"]:
        # 如果只是指定成都，给基础分
        score += 1
    
    # 2.价格匹配(2分)
    if intent_dict["price"]:
        if intent_dict["price"] == "性价比高" and 0 < item["price"] < 50:
            score += 2
        elif intent_dict["price"] == "免费" and item["price"] == 0:
            score += 2
        elif intent_dict["price"] == "高价" and item["price"] > 200:
            score += 2
    
    # 3.标签匹配(最多5分，每个标签1分)
    tag_match_count = len(set(intent_dict["tags"]) & set(item["tags"]))
    score += min(tag_match_count, 5)
    
    return score

def personalized_recommend(tourism_data, intent_dict, top_n=5):
    """
    个性化推荐核心函数
    :param tourism_data: 本地文旅数据集
    :param intent_dict: 解析后的意图字典
    :param top_n: 推荐结果数量
    :return: 排序后的推荐结果列表
    """
    # 1.筛选数据类型
    data_type = intent_dict.get("type")
    
    if not data_type or data_type not in tourism_data:
        print("未匹配到具体类型，返回所有类型数据")
        # 合并所有类型数据
        all_data = []
        for key in ["scenic_spots", "food", "homestay"]:
            all_data.extend(tourism_data.get(key, []))
        target_data = all_data
    else:
        target_data = tourism_data[data_type]
    
    # 2.计算每条数据的综合得分(匹配度 × 评分)
    for item in target_data:
        match_score = calculate_match_score(item, intent_dict)
        item["match_score"] = match_score
        item["comprehensive_score"] = match_score * item["score"]
    
    # 3.按综合得分降序排序
    sorted_data = sorted(target_data, key=lambda x: x["comprehensive_score"], reverse=True)
    
    # 4.返回前N条结果
    return sorted_data[:top_n]

# ==================== 可视化模块 ====================
def visualize_recommendations(recommendations):
    """
    可视化推荐结果
    :param recommendations: 推荐结果列表
    """
    if not recommendations:
        print("无推荐结果，无需可视化")
        return
    
    # 1.提取可视化所需数据
    names = [item["name"] for item in recommendations]
    scores = [item["score"] for item in recommendations]
    prices = [item["price"] for item in recommendations]
    
    # 2.绘制评分分布柱状图
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    bars = plt.bar(range(len(names)), scores, color="#4CAF50", alpha=0.7)
    plt.title("推荐结果评分分布")
    plt.xlabel("文旅项目")
    plt.ylabel("评分(0-5)")
    plt.xticks(range(len(names)), names, rotation=45, ha="right")
    plt.ylim(0, 5.5)
    
    # 在柱子上添加数值标签
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{score:.1f}', ha='center', va='bottom')
    
    # 3.绘制价格区间饼图
    plt.subplot(1, 2, 2)
    
    # 划分价格区间
    price_ranges = {
        "免费(0元)": 0,
        "低价(0-50元)": 0,
        "中价(50-200元)": 0,
        "高价(>200元)": 0
    }
    
    for price in prices:
        if price == 0:
            price_ranges["免费(0元)"] += 1
        elif 0 < price <= 50:
            price_ranges["低价(0-50元)"] += 1
        elif 50 < price <= 200:
            price_ranges["中价(50-200元)"] += 1
        else:
            price_ranges["高价(>200元)"] += 1
    
    # 过滤无数据的区间
    pie_data = {k: v for k, v in price_ranges.items() if v > 0}
    
    if pie_data:
        plt.pie(pie_data.values(), labels=pie_data.keys(), autopct="%1.1f%%", 
                startangle=90, colors=["#FF9999", "#66B2FF", "#99FF99", "#FFD700"])
        plt.title("推荐结果价格区间分布")
    else:
        plt.text(0.5, 0.5, "无价格数据", ha='center', va='center', transform=plt.gca().transAxes)
        plt.title("价格分布(无数据)")
    
    # 4.保存图片
    plt.tight_layout()
    plt.savefig("recommendation_visualization.png", dpi=300, bbox_inches="tight")
    plt.show()

# ==================== 主系统整合 ====================
def main():
    """系统主函数"""
    print("=" * 20 + " 成都本地文旅智能推荐系统 " + "=" * 20)
    
    # 1.加载数据集
    print("正在加载成都文旅数据集...")
    tourism_data = load_tourism_data()
    if not tourism_data:
        print("数据集加载失败，程序退出")
        return
    
    # 2.获取用户输入
    user_input = input("\n请输入你的文旅需求(如: 想找成都性价比高的火锅店): ").strip()
    if not user_input:
        print("输入不能为空")
        return
    
    # 3.意图解析(优先AI，失败则降级)
    print("\n正在解析你的需求...")
    intent_dict = ai_intent_analysis(user_input)
    
    if not intent_dict:
        print("AI解析失败，启用手动关键词匹配...")
        intent_dict = manual_intent_analysis(user_input)
    
    print(f"需求解析结果: {intent_dict}")
    
    # 4.个性化推荐
    print("\n正在为你推荐...")
    recommendations = personalized_recommend(tourism_data, intent_dict, top_n=5)
    
    if not recommendations:
        print("未找到匹配的文旅资源")
        return
    
    # 5.输出推荐结果
    print("\n" + "=" * 20 + " 推荐结果 " + "=" * 20)
    for idx, item in enumerate(recommendations, 1):
        print(f"""
{idx}. 名称: {item['name']}
   地址: {item['address']}
   评分: {item['score']} ⭐
   价格: {item['price']} 元
   特色: {', '.join(item['tags'])}
   匹配度: {item['match_score']} 分
   综合得分: {item['comprehensive_score']:.2f}
""")
    
    # 6.可视化展示
    print("正在生成可视化图表...")
    visualize_recommendations(recommendations)
    print("可视化图表已保存为 recommendation_visualization.png")

if __name__ == "__main__":
    main()