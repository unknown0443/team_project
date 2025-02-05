import os
import django
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from django.conf import settings

# 🔹 Django 환경 설정 불러오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 🔹 PostgreSQL 연결 설정 (Django settings에서 직접 가져오기)
db_settings = settings.DATABASES["default"]
DATABASE_URL = f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
engine = create_engine(DATABASE_URL)

# 🔹 저장할 디렉토리 설정
save_dir = "D:/projects/mysite/static/images"
os.makedirs(save_dir, exist_ok=True)  # 폴더가 없으면 생성

# 🔹 한글 폰트 설정 (Windows 환경)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지

# 🔹 데이터 불러오기
query = "SELECT name, category, rating, review_count FROM youtube_api_place"
df = pd.read_sql(query, engine)

# ✅ 숫자로 변환 (에러 발생 방지) & NaN 값 0으로 처리
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0)

# ✅ 1. 카테고리별 장소 개수 (가로 크기 확대)
plt.figure(figsize=(10, 6))
df["category"].value_counts().plot(kind="bar", color=["blue", "red", "green"])
plt.title("📊 카테고리별 장소 개수", fontsize=18)
plt.xlabel("카테고리", fontsize=16)
plt.ylabel("개수", fontsize=16)
plt.xticks(rotation=30, ha="right", fontsize=14)  # ✅ 라벨 가독성 개선
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "visualization_category.png"), dpi=300)
plt.close()

# ✅ 2. 평점이 높은 TOP 10 장소 (가로 크기 확대)
top_rated = df.nlargest(10, "rating")
plt.figure(figsize=(10, 6))
plt.barh(top_rated["name"], top_rated["rating"], color="purple")
plt.xlabel("평점", fontsize=16)
plt.ylabel("장소", fontsize=16)
plt.title("⭐ 평점이 높은 TOP 10 장소", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "visualization_top_rated.png"), dpi=300)
plt.close()

# ✅ 3. 리뷰 수가 많은 TOP 10 장소 (가로 크기 확대)
top_reviewed = df.nlargest(10, "review_count")
plt.figure(figsize=(10, 6))
plt.barh(top_reviewed["name"], top_reviewed["review_count"], color="orange")
plt.xlabel("리뷰 개수", fontsize=16)
plt.ylabel("장소", fontsize=16)
plt.title("💬 리뷰 수가 많은 TOP 10 장소", fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "visualization_top_reviewed.png"), dpi=300)
plt.close()

print(f"✅ 시각화 이미지 저장 완료: {save_dir}")