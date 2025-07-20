import re
import os
import ast
import csv
import requests
from bs4 import BeautifulSoup

SOUND_SAVED_FOLDER = "sound"
IMAGE_SAVED_FOLDER = "image"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


class AnkiCard:
    def __init__(self, kanji="", furigana="", sound="", image="", meaning="", example_sentence="", example_sentence_mean="", example_sentence_sound=""):
        self.kanji = kanji or ""
        self.furigana = furigana
        self.sound = sound
        self.image = image
        self.meaning = meaning
        self.example_sentence = example_sentence
        self.example_sentence_mean = example_sentence_mean
        self.example_sentence_sound = example_sentence_sound

    def display(self):
        print("Kanji: ", self.kanji)
        print("Furigana: ", self.furigana)
        print("Sound: ", self.sound)
        print("Image: ", self.image)
        print("Meaning: ", self.meaning)
        print("example Sentence: ", self.example_sentence)
        print("example Sentence Meaning: ", self.example_sentence_mean)
        print("example Sentence Sound: ", self.example_sentence_sound)


# kanji_meanings_1 = [
#     ('実績', 'Thành tích, thực tích'),
#     ('人柄', 'Nhân cách'),
#     ('自主', 'Tự giác, tự chủ'),
#     ('於いて', 'Ngoài ra, loại trừ ra'),
#     ('ドーピング', 'Dùng thuốc kích thích (trong thi đấu thể thao)'),
#     ('出場', 'Ra trận, ra thi đấu'),
#     ('封鎖', 'Phong tỏa'),
#     ('被災', 'Bị thiên tai, bị tai họa'),
#     ('無実', 'Vô tội'),
#     ('捜査', 'Điều tra'),
#     ('認める', 'Công nhận, chấp nhận'),
#     ('失格', 'Mất tư cách'),
#     ('下地', 'Nền tảng, cơ sở hạ tầng'),
#     ('国籍', 'Quốc tịch'),
#     ('有権者', 'Người có quyền, cử tri'),
#     ('合唱', 'Hợp xướng'),
#     ('空き巣', 'Ăn trộm lúc vắng nhà'),
#     ('防犯', 'Phòng ngừa tội phạm'),
#     ('パトロール', 'Xe cảnh sát đi tuần'),
#     ('如何', 'Tùy thuộc vào'),
#     ('いかにも', '… gì đi nữa thì cũng…'),
#     ('あやふや', 'mơ hồ, không rõ ràng, không chắc chắn'),
#     ('提携', 'Liên kết, hợp tác'),
#     ('医療', 'Y học, y dược'),
#     ('事情', 'Sự tình'),
#     ('器', 'Cái chén đựng'),
#     ('押し切る', 'Vượt lên đến cùng'),
#     ('押し込む', 'Dồn, đẩy (đến đường cùng)'),
#     ('追い込む', 'Đuổi (đến đường cùng)'),
#     ('華やか', 'Hoa hòe, sặc sỡ, rực rỡ'),
#     ('上回る', 'Tăng lên cao hơn (nói về số liệu)'),
#     ('下回る', 'Giảm xuống thấp hơn (nói về số liệu)'),
#     ('背景', 'Hậu cảnh, cảnh nền'),
#     ('特許', 'Đặc phép, giấy phép đặc biệt'),
#     ('揉める', 'Cãi nhau, giằng co nhau'),
#     ('総理大臣', 'Thủ tướng'),
#     ('象徴', 'Tượng trưng'),
#     ('吹雪', 'Bão tuyết'),
#     ('儚い', 'Hão huyền, rỗng tuyệt'),
#     ('魅了', 'Quyến rũ, hấp dẫn'),
#     ('由縁', 'Cơ duyên, nguyên do, duyên cớ'),
#     ('語源', 'Nguồn gốc của ngôn ngữ'),
#     ('俳句', 'Thơ haiku'),
#     ('散る', 'Rơi rụng, rải rác'),
#     ('心酔', 'Say mê, mê muội'),
#     ('間柄', 'Mối quan hệ'),
#     ('固有', 'Sở hữu riêng, cá hữu'),
#     ('従来', 'Kiểu cũ'),
#     ('所持', 'Nắm giữ'),
#     ('騒がしい', 'Ồn ào'),
#     ('ずらっと', '(xếp, nằm) la liệt'),
#     ('ずばり', '(Cắt) bén ngót, (lời nói) sắc bén'),
#     ('切実', 'Cấp bách, khẩn cấp'),
#     ('束ねる', 'Bó buộc'),
#     ('保つ', 'Giữ gìn'),
#     ('多様', 'Đa dạng'),
#     ('つくづく', 'Một cách thận trọng'),
#     ('貫く', 'Thâm nhập, thực hiện'),
#     ('定義', 'Định nghĩa'),
#     ('紛らわしい', 'Dễ lẫn lộn, dễ nhầm lẫn'),
#     ('惨め', 'Khủng khiếp, tàn khốc'),
#     ('夜更け', '(suốt) đêm muộn'),
#     ('夜更かし', 'Thức khuya, thức đêm'),
#     ('据える', 'Đặt, xây dựng, thiết lập'),
#     ('悩ましい', 'Lo âu'),
#     ('健やか', 'Khỏe mạnh, cường tráng'),
#     ('ゆとり', 'Thủng thỉnh, từ tốn'),
#     ('余程', 'Rất nhiều'),
#     ('野心', 'Dã tâm'),
#     ('くすぐったい', 'Nhột'),
#     ('もどかしい', 'Bứt rứt'),
# ]

