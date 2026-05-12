from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 폰트 등록 ──────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Malgun", "C:/Windows/Fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBd", "C:/Windows/Fonts/malgunbd.ttf"))
pdfmetrics.registerFont(TTFont("MalgunSl", "C:/Windows/Fonts/malgunsl.ttf"))

# ── 색상 팔레트 ─────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1B2A4A")
ACCENT    = colors.HexColor("#2563EB")
LIGHT_BG  = colors.HexColor("#F0F4FF")
GRAY_TEXT = colors.HexColor("#4B5563")
GRAY_LINE = colors.HexColor("#D1D5DB")
WHITE     = colors.white

W, H = A4
MARGIN = 18 * mm

# ── 스타일 정의 ─────────────────────────────────────────────────────────────
def s(name, font="Malgun", size=10, leading=14, color=colors.black, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          leading=leading, textColor=color, **kw)

ST = {
    "name":      s("name",  "MalgunBd", 26, 32, NAVY),
    "title":     s("title", "MalgunSl", 12, 18, ACCENT),
    "contact":   s("contact","Malgun",   9, 13, GRAY_TEXT),
    "sec_head":  s("sec_head","MalgunBd",11,15, WHITE),
    "item_title":s("item_title","MalgunBd",10,14, NAVY),
    "item_sub":  s("item_sub", "MalgunSl", 9, 13, ACCENT),
    "caption":   s("caption",  "Malgun",   8, 12, GRAY_TEXT),
    "body":      s("body",     "Malgun",   9, 14, GRAY_TEXT),
    "bullet":    s("bullet",   "Malgun",   9, 13, GRAY_TEXT, leftIndent=10),
    "tag":       s("tag",      "MalgunBd", 8, 11, ACCENT),
    "about":     s("about",    "Malgun",  9.5,15, GRAY_TEXT),
    "skill_key": s("skill_key","MalgunBd", 9, 13, NAVY),
    "award_item":s("award_item","Malgun",  9, 13, GRAY_TEXT),
}

# ── 헬퍼 ───────────────────────────────────────────────────────────────────
def section_header(title):
    tbl = Table(
        [[Paragraph(title, ST["sec_head"])]],
        colWidths=[W - 2 * MARGIN]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    return tbl

def tag_row(tags: list[str]):
    cells = [Paragraph(f"◆ {t}", ST["tag"]) for t in tags]
    tbl = Table([cells], colWidths=[None]*len(cells))
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), LIGHT_BG),
        ("TOPPADDING", (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING",(0,0),(-1,-1), 6),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
    ]))
    return tbl

def bullet_para(text):
    return Paragraph(f"• {text}", ST["bullet"])

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GRAY_LINE, spaceAfter=4)

# ── 문서 구성 ───────────────────────────────────────────────────────────────
story = []

# ── 헤더 ───────────────────────────────────────────────────────────────────
header_data = [[
    Paragraph("조윤하  Cho Yun Ha", ST["name"]),
    Paragraph(
        "jojojo7391@gmail.com  |  010-5440-5086  |  github.com/JoeYunHa",
        ST["contact"]
    ),
]]
header_tbl = Table(header_data, colWidths=[95*mm, W-2*MARGIN-95*mm])
header_tbl.setStyle(TableStyle([
    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",   (0,0),(-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("BACKGROUND",   (0,0),(-1,-1), NAVY),
    ("LEFTPADDING",  (0,0),(0,-1),  10),
    ("RIGHTPADDING", (1,0),(1,-1),  10),
    ("ALIGN",        (1,0),(1,-1),  "RIGHT"),
]))
story.append(header_tbl)

# 직함 배너
title_tbl = Table(
    [[Paragraph("신입 백엔드 개발자", ST["title"])]],
    colWidths=[W - 2 * MARGIN]
)
title_tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), LIGHT_BG),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 10),
]))
story.append(title_tbl)
story.append(Spacer(1, 5*mm))

