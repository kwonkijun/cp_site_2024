from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from jinja2 import Environment

# 절대 경로를 사용해야지 호스팅에서 경로를 읽을 수 있다
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "myblog.db")
print(db_path)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic')
def basic():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 커서가 반환하는 행을 딕셔너리처럼 접근할 수 있도록 설정합니다.
    cursor = conn.cursor()

    # 페이지 번호 가져오기 (기본값은 1)
    page = int(request.args.get('page', 1))
    items_per_page = 10
    offset = (page - 1) * items_per_page

    # 검색어 가져오기 (기본값은 빈 문자열)
    search_term = request.args.get('keyword', "")

    # 총 검색 결과 개수 조회
    cursor.execute("SELECT COUNT(*) FROM products WHERE name LIKE ? OR category LIKE ?", 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    total_results = cursor.fetchone()[0]
    total_pages = (total_results + items_per_page - 1) // items_per_page

    # 검색어를 포함하는 name 또는 category를 가진 레코드 검색
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ? LIMIT ? OFFSET ?", 
                   ('%' + search_term + '%', '%' + search_term + '%', items_per_page, offset))
    
    # fetchall() 호출 결과를 딕셔너리 리스트로 변환
    product_data = [dict(row) for row in cursor.fetchall()]

    # 연결 종료
    conn.close()

    return render_template('basic.html', product_data=product_data, current_page=page, total_pages=total_pages, keyword=search_term, total_results=total_results, page=page)

@app.route('/dynamic', methods=['GET'])
def dynamic():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 커서가 반환하는 행을 딕셔너리처럼 접근할 수 있도록 설정합니다.
    cursor = conn.cursor()

    # 페이지 번호 가져오기 (기본값은 1)
    page = int(request.args.get('page', 1))
    items_per_page = 10
    offset = (page - 1) * items_per_page

    # 검색어 가져오기 (기본값은 빈 문자열)
    search_term = request.args.get('keyword', "")
    print(search_term)

    # 총 검색 결과 개수 조회
    cursor.execute("SELECT COUNT(*) FROM products WHERE name LIKE ? OR category LIKE ?", 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    total_results = cursor.fetchone()[0]
    total_pages = (total_results + items_per_page - 1) // items_per_page

    # 검색어를 포함하는 name 또는 category를 가진 레코드 검색
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ? LIMIT ? OFFSET ?", 
                   ('%' + search_term + '%', '%' + search_term + '%', items_per_page, offset))
    
    # fetchall() 호출 결과를 딕셔너리 리스트로 변환
    product_data = [dict(row) for row in cursor.fetchall()]

    # 연결 종료
    conn.close()
    
     # 검색 결과와 페이지 정보를 JSON으로 반환
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Flask에서는 request.is_xhr로 AJAX 요청을 확인할 수 있습니다.
        return jsonify({
            'product_data': product_data,
            'total_pages': total_pages,
            'current_page': page,
            'keyword': search_term
        })
    else:
        return render_template('dynamic.html',  product_data=product_data, current_page=page, total_pages=total_pages, keyword=search_term, total_results=total_results, page=page)


# 정수를 문자열로 변환하고 천 단위마다 콤마를 삽입
def format_int_comma(value):
    return "{:,}".format(value)

# 커스텀 필터를 Flask의 Jinja2 환경에 추가
app.jinja_env.filters['intcomma'] = format_int_comma

if __name__ == '__main__':
    app.run(debug=True)