kanji_meanings_lesson_2 = [
    ('至る', 'tới, đến'),
    ('情勢', 'tình thế'),
    ('観測', 'quan sát đo đạt'),
    ('水位', 'mức nước'),
    ('ゲリラ', 'cơn bão Guerrilla (mưa lớn bất ngờ)'),
    ('豪雨', 'mưa to, mưa như trút nước'),
    ('猛暑', 'nóng dữ dội'),
    ('残暑', 'cái nóng còn sót lại sau lập thu'),
    ('絶滅', 'tuyệt chủng'),
    ('マラリア', 'sốt rét'),
    ('デング熱', 'sốt xuất huyết'),
    ('感染', 'truyền nhiễm'),
    ('余儀ない', 'hết cách, không còn cách nào khác'),
    ('識者', 'tiên tri (người có khả năng tuyên đoán)'),
    ('遂げる', 'làm đến cùng'),
    ('根本', 'căn bản'),
    ('リストラ', 'giảm bớt nhân viên, cắt hợp đồng'),
    ('赤字', 'thua lỗ'),
    ('黒字', 'có lời'),
    ('尊重', 'tôn trọng'),
    ('重んずる', 'trân trọng, chú trọng'),
    ('天井', 'trần nhà'),
    ('内装', 'nội thất'),
    ('賄賂', 'tiền mãi lộ, hối lộ'),
    ('辞職', 'từ chức, nghỉ việc'),
    ('破棄', 'bỏ đi, loại bỏ'),
    ('沈黙', 'im lặng'),
    ('参入', 'tham gia vào'),
    ('窃盗', 'trộm cắp'),
    ('弁償', 'bồi thường'),
    ('吾輩', 'tôi (cách nói ngày xưa)'),
    ('じめじめ', 'ẩm ướt'),
    ('書生', 'học sinh'),
    ('一段と', 'thêm nữa'),
    ('いきなり', 'bất ngờ, đột nhiên'),
    ('怪しい', 'nghi ngờ'),
    ('危うい', 'nguy hiểm'),
    ('獰悪', 'thô thiển, xấu xí'),
    ('種族', 'chủng tộc'),
    ('掌', 'lòng bàn tay'),
    ('別段', 'đặc biệt, cá biệt'),
    ('薬缶', 'ấm nước'),
    ('装飾', 'trang trí'),
    ('出会す', 'tình cờ gặp nhau'),
    ('突起', 'lồi lên, nhô lên'),
    ('煙', 'khói'),
    ('呟く', 'nói lầm bầm'),
    ('体裁', 'vẻ bên ngoài'),
    ('適宜', 'thích hợp'),
    ('咎める', 'nhắc nhở, trách móc'),
    ('和やか', 'hiền hậu, hòa nhã'),
    ('巧む', 'chế ra, làm ra'),
    ('巧み', 'khéo léo, thông minh, lanh lợi'),
    ('粗い', 'thô'),
    ('渋い', 'chát, đắng, cau có'),
    ('著しい', 'đáng kể, nổi bật'),
    ('とりわけ', 'đặc biệt'),
    ('台無し', 'sự tàn phá, sự phá hủy'),
    ('月並み', 'hằng tháng'),
    ('辻褄', 'hợp đạo lý'),
    ('どうにか', 'bằng cách nào đó'),
    ('乏しい', 'thiếu thốn'),
    ('名高い', 'có tên tuổi'),
    ('成り立つ', 'hội đủ, hình thành từ'),
    ('音色', 'âm sắc'),
    ('値引き', 'giảm giá'),
    ('惚ける', 'giả vờ'),
    ('把握', 'nắm bắt tình hình'),
    ('剥ぐ', 'bóc, tước ra, lột ra (vỏ cây, bọc chăn)'),
    ('密か', 'bí mật, riêng tư'),
    ('一息', '1 hơi thở, nghỉ ngơi, nổ lực thêm 1 chút nữa'),
    ('人柄', 'kiểu người, nhân cách'),
    ('不振', 'không tốt, không phát đạt, không trôi chảy'),
    ('報じる', 'thông báo, hồi đáp')
]

kanji_meanings_lesson_3 = [
    ('欠ける', 'mẻ'),
    ('欠かす', 'làm mẻ'),
    ('ひつじゅひん', 'nhu yếu phẩm'),
    ('囲む', 'bao lại, vây lại'),
    ('浅ましい', 'tồi tệ'),
    ('あくどい', 'lòe loẹt, phô trương'),
    ('コンセント', 'ổ cấm điện'),
    ('グリーンカーテン', 'bức rèm xanh'),
    ('抑制', 'ức chế'),
    ('収穫', 'thu hoạch'),
    ('最適', 'thích hợp nhất'),
    ('ほほえみ', 'mỉm cười'),
    ('訓練', 'huấn luyện'),
    ('治癒', 'lành bệnh, bình phục'),
    ('心遣い', 'sự chu đáo'),
    ('暴風雨', 'mưa gió'),
    ('愛好家', 'người hâm mộ, người yêu'),
    ('克服', 'khắc phục'),
    ('開ける', 'mở ra'),
    ('怒鳴る', 'hét lớn'),
    ('処分', 'xử lý'),
    ('ざわざわ', 'xào xạc'),
    ('札', 'bảng tên'),
    ('看板', 'bảng quảng cáo'),
    ('瀬戸', 'vịnh'),
    ('煉瓦', 'gạch'),
    ('硝子', 'kính'),
    ('裏側', 'mặt trái'),
    ('ペンキ', 'cây cọ'),
    ('当軒', 'ngôi nhà này'),
    ('大通り', 'con đường lớn'),
    ('予め', 'trước'),
    ('前もって', 'trước'),
    ('ありふれる', 'không hiếm'),
    ('依然', 'trước đây'),
    ('一心に', '1 lòng'),
    ('自惚れ', 'tự đắc'),
    ('身近', 'thân thuộc, gần gũi'),
    ('身なり', 'dáng vẻ'),
    ('無駄遣い', 'lãng phí'),
    ('明白', 'minh bạch, trong trắng'),
    ('目盛り', 'vạch trên thước đo'),
    ('申し出る', 'xin, nộp'),
    ('緩む', 'lỏng lẻo'),
    ('やけに', 'khủng khiếp'),
    ('養う', 'nuôi dưỡng'),
    ('もしくは', 'hay là'),
    ('見渡す', 'nhìn xa, nhìn rộng'),
    ('無言', 'không nói gì'),
    ('見苦しい', 'xấu xí, khó chịu'),
    ('まして', 'hơn'),
    ('施す', 'tiến hành, bố thí'),
    ('放り出す', 'phóng ra'),
    ('放り込む', 'phóng vào'),
    ('のんき', 'ung dung, chậm rãi'),
    ('朗らか', 'vui vẻ, rạng rỡ'),
    ('目覚ましい', 'nổi bật, gây chú ý'),
    ('本場', 'nơi chính thức, nơi sinh'),
    ('言い訳', 'ngụy biện'),
    ('マスコミ', 'thông tin đại chúng'),
    ('見計らう', 'lựa chọn, phán đoán'),
    ('勇ましい', 'dũng cảm'),
    ('絶え間ない', 'không ngừng nghỉ, liên tục'),
    ('いわゆる', 'nói chung'),
    ('捲る', 'cuốn lên, lật (trang sách)'),
    ('野外', 'ngoài trời'),
    ('融通', 'mượn và cho mượn tiền'),
    ('だいいち', 'trên hết'),
    ('空しい', 'rỗng'),
    ('ややこしい', 'phức tạp'),
    ('紛失', 'thất lạc'),
    ('手腕', 'năng lực, tài nghệ'),
    ('難儀', 'vất vả, khó khăn, khổ sở')
]