# ── ABOUT ──────────────────────────────────────────────────────────────────
story.append(section_header("ABOUT"))
story.append(Spacer(1, 3*mm))
about_lines = [
    "<b>성능 병목을 계측·분석·구조 재설계로 해결하는 신입 백엔드 개발자</b>입니다.",
    "Spring Boot · FastAPI 기반 REST API 설계, WebSocket 실시간 통신, AWS 클라우드 아키텍처를 직접 설계·구현했습니다.",
    "문제가 발생하면 데이터로 원인을 파악하고, 아키텍처 수준의 근본 해결을 지향합니다.",
]
for line in about_lines:
    story.append(Paragraph(line, ST["about"]))
    story.append(Spacer(1, 2*mm))
story.append(Spacer(1, 3*mm))

# ── 기술 스택 ──────────────────────────────────────────────────────────────
story.append(section_header("SKILLS"))
story.append(Spacer(1, 3*mm))
skills = [
    ("주력 언어",    "Java · Python"),
    ("Frameworks",  "Spring Boot · FastAPI"),
    ("Cloud & Infra","AWS (Lambda · EC2 · RDS · S3 · API Gateway) · Docker · Nginx · Redis"),
    ("기타",         "C++ · JavaScript · TypeScript · WebSocket · SQL · Git"),
]
for key, val in skills:
    row_tbl = Table(
        [[Paragraph(key, ST["skill_key"]), Paragraph(val, ST["body"])]],
        colWidths=[32*mm, W-2*MARGIN-32*mm]
    )
    row_tbl.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING", (0,0),(-1,-1), 4),
    ]))
    story.append(row_tbl)
story.append(Spacer(1, 4*mm))

# ── EXPERIENCE ─────────────────────────────────────────────────────────────
story.append(section_header("EXPERIENCE"))
story.append(Spacer(1, 3*mm))

experiences = [
    {
        "title":   "RealGain",
        "sub":     "기술 자문 계약직",
        "caption": "2026.02 – 2026.06",
        "tags":    ["Python", "AI/ML", "FastAPI", "Hot-standby"],
        "project": "원자력 발전소 RCP 진동 감시 시스템 RCPVMS 개발",
        "bullets": [
            "3계층 탐지 파이프라인: 앙상블(ResNet18 + OrbitCNN1D) → OOD 탐지 → MAE 재구성 오차(Transformer). 컴포넌트별 Graceful Degradation 설계",
            "물리 정보 인코딩: 4채널 스펙트로그램 — Im(Gxy)로 와류 방향 명시 인코딩",
            "XAI: Integrated Gradients(30-step) + GradCAM 히트맵으로 예측 근거 시각화",
            "Hot-standby 워커 풀: Python inference daemon 사전 적재, 콜드 스타트 비용 0, 워커 크래시 → 자동 재시작",
        ],
    },
    {
        "title":   "RealGain",
        "sub":     "현장실습",
        "caption": "2026.01 – 2026.02",
        "tags":    ["Electron", "React", "Python", "C++", "IPC"],
        "project": "산업용 계측 시스템(NIMS) 데이터 통합 처리 데스크톱 앱 NIMS I/O Simulator 개발",
        "bullets": [
            "Electron · React · Python · C++ N-API Addon 4개 런타임 멀티 아키텍처 설계 및 구현",
            "커스텀 바이너리 IPC 프로토콜 설계: 전송 크기 61% 감소, 역직렬화 218× 향상",
            "DLL 비스레드 안전 문제 → C++ 단일 워커 스레드 + TSFN 패턴으로 아키텍처 수준 해결",
            "Canvas 2D 뷰포트 다운샘플 렌더러로 수백만 샘플 파형 고성능 렌더링",
        ],
    },
]

