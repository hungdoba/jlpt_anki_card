import csv
import requests
import re


def get_kanji():
    input_file = r'C:\Users\hungba\Documents\Programming\Python\2112-public-personal-tool-jlpt\anki_card.csv'
    output_file = 'updated_file.csv'

    with open(input_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    kanji_list_unique = []
    for row in rows:
        kanji = row['Kanji']
        kanji_list = re.findall(r'[\u4e00-\u9faf]', kanji)
        if len(kanji_list) > 0:
            kanji_list_unique.extend(kanji_list)
    print(list(set(kanji_list_unique)))


def get_hanviet(kanji):
    result = requests.get(
        f"https://jdict.net/api/v1/suggest?keyword={kanji}&keyword_position=start&type=kanji")
    hanviet = result.json()
    
    hanviet = hanviet.get('list')
    if hanviet is not None:
        if len(hanviet) > 0:
            hanviet = hanviet[0].get('hanviet')
            if hanviet is not None:
                return {kanji: hanviet}
            return {kanji: ''}
        return {kanji: ''}
    return {kanji: ''}

combined_dict = {'曲': 'KHÚC', '耳': 'NHĨ', '駆': 'KHU', '彰': 'CHƯƠNG', '調': 'ĐIỀU', '供': 'CUNG', '極': 'CỰC', '挫': 'TỎA', '志': 'CHÍ', '淑': 'THỤC', '名': 'DANH', '切': 'THIẾT', '推': 'SUY,THÔI', '来': 'LAI', '出': 'XUẤT', '繊': 'TIỆM', '臭': 'XÚ', '留': 'LƯU', '白': 'BẠCH', '本': 'BẢN,BỔN', '失': 'THẤT', '質': 'CHẤT', '討': 'THẢO', '強': 'CƯỜNG', '矯': 'KIỂU', '撃': 'KÍCH', '運': 'VẬN', '衛': 'VỆ', '概': 'KHÁI', '背': 'BỐI', '羨': '', '括': 'QUÁT', '鑑': 'GIÁM', '送': 'TỐNG', '式': 'THỨC', '笹': 'SẬY', '義': 'NGHĨA', '満': 'MÃN', '戒': 'GIỚI', '嘲': 'TRÀO', '代': 'ĐẠI', '景': 'CẢNH', '弾': 'ĐÀN,ĐẠN', '込': 'NHẬP', '行': 'HÀNH', '命': 'MỆNH', '先': 'TIÊN', '揮': 'HUY', '辟': 'BÍCH,TỊCH', '電': 'ĐIỆN', '塵': 'TRẦN', '手': 'THỦ', '徹': 'TRIỆT', '知': 'TRI', '棚': 'BẰNG', '仮': 'GIẢ', '停': 'ĐÌNH', '待': 'ĐÃI', '様': 'DẠNG', '算': 'TOÁN', '務': 'VỤ', '到': 'ĐÁO', '産': 'SẢN', '順': 'THUẬN', '断': 'ĐOẠN,ĐOÁN', '力': 'LỰC', '抱': 'BÃO', '着': 'TRƯỚC', '原': 'NGUYÊN', '瞑': '', '馴': 'THUẦN', '漬': 'TÝ', '視': 'THỊ', '臆': 'ỨC', ' 資': 'TƯ', '滑': 'HOẠT', '混': 'HỖN', '際': 'TẾ', '盛': 'THỊNH', '俯': 'PHỦ', '離': '', '観': 'QUAN', '替': 'THẾ', '用': 'DỤNG', '中': 'TRUNG', '平': 'BÌNH', '税': 'THUẾ', '能': 'NĂNG', '審': 'THẨM', '度': 'ĐỘ', '縁': 'DUYÊN', '似': 'TỰ', '朗': 'LÃNG', '級': 'CẤP', '私': 'TƯ', '活': 'HOẠT', '群': 'QUẦN', '業': '', '向': 'HƯỚNG', '憚': 'ĐẠN', '辛': 'TÂN', '紛': 'PHÂN', '告': 'CÁO', '天': 'THIÊN', '屋': 'ỐC', '始': 'THỦY', '相': 'TƯƠNG,TƯỚNG', '固': 'CỐ', '達': 'ĐẠT', '寄': 'KỲ', '壊': 'HOẠI', '直': 'TRỰC', '判': 'PHÁN', '灰': 'HÔI', '数': '', '妬': '', '傑': '', '雄': 'HÙNG', '声': 'THANH', '匹': 'THẤT', '春': 'XUÂN', '筋': 'CÂN', '投': 'ĐẦU', '粋': 'TÚY', '一': 'NHẤT', '踏': 'ĐẠP', '休': 'HƯU', '気': 'KHÍ', '慢': 'MẠN', '常': 'THƯỜNG', '正': 'CHÍNH', '永': 'VĨNH', '上': 'THƯỢNG', '妙': '', '釈': '', '掛': '', '則': '', '旨': 'CHỈ', '創': 'SÁNG', '衝': 'XUNG', '独': 'ĐỘC', '軽': 'KHINH', '体': 'THỂ', '好': 'HẢO', '汁': 'CHẤP', '状': 'TRẠNG', '界': 'CõiĐời', '厳': 'NGHIÊM', '才': 'TÀI', '躓': '', '予': 'DỰ', '痢': 'LỴ', '還': 'HOÀN', '差': '', '表': '', '望': 'VỌNG', '連': 'LIÊN', '墜': 'TRỤY', '端': 'ĐOAN', '証': 'CHỨNG', '退': 'THOÁI,THỐI', '寝': 'TẨM', '介': 'GIỚI', '処': 'XỬ,XỨ', '長': 'TRƯỜNG', '円': 'VIÊN', '築': 'TRÚC', '重': 'TRỌNG,TRÙNG', '鬱': 'UẤT', '眠': 'MIÊN', '逃': 'ĐÀO', '地': '', '率': 'XUẤT', '奢': 'XA', '苦': 'KHỔ', '頻': 'TẦN', '跨': '', '土': 'THỔ', '急': 'CẤP', '的': 'ĐÍCH', '紙': 'CHỈ', '聖': 'THÁNH', '脆': '', '敵': 'ĐỊCH', '立': 'LẬP', '胸': 'HUNG', '時': 'THỜI,THÌ', '突': 'ĐỘT', '役': '', '借': '', '客': '', '大': 'ĐẠI', '目': 'MỤC', '例': 'LIỆT', '配': 'PHỐI', '愛': 'ÁI', '戸': 'HỘ', '回': 'HỒI', '速': 'TỐC', '絵': 'HỘI', '横': 'HOÀNH', '転': 'CHUYỂN', '鋭': 'NHUỆ,DUỆ', '遠': 'VIỄN', '練': 'LUYỆN', '交': 'GIAO', '没': 'MỘT', '閑': '', '応': '', '酷': '', '美': 'MỸ', '流': 'LƯU', '材': 'TÀI', '誂': '', '脱': 'THOÁT', '計': 'KẾ', '傷': 'THƯƠNG', '異': 'DỊ', '華': 'HOA', '皮': 'BÌ', '怪': 'QUÁI', '鍋': 'OA', '返': 'PHẢN', '刃': 'NHẬN', '悲': 'BI', '心': 'TÂM', '冒': '', '収': '', '品': '', '即': '', '賞': '', '小': 'TIỂU', '倒': 'ĐẢO', '当': 'ĐƯƠNG', '尊': 'TÔN', '楽': 'LẠC,NHẠC', '格': 'CÁCH', '密': 'MẬT', '末': 'MẠT', '殺': 'SÁT', '入': 'NHẬP', '携': 'HUỀ', '毒': 'ĐỘC', '柄': 'BÍNH', '圏': 'QUYỀN', '恥': 'SỈ', '脅': 'HIẾP', '言': '', '茶': '', '浮': '', '世': 'THẾ', '信': 'TÍN', '種': 'CHỦNG', '庇': 'TÝ', '敗': 'BẠI', '単': 'ĐƠN', '取': 'THỦ', '道': 'ĐẠO', '解': 'GIẢI', '編': 'BIÊN', '情': 'TÌNH', '染': 'NHIỄM', '迫': 'BÁCH', '希': 'HY', '労': 'LAO,LẠO', '変': 'BIẾN', '織': '', '定': '', '遺': '', '病': '', '傾': 'KHUYNH', '願': 'NGUYỆN', '新': 'TÂN', '押': 'ÁP', '続': 'TỤC', '痛': 'THỐNG', '論': 'LUẬN', ' 累': 'LŨY', '寧': 'NINH', '仰': 'NGƯỠNG', '絶': 'TUYỆT', '箋': '', '瞬': 'THUẤN', '害': 'HẠI', '絹': 'QUYÊN', '廃': 'PHẾ', '間': '', '鈍': '', '諸': '', '清': '', '期': 'KỲ', '設': 'THIẾT', '闇': 'ÁM', '限': 'HẠN', '折': 'TRIẾT', '内': 'NỘI', '頑': 'NGOAN', '陶': 'ĐÀO', '懲': 'TRỪNG', '煽': '', '鮮': 'TIÊN', '腰': 'YÊU', '集': 'TẬP', '隔': 'CÁCH', '発': 'PHÁT', '進': 'TIẾN,TẤN', '次': '', '優': '', '明': '', '訣': '', '念': 'NIỆM', '類': 'LOẠI', '同': 'ĐỒNG', '静': 'TĨNH', '動': 'ĐỘNG', '抜': 'BẠT', '敬': 'KÍNH', '公': 'CÔNG', '幼': 'ẤU', '察': 'SÁT', '夜': 'DẠ', '拝': 'BÁI', '感': 'CẢM', '快': 'KHOÁI', '委': 'ỦY', '通': '', '怠': '', '痴': '', '思': '', '誤': '', '物': 'VẬT', '見': 'KIẾN', '費': 'PHÍ', '綴': '', '部': 'BỘ', '雇': 'CỐ', '潤': 'NHUẬN', '値': 'TRỊ', '丁': 'ĐINH', '壁': 'BÍCH', '呑': 'THÔN', '暗': 'ÁM', '易': 'DỊ,DỊCH', '換': 'HOÁN', '被': 'BỊ', '聴': 'THÍNH', '掬': '', '銭': '', '提': '', '起': '', '綻': '', '顔': 'NHAN', '底': 'ĐỂ', '前': 'TIỀN', '打': 'ĐẢ', '有': 'HỮU', '成': 'THÀNH', '読': 'ĐỘC', '他': 'THA', '圧': 'ÁP', '微': 'VI', '層': 'TẦNG,TẰNG', '参': 'THAM,SÂM', '散': 'TÁN', '妨': 'PHƯƠNG', '面': 'DIỆN', '学': 'HỌC', '趣': '', '響': '', '憾': '', '馬': '', '頭': 'ĐẦU', '宿': 'TÚC,TÚ', '丸': 'HOÀN', '請': 'THỈNH', '笑': 'TIẾU', '婉': 'UYỂN', '議': 'NGHỊ', '所': 'SỞ', '英': 'ANH', '存': 'TỒN', '祥': 'TƯỜNG', '損': 'TỔN', '検': 'KIỂM', '愚': 'NGU', '眇': '', '未': 'VỊ,MÙI', '細': '', '使': '', '斉': '', '事': '', '傘': '', '語': 'NGỮ', '訳': 'DỊCH', '阻': 'TRỞ', '張': 'TRƯƠNG', '謙': 'KHIÊM', '対': 'ĐỐI', '炊': 'XUY', '支': 'CHI', '示': 'THỊ', '少': 'THIẾU,THIỂU', '懸': 'HUYỀN', '線': 'TUYẾN', '真': 'CHÂN', '穴': 'HUYỆT', '万': 'VẠN', '瞭': '', '排': '', '境': '', '便': '', '不': 'BẤT', '右': 'HỮU', '束': 'THÚC', '和': 'HÒA', '恨': 'HẬN', '丈': 'TRƯỢNG', '剥': 'BÁC', '戦': 'CHIẾN', '辞': 'TỪ', '員': 'VIÊN', '茫': 'MANG', '元': 'NGUYÊN', '持': 'TRÌ', '書': 'THƯ', '査': 'TRA', '柱': 'TRỤ', '無': '', '整': '', '認': '', '金': '', '下': 'HẠ', '述': 'THUẬT', '改': 'CẢI', '場': 'TRƯỜNG', '矢': 'THỈ', '搬': 'BAN,BÀN', '閣': 'CÁC', '裁': 'TÀI', '顧': 'CỐ', '虚': 'HƯ', '列': 'LIỆT', '栄': 'VINH', '根': 'CĂN', '操': 'THAO,THÁO', '性': 'TÍNH,TÁNH', '催': 'THÔI', '抗': '', '秘': '', '自': '', '髪': '', '鹿': '', '赤': 'XÍCH', '字': 'TỰ', '併': 'TÍNH', '汗': 'HÃN', '犯': 'PHẠM', '探': 'THÁM', '敷': 'PHU', '繁': 'PHỒN', '人': 'NHÂN', '仕': 'SĨ', '作': 'TÁC', '左': 'TẢ', '合': 'HỢP,CÁP', '譲': 'NHƯỢNG', '身': 'THÂN', '疲': 'BÍ', '覧': '', '光': '', '署': '', '互': '', '券': 'KHOÁN', '然': 'NHIÊN', '兆': 'TRIỆU', '反': 'PHẢN', '日': 'NHẬT', '弁': 'BIỆN,BIỀN', '初': 'SƠ', '舟': 'CHU,CHÂU', '生': 'SINH', '撲': 'PHÁC,BẠC', '器': 'KHÍ'}

def get_hanviet(kanji):
    return combined_dict.get(kanji)
    
    
def add_hanviet():
    input_file = r'C:\Users\hungba\Documents\Programming\Python\2112-public-personal-tool-jlpt\anki_card.csv'
    output_file = 'output_file.csv'

    rows = []
    with open(input_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        kanji_col = row['Kanji']
        kanji_list = re.findall(r'[\u4e00-\u9faf]', kanji_col)
        if len(kanji_list) > 0:
            hanviet_list = []
            for kanji in kanji_list:
                hanviet = get_hanviet(kanji)
                if hanviet is not None:
                    hanviet_list.append(hanviet)
            combined_hanviet = ' '.join(hanviet_list)
            row['Hanviet'] = combined_hanviet

    fieldnames = rows[0].keys()
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
add_hanviet()

# print(get_hanviet("曲"))