kanji_meanings_lesson_4 = [
    ('段落', 'một đoạn, một bước'),
    ('息抜き', 'nghỉ xả hơi'),
    ('リサーチ', 'nghiên cứu, tìm hiểu'),
    ('節約', 'tiết kiệm'),
    ('倹約', 'tiết kiệm, cắt giảm chi phí'),
    ('運命', 'số mệnh, vận mệnh'),
    ('辿る', 'lần theo, dõi theo'),
    ('単純', 'đơn thuần, đơn giản'),
    ('極端', 'cực đoan'),
    ('職人', 'người thợ, nghệ nhân'),
    ('道端', 'vỉa hè, lề đường'),
    ('乾杯', 'cụng ly, nâng ly'),
    ('受け継ぐ', 'kế tục'),
    ('コラーゲン', 'chất đạm collagen'),
    ('取締役', 'người quản lý, giám đốc'),
    ('駆け寄る', 'chạy nhào tới, chạy nhào vào'),
    ('背後', 'phía sau'),
    ('痴漢', 'sàm sỡ'),
    ('取り組む', 'tập trung hết sức, làm hết sức'),
    ('革新', 'cách tân'),
    ('導入', 'đưa vào'),
    ('強固', 'vững bền, cứng đầu'),
    ('活気', 'hoạt khí'),
    ('義務', 'nghĩa vụ'),
    ('塾', 'lớp dạy thêm, trường dạy thêm'),
    ('伸し掛かる', 'ngả người lên, đè lên'),
    ('突出', 'nhô ra, đâm ra'),
    ('連携', 'liên doanh, liên kết'),
    ('寄り掛かる', 'ghé vào'),
    ('揺らぐ', 'đung đưa'),
    ('がっくり', 'chùng xuống, thất vọng, gãy gấp khúc'),
    ('画期的', 'mang tính bước ngoặt (lịch sử), mốc đánh dấu'),
    ('着飾る', 'ăn diện, làm đẹp'),
    ('ジャンプ', 'dầu gội đầu'),
    ('シナリオ', 'kịch bản'),
    ('割り当て', 'phân công, chia phần'),
    ('ろくに', '(không) đủ, tươm tất'),
    ('連休', 'ngày nghỉ lễ liên tiếp'),
    ('領地', 'lãnh địa'),
    ('領土', 'lãnh thổ'),
    ('とかく', 'làm này làm kia, dù thế nào'),
    ('逞しい', 'khỏe mạnh, rắn chắc'),
    ('忠告', 'khuyên nhủ, dạy bảo'),
    ('到底', 'hoàn toàn, tuyệt đối'),
    ('ちやほや', 'chiều chuộng'),
    ('募る', 'chiêu mộ'),
    ('手当', 'tiền phụ cấp'),
    ('遠ざかる', 'đi xa, rời xa'),
    ('内緒', 'bí mật, giữ kín'),
    ('何より', 'hơn tất cả là, không có gì bằng'),
    ('制裁', 'hình phạt, chế tài'),
    ('吊り革', 'cái tay nắm, tay cầm'),
    ('あっけない', 'không có gì thú vị, tẻ nhạt'),
    ('夥しい', 'nhiều, vô số, khủng khiếp'),
    ('回収', 'thu hồi'),
    ('該当', 'thích hợp, phù hợp, đúng với'),
    ('最中', '(cái gì đó) đang diễn ra'),
    ('さほど', '...đến như thế'),
    ('突如', 'đột nhiên'),
    ('並びに', 'song song với, cùng với'),
    ('汚らわしい', 'dơ bẩn, gớm ghiếc'),
    ('権限', 'quyền hạn'),
    ('光沢', 'độ bóng, sáng'),
    ('満場', 'đầy hội trường'),
    ('味覚', 'vị giác'),
    ('愛想', 'tình yêu, sự tử tế, tốt bụng'),
    ('一同に', 'đồng nhất, cùng với'),
    ('一律', 'đều nhau, đồng nhất với nhau'),
    ('清々しい', 'trong lành'),
    ('切実', 'thiết thực'),
    ('有望', 'đầy hi vọng'),
    ('ほとり', 'vùng lân cận, quan hệ gần gũi'),
    ('舗装', 'mặt đường lát, việc lát đường'),
    ('よそ見', 'nhìn đi chỗ khác'),
]




def download_sound_japandict(soup, word):
    print(f"Info: Download sound from japandict.com for {word}")
    sound_save_path = f"{SOUND_SAVED_FOLDER}/{word}.ogg"

    if os.path.exists(sound_save_path):
        print(f"Info: Sound is exist for {word}")
        return sound_save_path

    a_element = soup.find(
        'a', class_='btn btn-white play-reading-btn d-flex justify-content-center align-items-center p-0')

    parameter_str = a_element['data-reading']
    parameter_list = ast.literal_eval(parameter_str)

    base_url = "https://www.japandict.com/voice/read?text="
    phoneme_text = parameter_list[1]
    jwt_token = parameter_list[2]
    vid = parameter_list[3]
    url = f"{base_url}{phoneme_text}&outputFormat=ogg_vorbis&jwt={jwt_token}&vid={vid}"

    with open(sound_save_path, "wb") as f:
        r = requests.get(url, headers=HEADERS)
        f.write(r.content)

    print("Info: Download Success")
    return sound_save_path


def return_furigana(soup):
    print(f"Info: Get furigana from japandict.com")
    a_element = soup.find(
        'a', class_='btn btn-white play-reading-btn d-flex justify-content-center align-items-center p-0')

    parameter_str = a_element['data-reading']
    parameter_list = ast.literal_eval(parameter_str)

    phoneme_text = parameter_list[1]

    match = re.search(r"ph='(.*?)'", phoneme_text)

    if match:
        return match.group(1)
    else:
        return ''


def return_example(soup):
    print(f"Info: Get example from japandict.com")

    div_element = soup.find('div', class_='m-1 d-flex align-items-center')

    if div_element is None:
        print(f"Warning: No example")
        return None

    a_element = div_element.find(
        'a', class_='btn btn-white play-reading-btn d-flex justify-content-center align-items-center p-0')

    parameter_str = a_element['data-reading']
    parameter_list = ast.literal_eval(parameter_str)

    example_text = parameter_list[1]

    return example_text


def return_example_mean(soup):
    print(f"Info: Get example mean from japandict.com")

    sentence_element = soup.find('div', {'class': 'tab-pane p-3 active'})

    if sentence_element is None:
        print(f"Warning: No example mean")
        return None

    sentence = sentence_element.text.strip()

    return sentence


def download_example_sound(soup, example):
    print(f"Info: Get example sound from japandict.com")
    sound_save_path = f"{SOUND_SAVED_FOLDER}/{example.replace('。','')}.ogg"

    if os.path.exists(sound_save_path):
        print(f"Info: Sound is exist for {example}")
        return sound_save_path

    div_element = soup.find('div', class_='m-1 d-flex align-items-center')

    if div_element is None:
        print(f"Warning: No example sound")
        return None

    a_element = div_element.find(
        'a', class_='btn btn-white play-reading-btn d-flex justify-content-center align-items-center p-0')

    parameter_str = a_element['data-reading']
    parameter_list = ast.literal_eval(parameter_str)

    phoneme_text = parameter_list[1]
    jwt_token = parameter_list[2]
    vid = parameter_list[3]

    base_url = "https://www.japandict.com/voice/read?text="
    url = f"{base_url}{phoneme_text}&outputFormat=ogg_vorbis&jwt={jwt_token}&vid={vid}"

    with open(sound_save_path, "wb") as f:
        r = requests.get(url, headers=HEADERS)
        f.write(r.content)

    print("Info: Download Success")
    return sound_save_path


# def return_meaning(soup):
#     a_element = soup.find(
#         'div', class_='tab-pane active')

#     text = a_element.find('div', lang='en').get_text(strip=True)
#     return text