for exp in experiences:
    block = []
    meta = Table(
        [[Paragraph(exp["title"], ST["item_title"]),
          Paragraph(exp["caption"], ST["caption"])]],
        colWidths=[W-2*MARGIN-35*mm, 35*mm]
    )
    meta.setStyle(TableStyle([
        ("ALIGN",      (1,0),(1,-1), "RIGHT"),
        ("VALIGN",     (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 1),
    ]))
    block.append(meta)
    block.append(Paragraph(exp["sub"], ST["item_sub"]))
    block.append(Spacer(1, 1.5*mm))
    block.append(tag_row(exp["tags"]))
    block.append(Spacer(1, 1.5*mm))
    block.append(Paragraph(exp["project"], ST["body"]))
    block.append(Spacer(1, 1*mm))
    for b in exp["bullets"]:
        block.append(bullet_para(b))
    block.append(Spacer(1, 4*mm))
    story.append(KeepTogether(block))

# ── PROJECTS ───────────────────────────────────────────────────────────────
story.append(section_header("PROJECTS"))
story.append(Spacer(1, 3*mm))

projects = [
    {
        "title":   "kindMap",
        "sub":     "팀장 | 경로 탐색 알고리즘 · 시스템 아키텍처 · DB 설계 단독 담당 / PM",
        "caption": "2025.08 – 2025.11",
        "desc":    "교통약자 유형별 최적 경로 탐색 및 편의시설 안내 지도 서비스 (인하대학교 졸업작품)",
        "tags":    ["Python", "FastAPI", "AWS", "Docker", "Nginx", "C++", "XGBoost", "LangChain"],
        "bullets": [
            "경로 탐색 알고리즘 단독 설계·구현 — 19분 → 1초 달성 (서울 지하철 실데이터 기준)",
            "Predecessor pointer 경량화, epsilon-pruning, C++ 탐색 엔진, 토폴로지 캐시 사전 로딩, Marking 전략",
            "부하 테스트 실측: RPS 75배 향상, 알고리즘 수행 시간 99% 이상 감소",
            "AWS Bedrock + LangChain 기반 지하철 편의시설 AI 챗봇 구현 (RAG)",
            "XGBoost 서울 지하철 혼잡도 예측 모델 (R² 0.9151)",
            "Nginx Reverse Proxy + Load Balancing, AWS Lambda · RDS · S3 아키텍처",
        ],
    },
    {
        "title":   "수담(手談)",
        "sub":     "기술 총책임자 | 백엔드 전 담당 (시스템 아키텍처 · DB 설계 · API · WebSocket)",
        "caption": "2025.07 – 2025.09",
        "desc":    "텍스트/음성과 3D 아바타 수어 영상 간 실시간 양방향 번역 AI 서비스",
        "tags":    ["Python", "FastAPI", "WebSocket", "Redis", "AWS", "Claude API"],
        "bullets": [
            "AI I/O Spec 미확정 블로커 → 초기 모델 이식으로 선제적 테스트 환경 구축, 백엔드 의존성 제거",
            "프록시 계층 제거, AI 서버 ↔ WebSocket 직접 연결 아키텍처로 재설계",
            "정적 데이터 캐시 사전 적재로 불필요한 DB 접근 제거, O(1) 조회 구현",
            "WebSocket 프레임 처리 응답 시간 1,000ms → 100ms (로컬 부하 테스트 실측, 90% 이상 감소)",
        ],
    },
]

for proj in projects:
    block = []
    meta = Table(
        [[Paragraph(proj["title"], ST["item_title"]),
          Paragraph(proj["caption"], ST["caption"])]],
        colWidths=[W-2*MARGIN-35*mm, 35*mm]
    )
    meta.setStyle(TableStyle([
        ("ALIGN",      (1,0),(1,-1), "RIGHT"),
        ("VALIGN",     (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 1),
    ]))
    block.append(meta)
    block.append(Paragraph(proj["sub"], ST["item_sub"]))
    block.append(Spacer(1, 1.5*mm))
    block.append(tag_row(proj["tags"]))
    block.append(Spacer(1, 1.5*mm))
    block.append(Paragraph(proj["desc"], ST["body"]))
    block.append(Spacer(1, 1*mm))
    for b in proj["bullets"]:
        block.append(bullet_para(b))
    block.append(Spacer(1, 4*mm))
    story.append(KeepTogether(block))

# ── EDUCATION ──────────────────────────────────────────────────────────────
story.append(section_header("EDUCATION"))
story.append(Spacer(1, 3*mm))
edu_tbl = Table(
    [[Paragraph("인하대학교", ST["item_title"]),
      Paragraph("2020 – 2026.08 (졸업예정)", ST["caption"])],
     [Paragraph("컴퓨터공학과", ST["item_sub"]), ""]],
    colWidths=[W-2*MARGIN-40*mm, 40*mm]
)
edu_tbl.setStyle(TableStyle([
    ("ALIGN",      (1,0),(1,-1), "RIGHT"),
    ("VALIGN",     (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0),(-1,-1), 2),
    ("BOTTOMPADDING",(0,0),(-1,-1), 2),
]))
story.append(edu_tbl)
story.append(Spacer(1, 4*mm))

# ── 수상 & 자격증 ──────────────────────────────────────────────────────────
story.append(section_header("AWARDS & CERTIFICATIONS"))
story.append(Spacer(1, 3*mm))

awards_data = [
    ["날짜", "수상명", "주관"],
    ["2025.06", "Korea Software Empowerment Bootcamp MINI PROJECT 우수 교육생", "정보통신기획평가원"],
    ["2025.08", "K-SoftVation Showcase 우수상", "정보통신기획평가원"],
    ["2025.10", "2025 오픈소스SW 페스티벌 프로젝트 부문 최우수상 (총장상)", "인하대학교 SW중심대학사업단"],
    ["2025.12", "탄소중립 INNOVACATION ACADEMY 대상 — 개인역량 강화 부문", "인하대학교 SW중심대학사업단"],
    ["2025.12", "탄소중립 INNOVACATION ACADEMY 최종 발표회 대상 — 팀 프로젝트 부문", "인하대학교 SW중심대학사업단"],
]

cert_data = [
    ["취득일", "자격증명", "발급기관"],
    ["2026.03", "SQLD (SQL 개발자)", "한국데이터산업진흥원"],
    ["2025.09", "AWS Certified Cloud Practitioner", "Amazon Web Services (Foundational)"],
    ["2025.05", "TOPCIT 수준 3", "정보통신기획평가원"],
    ["2025.12", "탄소중립 SW/AI 엔지니어 인증서 등급 A", "인하대학교 SW중심대학사업단"],
]

def make_table(data, col_w):
    def cell(txt, bold=False):
        style = ST["skill_key"] if bold else ST["award_item"]
        return Paragraph(txt, style)
    rows = []
    for i, row in enumerate(data):
        rows.append([cell(c, bold=(i == 0)) for c in row])
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), LIGHT_BG),
        ("GRID",         (0,0),(-1,-1), 0.3, GRAY_LINE),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    return tbl

