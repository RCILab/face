# 영상 활용 및 원본 교체 메모

최종 영상의 실험 조건과 비교 장면을 홈페이지의 개별 영상으로 배치했습니다. 컵 6개 조건, 컵·달걀의 5개 방법 비교, 케첩 닦기 4개 조건과 baseline 비교를 보여줍니다. 시연 수집·로봇 장착·알고리즘·표면 준비 장면도 포함합니다.

## 최종 영상 활용 범위

원본: `ICRA27_3998_VI_i-2.mp4`. 아래 시간은 원본 기준입니다.

| 원본 구간 | 내용 | 홈페이지 파일 / 위치 |
| --- | --- | --- |
| 00:25.5–00:41.5 | 핸드헬드 시연 수집 | `handheld-demo.mp4` / Hardware |
| 00:43.7–00:46.7 | 같은 도구를 로봇에 장착 | `robot-transfer.mp4` / Hardware |
| 00:47–00:58.2 | 컵 6개 조건 | `cup-nominal`, `cup-vertical`, `cup-horizontal`, `cup-pvc`, `cup-plastic`, `cup-wet` / Experiments |
| 00:48–00:58.2 | 6개 Success 표시 | `hero-loop.mp4` / 상단 미리보기 |
| 01:08–01:18.2 | 컵 3개 조건 × 5개 방법 비교 | `cup-baselines.mp4` / Quantitative evaluation |
| 01:21.5–01:37.2 | 달걀 5개 방법 비교 | `egg-comparison.mp4` / Quantitative evaluation |
| 01:41.2–02:06.2 | 알고리즘 세 단계 | `method-walkthrough.mp4` / Method 펼침 영역 |
| 02:12.5–02:20.7 | Direct Force 닦기 비교 | `wiping-baseline.mp4` / Additional experiments |
| 02:22–02:25 | 물·비누 및 다른 접시 준비 | `surface-preparation.mp4` / 펼침 영역 |
| 02:25–02:35.6 | FACE 닦기 4개 조건 | `wiping-nominal`, `wiping-wet`, `wiping-soapy`, `wiping-unseen`, `ketchup-wiping.mp4` / Additional experiments |

클립은 모두 `static/videos/`, 포스터는 `static/images/`에 있습니다. 원본 전체 영상도 Video 섹션에 유지합니다. 컵 방법 비교의 세 행은 nominal / wet plastic shell / horizontally wrinkled cup입니다.

## 추출과 재생

- 기본 자료와 hero·달걀·닦기 통합 영상: `scripts/prepare_assets.py`.
- 조건별 크롭과 나머지 장면: `scripts/prepare_gallery.py`. 구간·크롭·최종 길이는 `scripts/gallery-manifest.json`에도 기록합니다.
- 실험 결과가 보이는 마지막 프레임을 1초 유지한 뒤 반복합니다. 시연·준비·알고리즘 클립에는 추가 정지 시간을 넣지 않습니다.
- 원본 재생 속도와 Success/실패 표시를 유지합니다. 닦기 개별 크롭에서 제외된 원본 속도 표시는 카드에 기재합니다.
- `static/js/experiment-videos.js`가 화면에 보이는 영상만 무음 반복 재생합니다. 사용자가 일시정지하면 스크롤 후에도 유지합니다. JavaScript 없이도 기본 컨트롤로 재생할 수 있습니다.
- 상단 6 / 5 / 4는 각각 영상에 나온 컵 조건 수 / 비교 방법 수 / 닦기 조건 수입니다. 같은 몽타주에서 잘라낸 클립을 새로운 실험 횟수로 집계하지 않습니다.

## 원본 클립을 추가로 받으면

같은 경로의 MP4와 JPG를 교체할 수 있습니다. 원본 비율이 달라지면 `static/css/face.css`의 해당 갤러리 비율도 조정합니다. 클립 길이가 달라지면 manifest 및 `scripts/check_site.py`의 예상 길이를 갱신합니다. 교체 후 `python scripts/check_site.py`로 재생·모바일·링크를 확인합니다.

## 논문 수치 및 출처

- 논문: `_2026__ICRA___FACE (2).pdf` → `static/pdfs/face-paper.pdf` (원본 유지).
- 수치: 논문 Tables I / II. 방법별 컵 변형 20회, 표면 변화 30회, 달걀 25회이며 nominal 조건을 제외한 집계입니다.
- 닦기 영상은 논문 외 추가 실험으로 소개합니다. 영상에 보이는 결과와 논문의 정량 성공률을 구분합니다.
- 시연 수집은 물체 종류별 200회입니다. 홈페이지 영상 클립 수와 학습·평가 시행 횟수는 별개입니다.
- 익명 저자 표기를 유지하며, 저자 이름·게재 확정·코드 공개 일정은 임의로 추가하지 않습니다.

본문은 영어이며 이 파일은 편집용 한국어 메모입니다.
