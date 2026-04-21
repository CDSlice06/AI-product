from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 简单成语库（可自行扩充）
IDIOMS = [
    "一帆风顺", "二龙戏珠", "三阳开泰", "四季平安", "五福临门",
    "六六大顺", "七星高照", "八方来财", "九九同心", "十全十美",
    "百花齐放", "万事如意", "心想事成", "花好月圆"
]

class IdiomGame:
    def __init__(self):
        self.current_idiom = random.choice(IDIOMS)
        self.game_history = []

    def get_random_idiom(self):
        return random.choice(IDIOMS)

    def get_ai_response(self, user_idiom):
        try:
            # 简单接龙规则：最后一个字开头
            last_char = self.current_idiom[-1]

            # 找一个以最后一个字开头的成语
            valid_idioms = [idiom for idiom in IDIOMS if idiom.startswith(last_char)]
            if not valid_idioms:
                return {
                    'success': False,
                    'error': 'AI接不上啦！你赢了！'
                }

            ai_idiom = random.choice(valid_idioms)

            # 记录历史
            self.game_history.append(user_idiom)
            self.game_history.append(ai_idiom)
            self.current_idiom = ai_idiom

            return {
                'success': True,
                'user_idiom': user_idiom,
                'ai_idiom': ai_idiom,
                'current_idiom': self.current_idiom,
                'history': self.game_history
            }

        except Exception as e:
            return {
                'success': False,
                'error': '对话失败'
            }

# 全局游戏实例
game = IdiomGame()

# 主页
@app.route('/')
def index():
    return send_file('index.html')
# 游戏接口
@app.route('/api/play', methods=['POST'])
def play_game():
    data = request.get_json()
    user_input = data.get('idiom', '').strip()

    if not user_input:
        return jsonify({'success': False, 'error': '请输入成语'})

    if len(user_input) != 4 or not all('\u4e00' <= char <= '\u9fff' for char in user_input):
        return jsonify({'success': False, 'error': '请输入有效的4字成语'})

    result = game.get_ai_response(user_input)
    return jsonify(result)

# 重新开始
@app.route('/api/restart', methods=['POST'])
def restart_game():
    new_idiom = game.get_random_idiom()
    game.current_idiom = new_idiom
    game.game_history = []
    return jsonify({
        'success': True,
        'message': '游戏已重新开始',
        'current_idiom': new_idiom,
        'history': []
    })

# 获取状态
@app.route('/api/status')
def game_status():
    return jsonify({
        'current_idiom': game.current_idiom,
        'history': game.game_history
    })

# 启动
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)