aw = W - 2 * MARGIN
story.append(Paragraph("수상", ST["item_title"]))
story.append(Spacer(1, 1.5*mm))
story.append(make_table(awards_data, [20*mm, aw - 55*mm, 35*mm]))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("자격증", ST["item_title"]))
story.append(Spacer(1, 1.5*mm))
story.append(make_table(cert_data, [20*mm, aw - 55*mm, 35*mm]))
story.append(Spacer(1, 4*mm))

# ── 활동 ───────────────────────────────────────────────────────────────────
story.append(Paragraph("교육 및 활동", ST["item_title"]))
story.append(Spacer(1, 1.5*mm))
activities = [
    "2025년 탄소중립 INNOVACATION ACADEMY 4기 수료 (2025.08 – 2025.12) — 인하대학교 SW중심대학사업단",
    "2025년 K-Software Empowerment Bootcamp 4기 수료 (2025.01 – 2025.11) — 정보통신기획평가원",
    "Start-Up K-Shield Jr. 수료 (80H)",
]
for a in activities:
    story.append(bullet_para(a))
story.append(Spacer(1, 6*mm))

# ── 빌드 ───────────────────────────────────────────────────────────────────
output_path = "C:/Users/yunha/Desktop/조윤하_포트폴리오.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=MARGIN,
)
doc.build(story)
print(f"생성 완료: {output_path}")
