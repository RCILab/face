# 자료 출처 및 편집 메모

## 적용 기준

현재 페이지의 연구 이미지는 제공 PDF에서, 실험 영상은 `FACE (2).pptx` 내부에서 직접 추출했다. 자체 제작 개념 GIF/MP4는 사용하지 않는다. 이후 materials에 제공된 전체 영상 `ICRA27_3998_VI_i-2.mp4`는 원본 스트림을 유지해 `face-full.mp4`로 추가했다. `robot-transfer`, `method-walkthrough`, standalone `surface-preparation`도 출처가 불명확한 기존 자산으로 남기지 않는다. 현재는 별도 하드웨어 섹션을 표시하지 않는다. 표면 준비 장면은 PPTX 닦기 원본 안에 포함되어 있다.

원본 PDF와 PPTX는 변경하지 않았다. `static/pdfs/face-paper.pdf`는 제공 PDF에서 저자·소속·이메일·프로젝트 주소·지원기관 감사문·메타데이터를 영구 삭제한 익명 사본이다. 원본과 사본의 해시는 manifest에 따로 기록한다.

## 영상 변환

- 총 48개 embedded video 중 34개를 사용한다. 조건·방법별 실험을 담되 인트로/아웃트로의 반복 영상은 중복 배치하지 않는다.
- HEVC 원본을 웹 호환 H.264/yuv420p MP4로 변환한다. `faststart`, 무음, 30fps, 원본 비율 보존.
- 원본 전체 구간을 사용한다. 시간 크롭·영상 크롭·배속 변경·새 Success 오버레이·마지막 프레임 추가 유지 없음. 프레임레이트 변환 때문에 길이는 프레임 단위로 반올림될 수 있다.
- 포스터는 각 변환 영상 7초 지점이다. 영상의 동작과 결과는 native controls로 끝까지 확인할 수 있다.
- 닦기 원본에는 준비 과정과 배속 표시가 이미 있다. FACE와 baseline의 배속이 서로 다를 수 있으므로 덮거나 동일 배속이라고 표기하지 않는다.
- 영상 파일 개수는 독립 시행 횟수가 아니다. 정량 결과는 논문의 평가 프로토콜을 따른다.

## 사용 영상 매핑

PPTX 내부 파일 이름은 `ppt/media/` 아래 경로다. 슬라이드 번호는 slide XML 번호이며 숨김 슬라이드를 포함한다.

| 홈페이지 영상 | PPTX 원본 | 슬라이드 | 웹 길이(초) |
| --- | --- | --- | --- |
| `cup-nominal.mp4` | `media19.mp4` | 3 | 15.00 |
| `cup-vertical.mp4` | `media18.mp4` | 3 | 15.00 |
| `cup-horizontal.mp4` | `media17.mp4` | 3 | 15.00 |
| `cup-pvc.mp4` | `media16.mp4` | 3 | 15.00 |
| `cup-plastic.mp4` | `media15.mp4` | 3 | 15.00 |
| `cup-wet.mp4` | `media14.mp4` | 3 | 15.00 |
| `compare-nominal-face.mp4` | `media20.mp4` | 5 | 10.00 |
| `compare-wet-face.mp4` | `media21.mp4` | 5 | 10.00 |
| `compare-wrinkled-face.mp4` | `media22.mp4` | 5 | 10.00 |
| `compare-wrinkled-vision.mp4` | `media23.mp4` | 5 | 10.00 |
| `compare-nominal-vision.mp4` | `media24.mp4` | 5 | 10.00 |
| `compare-wet-vision.mp4` | `media25.mp4` | 5 | 10.00 |
| `compare-wet-observation.mp4` | `media26.mp4` | 5 | 10.00 |
| `compare-wrinkled-observation.mp4` | `media27.mp4` | 5 | 10.00 |
| `compare-nominal-observation.mp4` | `media28.mp4` | 5 | 10.00 |
| `compare-wet-direct.mp4` | `media29.mp4` | 5 | 10.00 |
| `compare-wrinkled-direct.mp4` | `media30.mp4` | 5 | 10.00 |
| `compare-nominal-direct.mp4` | `media31.mp4` | 5 | 10.00 |
| `compare-nominal-analytic.mp4` | `media32.mp4` | 5 | 10.00 |
| `compare-wet-analytic.mp4` | `media33.mp4` | 5 | 10.00 |
| `compare-wrinkled-analytic.mp4` | `media34.mp4` | 5 | 10.00 |
| `egg-direct.mp4` | `media35.mp4` | 6 | 20.00 |
| `egg-observation.mp4` | `media36.mp4` | 6 | 20.00 |
| `egg-analytic.mp4` | `media37.mp4` | 6 | 20.00 |
| `egg-vision.mp4` | `media38.mp4` | 6 | 20.00 |
| `egg-face.mp4` | `media39.mp4` | 6 | 20.00 |
| `wiping-unseen-direct.mp4` | `media41.mp4` | 10 | 12.00 |
| `wiping-nominal-direct.mp4` | `media42.mp4` | 10 | 12.00 |
| `wiping-wet-direct.mp4` | `media43.mp4` | 10 | 12.00 |
| `wiping-soapy-direct.mp4` | `media44.mp4` | 10 | 12.00 |
| `wiping-unseen.mp4` | `media45.mp4` | 11 | 14.00 |
| `wiping-nominal.mp4` | `media46.mp4` | 11 | 15.00 |
| `wiping-wet.mp4` | `media47.mp4` | 11 | 15.00 |
| `wiping-soapy.mp4` | `media48.mp4` | 11 | 15.00 |