def fill_return_anki_card(anki_card: AnkiCard):
    url = f'https://www.japandict.com/{anki_card.kanji}'

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # download sound
        result = download_sound_japandict(soup, anki_card.kanji)
        if result != False:
            anki_card.sound = result

        # download image
        result = download_image(anki_card.kanji)
        if result != False:
            anki_card.image = result

        # get word's furigana
        anki_card.furigana = return_furigana(soup)

        # get meaning
        # anki_card.meaning = return_meaning(soup)

        # get example
        example = return_example(soup)
        if example is not None:
            anki_card.example_sentence = example

            # get example mean
            anki_card.example_sentence_mean = return_example_mean(soup)

            # download example sound
            result = download_example_sound(soup, anki_card.example_sentence)
            if result != False:
                anki_card.example_sentence_sound = result

        return anki_card

    print("Error: Cannot access japandict.com")


def list_kanji_from_csv(file_path):
    kanji_list = []

    with open(file_path, "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row

        for row in reader:
            kanji = row[0]  # Assuming kanji is stored in the first column
            kanji_list.append(kanji)

    return kanji_list


def write_to_csv(anki_cards):
    with open("anki_card.csv", "a", newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)

        for card in anki_cards:
            if card is not None:
                writer.writerow([card.kanji, card.furigana, card.sound, card.image, card.meaning,
                            card.example_sentence, card.example_sentence_mean, card.example_sentence_sound])



def save_image(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    return False


def download_image(search_term):
    print(f"Info: Get image for {search_term}")
    image_save_path = f"{IMAGE_SAVED_FOLDER}/{search_term.replace('。','')}.jpg"

    if os.path.exists(image_save_path):
        print(f"Info: Image is exist for {search_term}")
        return image_save_path

    API_KEY = "37203957-68239a3614010ec590245afe6"
    url = f"https://pixabay.com/api/?key={API_KEY}&q={search_term}&image_type=photo"
    response = requests.get(url)
    data = response.json()
    if "hits" in data and data["hits"]:
        # Get the URL of the first image
        image_url = data["hits"][0]["webformatURL"]
        save_image(image_url, image_save_path)
        return image_save_path
    return False


def full_kanji_meaning():
    text = '''1.そうぎょう 創業 n./vi. thành lập, khởi nghiệp
    2.ちめいど 知名度 n. mức độ nổi danh
    3.おりいって 折り入って adv. thật lòng là…
    4.エレガンス n. vẻ tao nhã, nét thanh lịch
    5.きわまる 極まる vi. cực độ, tột cùng
    6.ゆうび 優美 n./な-adj. tao nhã, ưu mỹ
    7.キャッチコピー khẩu hiệu, khẩu hiệu quảng cáo
    8.きょくせん 曲線 n. đường cong
    9.はんきょう 反響 n./vi. tiếng vang
    10.つうこん 痛恨 n./vt. thật sự đáng tiếc
    11.ひろう 疲労 n./vi. mệt mỏi, mệt nhọc
    12.いかん 遺憾 n./な-adj. đáng tiếc, hối tiếc
    13.ものだね 物種 n. khởi nguồn (của sự vật, sự việc)
    14.せきめん 赤面 n./vi. đỏ mặt (vì xấu hổ)
    15.のんき 呑気 n. vô lo, vô tư
    16.こうえい 光栄 n. vinh dự
    17.あたいする 値する vi. có giá trị, đáng giá
    18.かんがん 汗顔 n. mặt đổ cả mồ hôi (vì xấu hổ)
    19.かんしょう 鑑賞 n./vt. thưởng thức
    20.けいちょう 傾聴 n./vt. lắng nghe
    21.ねん 念 n. niệm, tâm niệm
    22.かわきり 皮切り n. bắt đầu từ…, lấy (cái gì đó) làm đầu tiên
    23.がっきゅういいん 学級委員 n. ủy viên của lớp
    24.エピソード n. chương, hồi (của tiểu thuyết, kịch v.v…)
    25.つかいこむ 使い込む vt. tham ô, chiếm đoạt (tiền của người khác)
    26.ちじ 知事 n. chủ tịch tỉnh, thống đốc
    27.こうひ 公費 n. tiền công vụ
    28.しひ 私費 n. tiền tư, tiền của cá nhân
    29.へきえき 辟易 n./vi. chùn bước lại, co rút người lại, lo lắng, băn khoăn
    30.はんじょう 繁盛 n./vi. (buôn bán) phát đạt
    31.かいざん 改ざん n./vt. làm giả, cải gian (giấy tờ)
    32.とうろん 討論 n./vt./vi. tranh luận
    33.こきゃくそう 顧客層 n. lớp khách hàng
    34.トレンド n. xu hướng, khuynh hướng
    35.ほんしょう 本性 n. bản tính
    36.もうける 設ける vt. thiết lập
    37.せいとう 正当 n./な-adj. chính đáng, công chính, ngay thẳng
    38.こく 酷 な-adj. kinh khủng, tàn khốc
    39.てつや 徹夜 n./vi. thức trắng đêm, thức thâu đêm
    40.とだな 戸棚 n. tủ (chén, quần áo)
    41.ふらふら adv./vi. lắc qua lắc lại, loạng choạng
    42.むてき 無敵 n./な-adj. vô địch
    43.あかし 証 n. bằng chứng, dấu hiệu
    44.あたりまえ 当たり前 な-adj. đương nhiên, hiển nhiên
    45.たにん 他人 n. người ngoài, người dưng
    46.ジャンル n. chủng loại, thể loại
    47.しゅるい 種類 n. loại, thể loại
    48.そんけいご 尊敬語 n. từ kính ngữ
    49.けんじょうご 謙譲語 n. từ khiêm tốn, khiêm nhường ngữ
    50.ていねいご 丁寧語 n. từ lễ phép
    51.しゅんじ 瞬時 n. tức thời
    52.きりかえる 切り替える vt. chuyển đổi, đổi qua cái khác
    53.ごよう 誤用 n./vt. dùng nhầm
    54.びんせん 便箋 n. giấy viết thư
    55.つづる 綴る vt. (viết) nối liền
    56.しゅくめい 宿命 n. định mệnh, số phận
    57.しよう 仕様 n. phương cách, cách thức
    58.ぐっと adv. dồn hết sức (để làm gì đó)
    59.ぜんてい 前提 n. tiền đề
    60.タイミング n. thời khắc, đúng lúc
    61.いまだ 未だ adv. vẫn chưa
    62.うつむく 俯く vi. cúi mặt
    63.ちょくちょく adv. thỉnh thoảng, lặp đi lặp lại
    64.てんで adv. hoàn toàn, toàn bộ
    65.どうかん 同感 n./vi. đồng cảm
    66.なれなれしい 馴れ馴れしい い-adj. (thái độ) xuề xòa, quá thân thiết
    67.にげだす 逃げ出す vi. bỏ chạy
    68.ねだる 強請る vt. giành giật, chiếm đoạt (bằng cách cưỡng chế)
    69.まちどおしい 待ち遠しい い-adj. chờ đợi mỏi mòn
    70.みっしゅう 密集 n./vi. đông đúc, chen chúc nhau
    71.もはや adv. (cái gì đó) trôi qua nhanh
    72.やくば 役場 n. trụ sở
    73.やしき 屋敷 n. khuôn viên ngôi nhà
    1.きまずい 気まずい い-adj. khó xử, ngại
    2.たいこう 対抗 n./vi. chống chọi, đối kháng
    3.とりつぐ 取り次ぐ vt. truyền tải, hồi âm
    4.とりたてる 取り立てる vt. thu hồi, lấy lại, đòi lại
    5.こける 転ける vi. té ngã
    6.つまずく 躓く vi. vấp chân, trượt chân
    7.さいばんちょう 裁判長 n. chủ tọa phiên tòa
    8.ちょうえき 懲役 n. đi tù
    9.むき 無期 n. tù chung thân, không kỳ hạn
    10.ゆうき 有期 n. có kỳ hạn
    11.げんこく 原告 n. nguyên cáo
    12.ひこく 被告 n. bị cáo
    13.びどう 微動 n./vi. rung rinh, lắc nhẹ
    14.はいたい 敗退 n./vi. thất bại, bại trận
    15.かべがみ 壁紙 n. giấy dán tường
    16.とうき 陶器 n. đồ gốm sứ
    17.ためる 矯める vt. uốn cong, sửa lỗi
    18.すがめる 眇める vt. nheo mắt
    19.おさななじみ 幼馴染み n. bạn thời thơ ấu
    20.ささぶね 笹舟 n. thuyền lá trúc (đồ chơi)
    21.じょうりゅう 上流 n. thượng lưu
    22.かりゅう 下流 n. hạ lưu
    23.デビュー n./vi. lần trình diễn đầu tiên
    24.ふしょうじ 不祥事 n. chuyện bê bối, chuyện tai tiếng
    25.はばかる 憚る vi./vt. do dự, lưỡng lự
    26.けっさく 傑作 n. kiệt tác
    27.だんげん 断言 n./vt. nói quả quyết, khẳng định
    28.たんけん 探検 n./vt. thám hiểm
    29.ばれる vi. bị bại lộ
    30.かんさつ 観察 n./vt. quan sát
    31.けいひん 景品 n. quà tặng
    32.さんきゅう 産休 n. nghỉ sinh
    33.だいたい 代替 n./vt. thay thế
    34.しょうとつ 衝突 n./vi. đâm vào, đụng vào
    35.ちょくしん 直進 n./vi. trực tiến, đi thẳng
    36.おうてん 横転 n./vi. ngã lộn nhào, té lộn nhào
    37.させつ 左折 n./vi. quẹo trái
    38.うせつ 右折 n./vi. quẹo phải
    39.パトカー n. xe cảnh sát
    40.だぼく 打撲 n./vt. ẩu đả, đánh nhau
    41.けいしょう 軽傷 n. vết thương nhẹ
    42.じゅうたい 重体 n. nghiêm trọng, bị thương nặng
    43.もくげき 目撃 n./vt. mục thị, chứng kiến
    44.さいぶ 細部 n. phần chi tiết
    45.はもの 刃物 n. đồ nhọn sắc bén, dao
    46.おしいる 押し入る n. đút vào, ấn vào
    47.おどす 脅す vt. đe dọa
    48.はんこう 犯行 n. hành vi phạm tội
    49.かけつける 駆けつける vi. chạy nhào tới, chạy nhanh tới
    50.スリル n. run sợ, kinh sợ, kinh hoàng
    51.とりおさえる 取り押さえる vt. tóm được, túm bắt
    52.きょうじゅつ 供述 n./vt. khai (sự thật)
    53.あおぐ 仰ぐ vt. ngước lên, ngước nhìn
    54.つぶら 円ら な-adj. tròn xoe
    55.てぎわ 手際 n. kỹ năng, tay nghề
    56.ときおり 時折 adv. thỉnh thoảng
    57.とうとい 尊い い-adj. cao cả, quý giá
    58.ふさわしい 相応しい い-adj. thích hợp, xứng đáng
    59.ぶらぶら adv./vi. (thòng xuống) đong đưa
    60.べんかい 弁解 n./vi./vt. giải bày, biện hộ, giải biện
    61.ほころびる 綻びる vi. hé mắt, hé nụ
    62.ほっさ 発作 n./vi. phát tán, bộc phát
    63.まぎれる 紛れる vi. trộn lẫn, lẫn lộn
    64.うっかり adv. đờ người ra, thờ người ra
    65.いっせいに 一斉に adv. đồng loạt
    66.みのうえ 身の上 n. số phận
    67.みれん 未練 n./な-adj. nuối tiếc, thương tiếc, sầu muộn
    68.おおがら 大柄 n./な-adj. dáng người to cao
    69.こがら 小柄 n./な-adj. dáng người thấp bé, nhỏ nhắn
    70.ひらたい 平たい い-adj. bằng phẳng
    71.げんみつ 厳密 な-adj. tuyệt mật, thật kín đáo
    72.こうご 交互 n. thay phiên nhau
    73.こころよい 快い い-adj. sảng khoái, thoải mái
    74.のどか 長閑 な-adj. yên bình, tĩnh lặng
    75.おごそかに 厳かに adv. một cách nghiêm túc, trịnh trọng, nghiêm khắc
    76.こころざす 志す vi. hướng tới, có ý định làm, muốn đạt được
    77.こころざし 志 n. ý định, chí hướng
    78.るいしん 累進 n./vi. thăng tiến, (sự nghiệp) thành công
    1.イマイチ adv. dở, kém, thiếu thiếu gì đấy
    2.しちょうりつ 視聴率 n. tỉ lệ người xem
    3.するどい 鋭い い-adj. nhạy bén, sắc sảo
    4.ミステリアス な-adj. huyền bí
    5.いちごがり イチゴ狩り n. hái dâu
    6.あなば 穴場 n. địa điểm hay nhưng ít được biết đến
    7.そんかい 損壊 n./vi. tổn hại
    8.しんきょう 心境 n. tâm trạng
    9.どんかん 鈍感 n./な-adj. không nhạy bén
    10.さんどう 参道 n. đường dành riêng cho người đi bộ
    11.さっとう 殺到 n./vi. dồn ép
    12.バタバタ adv./vi. phành phạch, tất bật
    13.ぜいむしょ 税務署 n. sở thuế vụ
    14.だつぜい 脱税 n./vi. sự trốn thuế
    15.しまつ 始末 n./vt. don dẹp, xử lý
    16.バケツ n. cái xô, thùng (đựng nước)
    17.ごにん 誤認 n./vt. ngộ nhận
    18.ずぶ prefix/adv. tất cả, toàn bộ
    19.かえりみる 顧みる vt. suy nghĩ chuyện đã qua
    20.コスプレ n. hóa trang thành nhân vật truyện tranh, anime
    21.せいち 聖地 n. thánh địa
    22.はずむ 弾む vi./vt. dội lại, đàn hồi
    23.ようつう 腰痛 n. đau thắt lưng
    24.いぶつ 異物 n. vật lạ
    25.こんにゅう 混入 n./vi./vt. trộn vào
    26.たいまん 怠慢 n./な-adj. lười biếng
    27.おこたる 怠る vi./vt. làm biếng
    28.かいこ 解雇 n./vt. đuổi việc, sa thải
    29.どくさいてき 独裁的 な-adj. tính độc tài
    30.ぎっくりごし ぎっくり腰 n. cụp xương sống
    31.はんそう 搬送 n./vt. chuyên chở
    32.アルコールちゅうどく アルコール中毒 n. ngộ độc rượu
    33.かみん 仮眠 n./vi. ngủ 1 giấc ngắn
    34.いへん 異変 n./な-adj. bất thường
    35.さっする 察する vt. phán đoán
    36.だんりょく 弾力 n. lực đàn hồi
    37.しなやか な-adj. dẻo, dẻo dai
    38.しめい 使命 n. sứ mệnh
    39.しんぼう 辛抱 n./vi. nhẫn nại
    40.すくう 掬う vt. hốt 1 nhúm, 1 ít (bột, chất lỏng)
    41.ついやす 費やす vt. tiêu xài
    42.つうせつ 痛切 な-adj. sâu sắc, thấm thía
    43.ねたむ 妬む vt. ganh tỵ
    44.ノイローゼ n.
    45.はいけい 背景 n. bối cảnh
    46.はくじょう 白状 n./vt. khai báo
    47.はじらう 恥じらう vi. mắc cỡ
    48.ぼっしゅう 没収 n./vt. tịch thu, thu hồi
    49.みすぼらしい い-adj. nghèo nàn, yếu đuối
    50.みじん 微塵 n. bụi nhỏ (cực nhỏ)
    51.ゆすぐ vt. súc miệng
    52.こうちょう 好調 n./な-adj. (máy) chạy tốt
    53.がんらい 元来 adv. trạng thái từ đầu
    54.げり 下痢 n. tiêu chảy
    55.はなばなしい 華々しい い-adj. rực rỡ, lộng lẫy
    56.アプローチ n./vi. tiếp cận
    57.インフレ n. lạm phát
    58.あざわらう 嘲笑う vt. cười nhạo, chế giễu
    59.あべこべ n./な-adj. ngược ngạo
    60.かぶれる vi. chìm, đắm, nổi mày đay
    61.しいて adv. quá sức, quá mức chịu đựng
    62.しいる 強いる vt. vắt, ép
    63.とんだ pre-noun adjectival không tưởng tượng nổi
    64.だぶだぶ adv./な-adj./vi. sóng sánh
    65.ちゅうしょう 中傷 n./vt. nói oan (vô căn cứ)
    66.つかのま 束の間 n. 1 chút, 1 lát
    67.らっかん 楽観 n. lạc quan
    68.ひかん 悲観 n. bi quan
    69.ぶかぶか adv./vi./な-adj. rộng thùng thình
    70.ぺこぺこ adv./vi./な-adj. trống rỗng
    71.またがる 跨る vi. ngồi tư thế cưỡi ngựa
    72.まるっきり adv. hoàn toàn
    73.むしる vt. nhổ (răng…)
    74.めいりょう 明瞭 n./な-adj. rõ ràng
    75.もっぱら adv. tập trung
    76.やりとおす やり通す vt. làm đến cùng
    78.めぢから 目力 n. sức mạnh của ánh mắt
    1.かけもち 掛け持ち n./vt. làm cả hai việc một lần
    2.ほんまつてんとう 本末転倒 n. không làm việc chính lại đi làm việc chẳng đâu vào đâu
    3.いっしゅん 一瞬 n./adv. trong phút chốc, trong tích tắc
    4.つうじょう 通常 n./adv. thông thường
    5.つねに 常に adv. thường lệ, lúc nào cũng, luôn luôn
    6.ざせつ 挫折 n./vi. thất bại, sụp đổ, chùn bước
    7.ぐち 愚痴 n. than vãn, phàn nàn
    8.とりよせる 取り寄せる vt. đặt hàng
    9.グルメ n. phong vị món ăn, người sành ăn
    10.たっせい 達成 n./vt. đạt được
    11.むだん 無断 n. tự ý (làm gì đó mà không xin phép)
    12.ぜんえい 前衛 n. tiền vệ, tiên phong, mới (nghệ thuật)
    13.そんぞく 存続 n./vi./vt. tiếp tục tồn tại
    14.あいこ 愛顧 n./vt. (khách hàng) thân thiết, quen thuộc
    15.しょ 諸 n./vt. prefix nhiều
    16.ひんぱつ 頻発 n./vi. thường xuyên (xảy ra)
    17.ばつぐん 抜群 n./な-adj. nổi bật, quá tốt
    18.かいしゃく 解釈 n./vt. giải thích, làm sáng tỏ
    19.やくす 訳す vt. dịch, thông dịch
    20.いちがん 一丸 n. (tất cả) cùng đồng lòng, nhất trí, trở thành một
    21.しつかん 質感 n. cảm giác (về đồ vật nào đó), chất lượng
    22.めど 目処 n. quan điểm, tầm nhìn, mục tiêu
    23.たちあがる 立ち上がる vi. đứng dậy
    24.はいしゅつ 排出 n./vt. thải ra ngoài
    25.にゅうかく 入閣 n./vi. vào nội các, gia nhập nội các
    26.くらく 苦楽 n. khổ lạc, khổ và sướng
    27.たいせん 対戦 n./vi. đối chiến, cuộc chiến
    28.ししゅんき 思春期 n. tuổi mới lớn, tuổi dậy thì
    29.あやしむ 怪しむ vt. nghi ngờ, ngờ vực, hồ nghi
    30.アピール n./vi./vt. thể hiện mình, tạo chú ý cho mình
    31.だいこんおろし 大根おろし n. củ cải trắng mài nhuyễn
    32.たく 炊く vt. nấu cơm
    33.どなべ 土鍋 n. nồi đất
    34.つけもの 漬物 n. món ngâm chua
    35.たんてき 端的 な-adj. trung trực, thẳng thắn
    36.ぜつみょう 絶妙 n./な-adj. tuyệt diệu
    37.てってい 徹底 n./vi. triệt để
    38.なまぐさい 生臭い い-adj. hôi tanh (cá)
    39.なまみ 生身 n. phần thịt, cá sống, tươi sống
    40.あいま 合間 n. thời gian giữa (hai việc gì đó)
    41.ガレージ n. ga-ra, nhà để ô tô
    42.コントラスト n. sự tương phản, sự trái ngược
    43.あつらえる 誂える vt. đặt thợ làm (quần áo, giày dép…)
    44.あやつる 操る vt. thao tác, điều khiển
    45.うっとうしい 鬱陶しい い-adj. tối tăm, u ám, ảm đạm, u sầu
    46.えんきょく 婉曲 な-adj. (nói) bóng gió, ẩn ý
    47.えんまん 円満 な-adj. viên mãn
    48.おくびょう 臆病 n./な-adj. sự nhát gan
    49.おだてる 煽てる vt. tâng bốc, xu nịnh
    50.おどおど adv./vi. run rẩy
    51.にかよう 似通う vi. giống nhau (khuôn mặt, hình dáng…)
    52.きよらか 清らか な-adj. trong xanh, trong lành
    53.なめらか 滑らか な-adj. mềm mại, mượt mà, mịn màng
    54.ぬけだす 抜け出す vi. lấy ra, tháo ra, rút ra
    55.にんじょう 人情 n. nhân tình
    56.ねまわし 根回し n./vt. bứng gốc (cây)
    57.のぞましい 望ましい い-adj. đáng ao ước, đáng mong đợi, hi vọng
    58.はいしゃく 拝借 n./vt. mượn
    59.はいれつ 配列 n./vt. sắp xếp, xếp hàng
    60.はくがい 迫害 n./vt. khủng bố, ngược đãi, hành hạ
    61.はつみみ 初耳 n. mới nghe lần đầu, lần đầu tiên nghe
    62.はばむ 阻む vt. cản trở, gây trở ngại
    63.ばんのう 万能 n./な-adj. vạn năng
    64.びっしょり adv. ướt chèm nhẹp, ướt tơi tả
    65.ひってき 匹敵 n./vi. ngang tài, ngang sức
    66.ひょっとしたら phrase nói không chừng thì…, không chừng thì…
    67.ぶつぎ 物議 n. chuyện ầm ĩ, xôn xao bàn tán, chuyện bị lên án
    68.ふまえる 踏まえる vt. giẫm lên, đạp lên, lấy làm cơ sở, lấy làm tiền đề (nghĩa bóng)
    69.ふんだん な-adj. dư thừa, quá nhiều
    70.ぼうぜん 茫然 adv.'s conjugation thờ người ra, ngẩn người ra
    71.ぼやく vi./vt. phàn nàn, càm ràm
    72.ただしく 正しく adv. một cách đúng đắn
    73.まちまち な-adj. mỗi cái mỗi khác, mỗi người mỗi khác
    74.まるめる 丸める vt. vo tròn, cuộn tròn
    75.みのまわり 身の回り n. xung quanh mình
    76.むちゃ 無茶 n./な-adj. vô lý, quá đáng, lố bịch
    77.むやみに 無闇に adv. một cách mù quáng, một cách thiếu suy nghĩ
    1.そうば 相場 n. giá cả nhìn chung, giá cả thị trường
    2.そくする 即する vi. vừa khớp, vừa khít, đúng chính xác
    3.しんちく 新築 n. nhà mới xây
    4.けん 圏 n. khu, vùng
    5.キャンペーン n. đợt khuyến mãi
    6.リフォーム n./vt. sửa nhà lại cho mới
    7.げんかい 限界 n. mức giới hạn
    8.りっち 立地 n. vị trí, nơi, chỗ
    9.さしつかえる 差し支える vi. gây trở ngại, gây tổn hại
    10.ないらん 内覧 n./vt. xem bên trong
    11.みだしなみ 身だしなみ n. sự chỉnh chu (vẻ ngoài)
    12.ひょうじょう 表情 n. biểu cảm, sự thể hiện tình cảm
    13.ようじん 用心 n./vi. sự cẩn thận, đề phòng, lo trước
    14.プランター n. chậu để trồng hoa, rau
    15.とうし 投資 n./vi. đầu tư
    16.きらく 気楽 な-adj. nhẹ người, thoải mái
    17.へんせい 編成 n./vt. tổ chức, sắp xếp
    18.のっとる 則る vi. theo quy tắc, tuân thủ đúng quy tắc
    19.ひけつ 秘訣 n. bí quyết
    20.スーパーチェーン n. dây chuyền, hệ thống siêu thị
    21.じれい 事例 n. trường hợp, hoàn cảnh, tình thế
    22.とうはつ 頭髪 n. đầu tóc, mái tóc
    23.しゅし 趣旨 n. tiêu chí
    24.えま 絵馬 n. tấm gỗ để viết lời cầu nguyện trong đền, chùa
    25.えんぎもの 縁起物 n. vật mang điềm báo, vật để cầu nguyện
    26.ちょうかい 懲戒 n./vi. khiển trách, quở trách
    27.やくいん 役員 n. người lãnh đạo
    28.しんきゅう 進級 n./vi. tiến cấp
    29.あっぱく 圧迫 n./vt. sức ép, ép, áp lực, áp đảo
    30.ぬいぐるみ n. thú nhồi bông
    31.そうたい 相対 n./vi. tương đối
    32.しっつい 失墜 n./vt. thất thế, mất uy thế
    33.かみくず 紙くず n. giấy nháp, giấy bỏ
    34.うちあける 打ち明ける vt. bộc bạch, tâm sự, thổ lộ
    35.せんさい 繊細 な-adj. mỏng manh, mảnh khảnh, chi tiết
    36.がっぺい 合併 n./vi./vt. liên doanh, liên kết
    37.あく 灰汁 n. bọt (khi nấu ăn hay có bọt của thịt, cá nổi lên trên)
    38.えいみん 永眠 n./vi. vĩnh miên, chết
    39.ねころぶ 寝転ぶ vi. nằm thườn ra, nằm bẹp ra
    40.はっき 発揮 n./vt. phát huy
    41.きじ 生地 n. vải, chất liệu vải
    42.ており 手織り n. may tay, may bằng tay
    43.モール n. dải buộc, thanh viền
    44.カウンター n. quầy hàng, kiểu bàn ngồi cao
    45.ギフトけん ギフト券 n. thẻ tặng quà, phiếu tặng quà
    46.るいけい 累計 n./vt. lũy kế, hệ số
    47.こうかん 交換 n./vt. trao đổi, đổi
    48.あざやか 鮮やか な-adj. rực rỡ, nhiều màu sắc
    49.あらかじめ 予め adv. trước, (làm) trước, (chuẩn bị) trước
    50.あんじ 暗示 n./vt. ám chỉ
    51.いき／すい 粋 n. thanh nhã, lịch sự, khéo léo
    52.いちがいに 一概に adv. 1 cách phóng khoáng, cứ…
    53.いっかつ 一括 n./vt. gom lại một lần, trả gọn một lần (tiền)
    54.いちれん 一連 n. một loạt, một chuỗi
    55.うつろ 虚ろ n./な-adj. rỗng, trống
    56.うるおう 潤う vi. trơn, nhờn, ẩm ướt
    57.うんざり adv./vi. chán ngấy
    58.おおまか 大まか な-adj. đại khái, khoảng
    59.おのずから 自ずから adv. tự bản thân
    60.がいする 害する vt. gây hại, gây tổn hại
    61.ぼうがい 妨害 n./vt. cản trở, gây trở ngại
    62.かおつき 顔つき n. nét mặt
    63.かいにゅう 介入 n./vi. xen vào, can thiệp
    64.かくさ 格差 n. sự phân biệt giàu nghèo
    65.かすか 微か な-adj. nhỏ nhặt, bé nhỏ
    66.かばう 庇う vt. bênh vực, bao che
    67.かんげん 還元 n./vi./vt. thu hồi, quay trở về
    68.かんさん 換算 n./vt. chuyển đổi (tiền tệ)
    69.がんじょう 頑丈 な-adj. chắc chắn, bền vững
    70.きざし 兆し n. dấu hiệu, điềm báo
    71.きまじめ 生真面目 な-adj. đứng đắn, nghiêm túc, nghiêm chỉnh
    72.きゃしゃ 華奢 n./な-adj. hoa hòe, lòe loẹt, sặc sỡ
    73.ばかばかしい 馬鹿馬鹿しい い-adj. thật nực cười, thật ngu xuẩn
    74.このましい 好ましい い-adj. rất được ưa thích, thích thú
    75.はげる 剥げる vi. tróc ra
    76.はらはら adv./vi. căng thẳng vì lo sợ / (lá) rơi đầy
    77.ひいては adv. chỉ vì
    78.ひどり 日取り n. chọn ngày, quyết định ngày
    79.ひなた 日向 n. hướng nắng tốt, nơi có nắng chiếu tốt
    1.コンクール n. cuộc thi
    2.イラスト n. tranh vẽ
    3.わがさ 和傘 n. dù kiểu Nhật
    4.コントラスト n. tương phản
    5.しんさいん 審査員 n. giám khảo
    6.ひょうしょうしき 表彰式 n. lễ phát bằng khen
    7.イメージキャラクター n. nhân vật mẫu, tượng trưng
    8.がんこ 頑固 な-adj. cứng đầu
    9.がんしょ 願書 n. đơn xin
    10.トリミング n./vt. cắt
    11.スケッチ n./vt. vẽ phong cảnh
    12.ナンセンス n. không có ý nghĩa
    13.ファイル n. file
    14.ていぎ 定義 n./vt. định nghĩa
    15.きんせん 金銭 n. tiền bạc
    16.てんさい 天才 n. tài năng
    17.えいゆう 英雄 n. anh hùng
    18.きょうちゅう 胸中 n. trong lòng
    19.うきよえ 浮世絵 n. tranh Ukiyo (tranh Phù Thế)
    20.すいさつ 推察 n./vt. suy đoán
    21.あからさま な-adj. không giấu diếm, rõ ràng
    22.なげやり 投げやり n./な-adj. làm ẩu tả, không đàng hoàng
    23.ちらっと adv. liếc (nhìn), (nhìn) thoáng qua
    24.しずまりかえる 静まり返る vi. im bặt
    25.けはい 気配 n. bóng dáng
    26.ものづくり n. thủ công
    27.コンパクト n./な-adj. nhỏ gọn
    28.モーター n. động cơ
    29.パジャマ n. áo ngủ
    30.きごこち 着心地 n. cảm giác khi mặc
    31.きぬ 絹 n. lụa
    32.はいざい 廃材 n. phế liệu
    33.サイレン n.  Siren (tên ma nữ trong thần thoại Hy lạp)
    34.やさき 矢先 n. đầu mũi tên
    35.せんぼう 羨望 n./vi. ganh tỵ
    36.こみあげる vi. dâng trào
    37.ちょくりつ 直立 n./vi. đứng thẳng
    38.でんしんばしら 電信柱 n. cột điện tín hiệu
    39.かぞえたてる 数え立てる vt. đếm từng cái một
    40.たんちょう 単調 n./な-adj. đều đều, đơn điệu
    41.あからむ 赤らむ vi. đỏ lên
    42.かくり 隔離 n./vt. cách ly
    43.かんさん 閑散 な-adj./n. yên tĩnh
    44.あてはまる 当てはまる vi. thích hợp
    45.けねん 懸念 n./vt. chuyên tâm
    46.しめん 紙面 n. mặt giấy
    47.かつじ 活字 n. con chữ trên máy đánh chữ (khuôn chữ)
    48.ていりゅうじょ 停留所 n. nơi dừng lại
    49.おかす 冒す vt. bất chấp, không màn đến
    50.ろうどく 朗読 n./vt. đọc lên thành tiếng
    51.インテリ n. thành phần tri thức
    52.つぶる 瞑る vt. nhắm (mắt)
    53.てじゅん 手順 n. trình tự thao tác
    54.みせびらかす 見せびらかす vt. khoe khoang
    55.えんかつ 円滑 な-adj./n. trôi chảy, suôn sẻ
    56.うんよう 運用 n./vt. vận dụng
    57.おおすじ 大筋 n. đại khái
    58.すみやか 速やか な-adj. nhanh, (làm) ngay
    59.すんなり adv. mảnh khảnh
    60.せいぜん 整然 n./な-adj. trật tự
    61.せいめい 声明 n./vi./vt. thanh minh
    62.せかす 急かす vt. hối thúc
    63.そびえる vi. cao vút
    64.たずさわる 携わる vi. liên quan
    65.ちょくちょく adv. liên tục
    66.だるい い-adj. bủn rủn
    67.つっぱる 突っ張る vi. chống đỡ, căng
    68.たんいつ 単一 n./な-adj. đơn độc
    69.ずるずる adv. lê lết
    70.せじ 世辞 n. nịnh nọt
    71.まるごと 丸ごと adv. trọn vẹn, hoàn toàn
    72.めいちゅう 命中 n./vi. trúng (đích)
    73.めんぼく 面目 n. danh dự, thể diện
    74.もろい 脆い い-adj. giòn, dễ vỡ
    75.もよおす 催す vi./vt. mở màng, cử hành
    76.しとやか 淑やか な-adj. thanh nhã, duyên dáng
    77.じっくり adv. kỹ lưỡng, triệt để
    78.きしょう 希少 な-adj. hiếm có'''

    def is_kanji(word):
        for char in word:
            if ('\u4e00' <= char <= '\u9fff' or '\u3400' <= char <= '\u4dbf' or '\U00020000' <= char <= '\U0002a6df'):
                return True
        return False

    def get_meanning(string):
        text = string.replace(string.split('.')[0]+".","")
        split_strings = text.split(' ')
        meaning = ''
        
        if is_kanji(split_strings[1]):
            hiragana = split_strings[0]
            kanji = split_strings[1]
            verb = split_strings[2]
            if len(split_strings) > 4:
                meaning = split_strings[3]
                
                for i in range(4, len(split_strings)):
                    meaning =  meaning + " " + split_strings[i]
        else:
            hiragana = split_strings[0]
            kanji = split_strings[0]
            verb = split_strings[1]
            if len(split_strings) > 3:
                meaning = split_strings[2]
                
                for i in range(3, len(split_strings)):
                    meaning =  meaning + " " + split_strings[i]
        
        if kanji not in kanji_list:
            anki_card = AnkiCard(kanji=kanji, meaning=meaning)
            anki_card = fill_return_anki_card(anki_card)
            anki_cards.append(anki_card)
        else:
            print(f"Info: {kanji} is checked")
            
    anki_cards = []
    kanji_list = []
    with open("anki_card.csv", "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row

        for row in reader:
            kanji = row[0]  # Assuming kanji is stored in the first column
            kanji_list.append(kanji)

    for row in text.split('\n'):
        get_meanning(row)
    write_to_csv(anki_cards)
        

full_kanji_meaning()