## 이미지와 출판 정보

- 논문 도판은 두 장만 캡션·번호 없이 크롭해 쓴다: 구조도(2쪽, `architecture.png`)와 접촉 인자 추정 결과(6쪽, `contact-estimation.png`). 크롭 좌표와 해시는 manifest에 있다. `contact-estimation.png`는 pdftoppm 216 dpi로 만들었고, `prepare_assets.py`를 다시 돌리면 같은 좌표로 PyMuPDF가 재생성한다.
- Figure 번호·논문 캡션은 웹 본문과 alt text에서도 제거했다. 각 섹션의 본문이 설명을 담당한다.
- 익명 심사용 페이지이므로 저자·소속·연락처·연구실 주소·식별 가능한 인용문을 표시하지 않는다. HTML 메타데이터에도 포함하지 않는다.
- 학회 채택, 공개 코드, arXiv ID, 출판 연도는 자료만으로 확정하지 않는다.

## 정량 결과 확인

컵 표면: PVC tape, plastic shell, wet plastic shell 각각 10회, 총 30회. 컵 변형: horizontal/vertical × mild/severe 각각 5회, 총 20회. 달걀: unseen 5개체 각각 5회, 총 25회. Nominal은 집계에서 제외한다. FACE는 각각 29/30, 13/20, 17/25다. 모든 비교군은 같은 데이터와 backbone을 쓰는 controlled variants로 설명한다.

닦기는 추가 정성 실험으로 제시하며 위 성공률 표에 합산하지 않는다. 컵에서 학습한 하나의 정책이 달걀·닦기를 모두 수행한다는 표현은 사용하지 않는다.

## 재현 및 유지보수

`python3 scripts/prepare_assets.py`로 자료를 다시 생성한다. PDF 익명화는 `scripts/anonymize_paper.py`가 자동 적용하며, 새 원고로 바꾸는 경우 삭제 영역을 다시 검토해야 한다. `scripts/media-manifest.json`에 원본 파일·embedded member·슬라이드·SHA-256·변환 결과·포스터·PDF 크롭 좌표가 기록된다. 자산을 바꾸면 manifest도 재생성한 뒤 `python3 scripts/check_site.py`로 검증한다.

과거 초안은 Git 이력에 보존되어 있다. 출처 없는 영상을 만드는 구형 `prepare_gallery.py`, `prepare_method_loops.py`와 그 manifest는 제거했다.

## 현재 노출 범위

버튼 아래에 FACE 컵 6개 조건과 공통 캡션 하나를 배치한다. 이어 Abstract → 전체 영상 → 방법별 비교 실험 → Generalization → Contact factor estimation(그림 + 세부 표) 순서다. 전체 영상은 `face-full.mp4`(172.90초)이며 원본 재인코딩 없이 메타데이터만 제거하고 faststart 처리했다. 포스터는 15초 지점이다.

컵 6개 갤러리는 상단에서 한 번만 보여준다. 아래에는 controlled comparisons와 달걀의 접촉 유지 실험을 배치한다. 닦기는 네 조건의 FACE·Direct force 8개 영상을 동시에 보여주며 조건 버튼은 쓰지 않는다. Paper/Code는 계속 비활성 상태다.
